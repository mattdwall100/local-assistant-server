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
|-- assets/                      # Diagrams, docs assets, prompt assets
|-- clients/                     # Lightweight client implementations
|   |-- raspberry-pi-client/
|   `-- windows-mic-client/
|-- deployment/                  # Deployment assets (systemd, container files later)
|   `-- systemd/
|-- scripts/                     # Local helper scripts
|-- src/
|   `-- assistant_server/
|       |-- api/                 # HTTP layer + request/response schemas
|       |-- core/                # Configuration and app-wide primitives
|       |-- memory/              # Conversation/session memory placeholder
|       |-- orchestrator/        # STT -> LLM/tool loop -> TTS coordination
|       |-- rag/                 # Retrieval placeholder
|       |-- services/            # STT/LLM/TTS abstractions
|       `-- tools/               # Tool registration/execution placeholder
|-- tests/
|-- .env.example
|-- pyproject.toml
|-- requirements.txt
`-- requirements-dev.txt
```

## Start The App (Windows PowerShell)

This project currently works with Python `3.11` to `3.13`.
It does not support Python `3.14` yet.

1. Check your Python version:

```powershell
python --version
```

2. Create a virtual environment:

```powershell
python -m venv .venv
```

3. Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

5. Create a local `.env` file:

```powershell
Copy-Item .env.example .env
```

6. Start the API from the repo root:

```powershell
python -m uvicorn assistant_server.main:app --app-dir src --host 127.0.0.1 --port 8000 --reload
```

7. In a second PowerShell window, test the server:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

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
