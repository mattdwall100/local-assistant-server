r"""End-to-end latency benchmark for the /speak voice pipeline.

Drives the real AssistantPipeline in-process (no mocks): the input audio is
produced by Piper speaking a fixed utterance, fed back through Faster Whisper
STT, the FunctionGemma router, tool execution, the Granite main LLM, and Piper
TTS. Per-stage timings are read from the same `log_latency` events the server
emits in production; the full stream is consumed each run so streamed stages
(first LLM token, TTS synthesis) are actually exercised.

Run (from the repo root, with Ollama running and models pulled):

    .\.venv\Scripts\python.exe scripts\benchmark.py

Results are written to benchmarks/results.json and printed as a Markdown table.
"""

from __future__ import annotations

import ctypes
import json
import logging
import os
import re
import statistics
import sys
import time
from io import BytesIO
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"
sys.path.insert(0, str(SRC))

# The committed .env points ROUTING_MODEL_NAME at a tag that may not be pulled
# locally. Allow an override via the environment before settings are cached.
os.environ.setdefault("ROUTING_MODEL_NAME", os.environ.get("BENCH_ROUTING_MODEL", "functiongemma:latest"))

WARMUP_RUNS = 3
MEASURED_RUNS = int(os.environ.get("BENCH_RUNS", "15"))
UTTERANCE = "what time is it"

# Stages we report, in pipeline order. Keys are the log event names emitted by
# log_latency(); values are the human-readable labels for the table.
STAGE_LABELS = {
    "stt_completed": "STT (Faster Whisper)",
    "routing_llm_inference_completed": "Router LLM (FunctionGemma)",
    "tool_execution_completed": "Tool execution",
    "first_llm_token_received": "TTFT (first main-LLM token)",
    "tts_stream_setup": "TTS stream setup",
    "pipeline_completed": "Pipeline (to stream ready)",
}

_EVENT_RE = re.compile(r"^(?P<event>[^|]+?)\s*\|.*latency_ms=(?P<ms>\d+)")


class LatencyCapture(logging.Handler):
    """Collects latency_ms values keyed by event name for the current run."""

    def __init__(self) -> None:
        super().__init__(level=logging.DEBUG)
        self.current: dict[str, int] = {}

    def reset(self) -> None:
        self.current = {}

    def emit(self, record: logging.LogRecord) -> None:
        match = _EVENT_RE.match(record.getMessage())
        if match:
            self.current[match.group("event").strip()] = int(match.group("ms"))


def peak_working_set_mb() -> float:
    """Peak working set of THIS process in MB (Windows). LLM inference happens
    out-of-process in Ollama, so this covers STT + TTS + the app, not the LLMs."""
    if os.name != "nt":
        return 0.0

    class _Counters(ctypes.Structure):
        _fields_ = [
            ("cb", ctypes.c_uint32),
            ("PageFaultCount", ctypes.c_uint32),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    counters = _Counters()
    counters.cb = ctypes.sizeof(_Counters)
    kernel32 = ctypes.windll.kernel32
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p  # pseudo-handle must not truncate on x64
    handle = kernel32.GetCurrentProcess()
    ok = ctypes.windll.psapi.GetProcessMemoryInfo(
        ctypes.c_void_p(handle), ctypes.byref(counters), counters.cb
    )
    if not ok:
        return 0.0
    return counters.PeakWorkingSetSize / (1024 * 1024)


def pct(values: list[int], p: float) -> int:
    if not values:
        return 0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    rank = (len(ordered) - 1) * p
    lo = int(rank)
    hi = min(lo + 1, len(ordered) - 1)
    return round(ordered[lo] + (ordered[hi] - ordered[lo]) * (rank - lo))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    capture = LatencyCapture()
    logging.getLogger().addHandler(capture)

    # Imported after env + path are set so cached settings pick up the override.
    from assistant_server.dependencies import create_services  # noqa: E402
    from assistant_server.orchestrator.pipeline import AssistantPipeline  # noqa: E402

    print(f"Building services (routing={os.environ['ROUTING_MODEL_NAME']}) ...")
    services = create_services()
    pipeline = AssistantPipeline(
        stt=services.stt,
        llm=services.llm,
        routing_llm=services.routing_llm,
        tts=services.tts,
        fallback_handler=services.fallback_handler,
        memory=services.memory,
        tools=services.tools,
        retriever=services.retriever,
    )

    # Produce the STT input once: Piper speaks the fixed utterance to a WAV.
    wav_path = REPO_ROOT / "benchmarks" / "_bench_input.wav"
    wav_path.parent.mkdir(exist_ok=True)
    services.tts.synthesize_file(UTTERANCE, str(wav_path))
    audio_bytes = wav_path.read_bytes()
    print(f"Input WAV: {len(audio_bytes)} bytes ('{UTTERANCE}')")

    end_to_end: list[int] = []
    stage_samples: dict[str, list[int]] = {k: [] for k in STAGE_LABELS}
    transcripts: list[str] = []

    total = WARMUP_RUNS + MEASURED_RUNS
    for i in range(total):
        warm = i < WARMUP_RUNS
        capture.reset()
        start = time.perf_counter()
        result = pipeline.run(BytesIO(audio_bytes), session_id="")
        for _ in result.stream:  # consume fully to trigger streamed-stage timings
            pass
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        tag = "warmup" if warm else "measure"
        print(f"[{i + 1}/{total}] {tag} end_to_end={elapsed_ms}ms transcript={result.transcript!r}")
        if warm:
            continue

        end_to_end.append(elapsed_ms)
        transcripts.append(result.transcript.strip())
        for event, samples in stage_samples.items():
            if event in capture.current:
                samples.append(capture.current[event])

    peak_mb = peak_working_set_mb()

    def summarize(values: list[int]) -> dict[str, int]:
        return {
            "n": len(values),
            "p50_ms": pct(values, 0.50),
            "p95_ms": pct(values, 0.95),
            "min_ms": min(values) if values else 0,
            "max_ms": max(values) if values else 0,
        }

    results = {
        "utterance": UTTERANCE,
        "measured_runs": MEASURED_RUNS,
        "warmup_runs": WARMUP_RUNS,
        "device": "cpu",
        "routing_model": os.environ["ROUTING_MODEL_NAME"],
        "python_peak_working_set_mb": round(peak_mb, 1),
        "end_to_end": summarize(end_to_end),
        "stages": {
            STAGE_LABELS[event]: summarize(samples)
            for event, samples in stage_samples.items()
        },
    }

    out = REPO_ROOT / "benchmarks" / "results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("\n### Latency (CPU, n={} after {} warmups)\n".format(MEASURED_RUNS, WARMUP_RUNS))
    print("| Stage | p50 | p95 |")
    print("| --- | ---: | ---: |")
    print(f"| **End-to-end (/speak)** | **{results['end_to_end']['p50_ms']} ms** "
          f"| **{results['end_to_end']['p95_ms']} ms** |")
    for label, s in results["stages"].items():
        if s["n"]:
            print(f"| {label} | {s['p50_ms']} ms | {s['p95_ms']} ms |")
    print(f"\nPython process peak working set: {results['python_peak_working_set_mb']} MB "
          f"(excludes Ollama; LLMs run in the Ollama process)")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
