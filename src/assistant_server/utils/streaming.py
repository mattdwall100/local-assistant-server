"""Helpers for the opt-in multiplexed (text + audio) ``/speak`` stream.

The stream is newline-delimited JSON. For each spoken sentence the server emits a
``text`` frame immediately followed by that sentence's ``audio`` frames, so a client
can render the chat text in lockstep with playback without bottlenecking the audio.
"""

import base64
import json
from collections.abc import Iterator, Sequence
from typing import Any
from urllib.parse import quote

from ollama import Message

# Media type used for content-negotiation and the multiplexed response body.
MULTIPLEX_MEDIA_TYPE = "application/x-ndjson"


def encode_tool_calls_header(tool_calls: Sequence[Message.ToolCall]) -> str:
    """Percent-encoded JSON list of ``{name, arguments}`` for the ``X-Tool-Calls`` header."""
    payload = [
        {"name": call.function.name, "arguments": dict(call.function.arguments or {})}
        for call in tool_calls
    ]
    return quote(json.dumps(payload, ensure_ascii=False))


def encode_header_text(text: str) -> str:
    """Percent-encode arbitrary text so it is safe to carry in an HTTP header."""
    return quote(text or "")


def tagged_stream_to_ndjson(tagged: Iterator[tuple[str, Any]]) -> Iterator[bytes]:
    """Serialise ``("text", str)`` / ``("audio", bytes)`` items to NDJSON byte-lines.

    Audio payloads are base64-encoded. A trailing ``done`` frame terminates the stream,
    and a failure mid-stream is surfaced as an ``error`` frame rather than a broken body.
    """
    seq = -1
    try:
        for kind, data in tagged:
            if kind == "text":
                seq += 1
                frame: dict[str, Any] = {"type": "text", "seq": seq, "data": data}
            elif kind == "audio":
                frame = {
                    "type": "audio",
                    "seq": seq,
                    "data": base64.b64encode(data).decode("ascii"),
                }
            else:
                frame = {"type": kind, "data": data}
            yield (json.dumps(frame, ensure_ascii=False) + "\n").encode("utf-8")
    except Exception as exc:  # surface mid-stream failures to the client as a frame
        yield (json.dumps({"type": "error", "data": str(exc)}) + "\n").encode("utf-8")
    yield b'{"type": "done"}\n'
