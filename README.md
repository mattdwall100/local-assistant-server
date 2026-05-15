# Local AI Assistant Server

Python/FastAPI backend for a local-first voice assistant. The server owns the AI-heavy work: speech-to-text, LLM inference, tool execution, session memory, text-to-speech, and streamed audio responses. It is designed to run on a local Linux host or Docker container and serve lightweight microphone clients over the local network.

The companion `mic-client` project provides the edge microphone/speaker client. The client records audio and plays responses; this server performs inference and orchestration.

## What It Implements

- FastAPI API with `/health`, `/activity`, `/chat`, `/transcribe`, `/synthesize`, and `/speak`.
- Full voice pipeline: audio upload -> Faster Whisper STT -> Ollama LLM -> optional tool calls -> Piper TTS audio stream.
- Local inference focus using Ollama, Faster Whisper, Piper, ONNX voice assets, and configurable CPU/GPU STT device selection.
- Automated Pytest Unit and Integration suite 85%+ coverage
- Session-scoped in-memory conversation and paper/tool state.
- Custom tool registry with time/date tools and Hugging Face daily paper tools.
- Graceful fallback handling for STT, LLM, and TTS failures using generated or prerecorded fallback audio.
- Streaming byte responses for TTS playback by a remote client.
- Latency logging around API requests, STT, LLM, tool execution, TTS, and full pipeline execution.
- Docker, Docker Compose, PowerShell helper scripts, and draft systemd/CUDA deployment assets.

## Technologies

- Python 3.11-3.13
- FastAPI, Starlette, Uvicorn
- Pydantic v2, pydantic-settings
- Ollama Python client
- faster-whisper, CTranslate2
- Piper TTS, ONNX Runtime
- Hugging Face Hub API
- pytest, pytest-cov
- Ruff, mypy
- Docker, Docker Compose, systemd assets

## Engineering Practices Demonstrated

- Modular layered structure: API, orchestration, services, memory, tools, RAG extension point, config, logging.
- Dependency injection through `create_app(service_factory=...)`, enabling tests to replace real model clients with mocks.
- Typed request/response schemas and centralized environment configuration.
- Local-first architecture with clear client/server separation.
- Production-style observability through structured log messages and reusable latency measurement.
- Fault-tolerant pipeline design with fallback audio/text paths.
- Automated Unit, Integration test coverage for API contracts, streaming, pipeline behavior, memory, tools, and fallback flows.
- Deployment-aware design for local network hosting, containerization, and long-running Linux service operation.

## Repository Structure

```text
local-assistant-server/
|-- src/
|   `-- assistant_server/
|       |-- main.py                    # FastAPI app factory and Uvicorn entrypoint
|       |-- dependencies.py            # Service construction and app wiring
|       |-- api/
|       |   |-- router.py              # HTTP endpoints
|       |   |-- schemas.py             # Pydantic request/response models
|       |   `-- dependencies.py        # API dependency providers
|       |-- core/
|       |   |-- config.py              # Environment-backed settings
|       |   `-- logging.py             # Logging setup
|       |-- memory/
|       |   |-- store.py               # Session memory
|       |   `-- papers.py              # Session-scoped paper state
|       |-- orchestrator/
|       |   |-- pipeline.py            # STT -> LLM/tools -> TTS pipeline
|       |   |-- fallback.py            # Failure handling and fallback streams
|       |   `-- state.py               # Session state object
|       |-- services/
|       |   |-- llm/                   # Ollama abstraction
|       |   |-- stt/                   # Faster Whisper abstraction
|       |   `-- tts/                   # Piper abstraction
|       |-- tools/
|       |   |-- base.py                # Tool registry
|       |   |-- registry.py            # Legacy function schema registry
|       |   `-- implementations/       # Time/date and paper tools
|       |-- rag/
|       |   `-- retriever.py           # RAG extension point
|       `-- utils/
|           `-- latency_logger.py      # Latency context manager
|-- tests/
|   |-- Unit/                          # Unit tests for pipeline, memory, tools, fallback
|   |-- Integration/                   # API, streaming, fallback, paper-flow tests
|   |-- conftest.py
|   `-- mocks.py                       # Mock STT/LLM/TTS services
|-- models/
|   |-- llm/                           # Ollama modelfiles
|   `-- tts/                           # Piper ONNX voices
|-- assets/
|   |-- fallback_audio/                # Server fallback WAV files
|   |-- PROJECT_CONTEXT.md
|   `-- architecture.md
|-- deployment/
|   `-- systemd/local-assistant.service
|-- scripts/
|   |-- bootstrap.ps1
|   `-- run_server.ps1
|-- misc/
|   |-- Dockerfile_cuda
|   `-- docker-compose-cuda.yml
|-- Dockerfile
|-- docker-compose.yml
|-- pyproject.toml
|-- requirements.txt
|-- requirements-dev.txt
`-- .env.example
```

## Running Locally

This project currently targets Python `>=3.11,<3.14`.

```powershell
.\scripts\bootstrap.ps1
.\scripts\run_server.ps1
```

The server listens on the configured `API_HOST` and `API_PORT` values. Defaults are `0.0.0.0:8000`.

## Testing

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The test suite uses mock model clients so most API and orchestration behavior can be tested without starting Ollama, Faster Whisper, or Piper.

## Current Notes

- RAG is represented by a clean retriever extension point, but retrieval is not yet implemented.
- Raspberry Pi and wake-word support live in the client roadmap, not this server.
- Some deployment assets are templates/drafts and should be reviewed before production use.
