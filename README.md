# Local AI Assistant

Milestone 1 baseline repository for a local-network AI assistant.

This repo is structured to support long-term growth:
- Always-on Linux server (`FastAPI` + orchestration + inference services)
- Lightweight clients (Windows mic client first, Raspberry Pi client later)
- Placeholder modules for tools, memory, and RAG
- Deployment assets for local 24/7 operation

## Repository Structure

```text
.
├── assets/                      # Diagrams, docs assets, prompt assets
├── clients/                     # Lightweight client implementations
│   ├── raspberry-pi-client/
│   └── windows-mic-client/
├── deployment/                  # Deployment assets (systemd, container files later)
│   └── systemd/
├── scripts/                     # Local helper scripts
├── src/
│   └── assistant_server/
│       ├── api/                 # HTTP layer + request/response schemas
│       ├── core/                # Configuration and app-wide primitives
│       ├── memory/              # Conversation/session memory placeholder
│       ├── orchestrator/        # STT -> LLM/tool loop -> TTS coordination
│       ├── rag/                 # Retrieval placeholder
│       ├── services/            # STT/LLM/TTS abstractions
│       └── tools/               # Tool registration/execution placeholder
├── tests/
├── .env.example
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

## Quick Start (Windows PowerShell)

1. Create and activate a virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
pip install --upgrade pip
pip install -r requirements-dev.txt
```

3. Create a local environment file:
```powershell
Copy-Item .env.example .env
```

4. Run the API:
```powershell
uvicorn assistant_server.main:app --reload --host 0.0.0.0 --port 8000 --app-dir src
```

5. Test health endpoint:
```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
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
