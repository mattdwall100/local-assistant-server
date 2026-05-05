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
├─ src/
│  └─ assistant_server/
│     ├─ __init__.py
│     ├─ main.py
│     ├─ dependencies.py
│     ├─ api/
│     │  ├─ __init__.py
│     │  ├─ dependencies.py
│     │  ├─ router.py
│     │  └─ schemas.py
│     ├─ core/
│     │  ├─ __init__.py
│     │  ├─ config.py
│     │  └─ logging.py
│     ├─ memory/
│     │  ├─ __init__.py
│     │  └─ store.py
│     ├─ orchestrator/
│     │  ├─ __init__.py
│     │  ├─ fallback.py
│     │  ├─ pipeline.py
│     │  └─ state.py
│     ├─ rag/
│     │  ├─ __init__.py
│     │  └─ retriever.py
│     ├─ services/
│     │  ├─ __init__.py
│     │  ├─ audio.py
│     │  ├─ llm/
│     │  │  ├─ __init__.py
│     │  │  ├─ base.py
│     │  │  └─ ollama_client.py
│     │  ├─ stt/
│     │  │  ├─ __init__.py
│     │  │  ├─ base.py
│     │  │  └─ fasterWhisper_client.py
│     │  └─ tts/
│     │     ├─ __init__.py
│     │     ├─ base.py
│     │     └─ piper_client.py
│     ├─ tools/
│     │  ├─ __init__.py
│     │  ├─ base.py
│     │  ├─ registry.py
│     │  └─ implementations/
│     │     └─ time.py
│     └─ utils/
│        ├─ __init__.py
│        └─ latency_logger.py
├─ clients/
│  ├─ README.md
│  ├─ raspberry-pi-client/
│  │  └─ README.md
│  └─ windows-mic-client/
│     ├─ README.md
│     ├─ requirements.txt
│     ├─ assets/
│     │  └─ fallback_audio/
│     │     ├─ bad_audio.wav
│     │     ├─ fallback_recieved.wav
│     │     └─ server_not_found.wav
│     ├─ src/
│     │  └─ windows_mic_client/
│     │     ├─ __init__.py
│     │     ├─ main.py
│     │     ├─ audio/
│     │     │  ├─ audio_utils.py
│     │     │  ├─ player.py
│     │     │  └─ recorder.py
│     │     ├─ client/
│     │     │  ├─ __init__.py
│     │     │  └─ assistant_api_client.py
│     │     ├─ core/
│     │     │  ├─ config.py
│     │     │  └─ logging.py
│     │     ├─ orchestrator/
│     │     │  ├─ __init__.py
│     │     │  ├─ fallback.py
│     │     │  └─ orchestrator.py
│     │     └─ utils/
│     │        └─ latency_logger.py
│     └─ tests/
│        ├─ test_config.py
│        └─ audio_files/
│           ├─ mic_20260427_223838.wav
│           ├─ mic_20260427_223912.wav
│           └─ mic_20260427_224230.wav
├─ service-manager/
│  ├─ README.md
│  ├─ pyproject.toml
│  ├─ config/
│  │  └─ services.yaml
│  ├─ deployment/
│  │  └─ systemd/
│  │     └─ server-manager.service
│  ├─ src/
│  │  └─ server_manager/
│  │     ├─ __init__.py
│  │     ├─ api.py
│  │     ├─ config.py
│  │     ├─ main.py
│  │     ├─ models.py
│  │     ├─ monitor.py
│  │     ├─ runtime.py
│  │     └─ state.py
│  └─ tests/
│     └─ test_health.py
├─ tests/
│  ├─ __init__.py
│  ├─ conftest.py
│  ├─ mocks.py
│  ├─ test_health.py
│  ├─ Unit/
│  │  ├─ test_fallback.py
│  │  ├─ test_memory.py
│  │  ├─ test_pipeline.py
│  │  └─ test_tools.py
│  └─ Integration/
│     ├─ test_api.py
│     ├─ test_fallback_flow.py
│     └─ test_streaming.py
├─ assets/
│  ├─ README.md
│  ├─ PROJECT_CONTEXT.md
│  ├─ architecture.md
│  └─ fallback_audio/
│     ├─ llm.wav
│     ├─ stt.wav
│     └─ tts.wav
├─ models/
│  ├─ llm/
│  │  ├─ alfred_modelfile_granite
│  │  └─ alfred_modelfile_qwen
│  └─ tts/
│     ├─ en_GB-alan-medium.onnx
│     └─ en_GB-alan-medium.onnx.json
├─ deployment/
│  ├─ README.md
│  └─ systemd/
│     └─ local-assistant.service
├─ scripts/
│  ├─ README.md
│  ├─ bootstrap.ps1
│  ├─ run_client.ps1
│  └─ run_server.ps1
├─ .env
├─ .env.example
├─ .gitignore
├─ LICENSE
├─ pyproject.toml
├─ README.md
├─ requirements.txt
└─ requirements-dev.txt

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
