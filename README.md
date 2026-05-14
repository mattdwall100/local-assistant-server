# Local AI Assistant

Milestone 1 baseline repository for a local-network AI assistant.

This repo is structured to support long-term growth:

- Always-on Linux server (`FastAPI` + orchestration + inference services)
- Lightweight clients (Windows mic client first, Raspberry Pi client later)
- Placeholder modules for tools, memory, and RAG
- Deployment assets for local 24/7 operation

## Repository Structure

```
local-assistant-server/
├── src/
│   └── assistant_server/
│       ├── __init__.py
│       ├── main.py                  # FastAPI app entrypoint
│       ├── dependencies.py          # App-level dependency wiring
│       ├── api/
│       │   ├── __init__.py
│       │   ├── dependencies.py      # API dependency providers
│       │   ├── router.py            # HTTP routes
│       │   └── schemas.py           # Request/response models
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py            # Settings/config
│       │   └── logging.py           # Logging setup
│       ├── memory/
│       │   ├── __init__.py
│       │   ├── papers.py            # Paper-related memory helpers
│       │   └── store.py             # Memory store
│       ├── orchestrator/
│       │   ├── __init__.py
│       │   ├── fallback.py          # Fallback flow handling
│       │   ├── pipeline.py          # Main request pipeline
│       │   └── state.py             # Orchestration state models
│       ├── rag/
│       │   ├── __init__.py
│       │   └── retriever.py         # Retrieval logic
│       ├── services/
│       │   ├── __init__.py
│       │   ├── audio.py             # Audio utilities/service glue
│       │   ├── llm/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   └── ollama_client.py
│       │   ├── stt/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   └── fasterWhisper_client.py
│       │   └── tts/
│       │       ├── __init__.py
│       │       ├── base.py
│       │       └── piper_client.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── registry.py
│       │   └── implementations/
│       │       ├── papers.py
│       │       └── time.py
│       └── utils/
│           ├── __init__.py
│           └── latency_logger.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── mocks.py
│   ├── Unit/
│   │   ├── test_fallback.py
│   │   ├── test_memory.py
│   │   ├── test_pipeline.py
│   │   └── test_tools.py
│   └── Integration/
│       ├── test_api.py
│       ├── test_fallback_flow.py
│       └── test_streaming.py
├── models/
│   ├── llm/
│   │   ├── alfred_modelfile_granite
│   │   ├── alfred_modelfile_qwen
│   │   └── alfred_2_modelfile_granite4
│   └── tts/
│       ├── en_GB-alan-medium.onnx
│       ├── en_GB-alan-medium.onnx.json
│       ├── en_GB-northern_english_male-medium.onnx
│       └── en_GB-northern_english_male-medium.onnx.json
├── assets/
│   ├── README.md
│   ├── PROJECT_CONTEXT.md
│   ├── architecture.md
│   └── fallback_audio/
│       ├── llm.wav
│       ├── stt.wav
│       └── tts.wav
├── deployment/
│   ├── README.md
│   └── systemd/
│       └── local-assistant.service
├── scripts/
│   ├── README.md
│   ├── bootstrap.ps1
│   └── run_server.ps1
├── misc/
│   ├── Dockerfile_cuda
│   └── docker-compose-cuda.yml
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── LICENSE
├── .env.example
├── .env
└── .gitignore

```

## Start The App (Windows PowerShell)

This project currently works with Python `3.11` to `3.13`.
It does not support Python `3.14` yet.

Within a venv at root (local-assistant-server)

run scripts/start_server.ps1 for server
and scripts/start_client.ps1 for client

## If Startup Fails

- If `python --version` shows `3.14`, install Python `3.13` or `3.12` and recreate `.venv`.
- If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

- If `uvicorn` is not found, make sure the virtual environment is activated and rerun:

```powershell
python -m pip install -r requirements-dev.txt
```

## Milestone 1 Scope

- Modular project layout with placeholders for future features
- Typed API models (`Pydantic`)
- Centralized environment configuration (`pydantic-settings` + `.env`)
- Pinned runtime and development dependencies
- Basic test scaffold

## Next Milestone Preview

Milestone 2 should add:

- Real API request handling for audio bytes
- Initial stubbed STT/LLM/TTS flow behind orchestrator interface
- Better request logging and error mapping
