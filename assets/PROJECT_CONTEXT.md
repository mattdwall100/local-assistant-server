# Project Context: Local AI Voice Assistant Server

## Project Purpose
This project is a **local-first AI voice assistant** designed to run primarily on a dedicated **Linux server hosted on an old PC** on the local network. The assistant should be accessible from separate client devices and eventually support voice interaction through a dedicated microphone/speaker client, initially on a laptop and later on a Raspberry Pi.

The project serves **two purposes at once**:
1. Build a genuinely useful local AI assistant system.
2. Demonstrate **production-style AI engineering skills** for CV and interview purposes.

Future prompts should treat this repository as a **serious engineering project**, not a toy demo.

---

## End Goal
The final target system should have the following characteristics:

- **Linux server running 24/7** on an old PC.
- Server available on the **local network** and able to receive API requests at any time.
- A Python-based **AI orchestrator/API layer** running on the server.
- Local inference for:
  - **Speech-to-text (STT)**
  - **LLM inference**
  - **Text-to-speech (TTS)**
- As much inference as practical should run on the **server GPU**, but the design should remain robust if some components end up running on CPU due to hardware or driver constraints.
- A **tool-calling loop** in the orchestrator so the model can trigger external actions.
- Later support for:
  - **MCP-style integrations** (for example Zapier MCP or similar)
  - **direct API integrations** (for example Gmail / Google Calendar)
  - **RAG / local retrieval** hosted on the same box
- A separate **mic client** living outside the server:
  - first on the main laptop during development
  - later on a **Raspberry Pi** with microphone and speaker attached
- The external mic client should:
  - run **wake-word detection locally**
  - record audio after activation
  - send audio bytes to the server
  - receive a **streamed response** back from the server
  - play the returned audio through a speaker

---

## Core Architectural Principle
The system is intentionally split into:

### 1. Server-side intelligence
The server is the “brain” and should own:
- STT
- LLM inference
- tool execution
- conversation orchestration
- optional retrieval / RAG
- TTS
- response streaming

### 2. Client-side device interface
The client is the “edge device” and should own:
- microphone input
- speaker output
- wake-word detection
- recording control
- sending/receiving audio to/from the server

This means the client stays lightweight, while the server handles the expensive inference.

---

## Current Scope Priorities
The project should be built **incrementally**. Future prompts should prioritize the following implementation order unless explicitly told otherwise.

### Phase 0 — Hardware discovery
Determine the actual old-PC hardware:
- CPU
- RAM
- GPU model
- VRAM if applicable
- storage type (SSD/HDD)
- Linux compatibility
- likely GPU acceleration path

This phase is important because the final stack depends heavily on whether the GPU is NVIDIA, AMD, Intel, or effectively unusable for some workloads.

### Phase 1 — Text-only local assistant
Build the first working version as:
- local API
- local model runtime
- simple chat endpoint
- no voice yet
- no real tools yet

### Phase 2 — Orchestrator and dummy tool loop
Add:
- tool schema support
- tool execution loop
- dummy tools / placeholder tools

This should establish the architecture needed later for API integrations and MCP.

### Phase 3 — Voice pipeline on the server
Add:
- STT module
- TTS module
- unified `/assistant/respond` style endpoint accepting text or audio

### Phase 4 — Laptop mic client
Before introducing Raspberry Pi hardware, build a separate client running on the laptop that:
- records audio
- sends it to the server
- receives text/audio response
- plays returned audio

### Phase 5 — Linux server deployment
Move the server to the old PC running Linux and configure it to run 24/7 using:
- `systemd`
- LAN exposure via local IP / `0.0.0.0`
- proper service startup and logging

### Phase 6 — Wake word
Add wake-word handling first on the laptop client, then later on Raspberry Pi.

### Phase 7 — Streaming responses
Upgrade to partial / streaming response playback so the assistant begins speaking before the full response is complete.

### Phase 8 — Real tools, MCP, and RAG
Only after the base system is stable:
- replace dummy tools with real integrations
- optionally add MCP integration layer
- add local RAG / retrieval on the server

---

## Design Philosophy
Future prompts should preserve these design choices unless there is a strong reason to change them.

### 1. Keep the orchestrator as the core brain
The Python orchestration layer is the central piece of the project. It should:
- manage conversation state
- expose the external API
- call LLM runtime
- execute tools
- later coordinate retrieval and streaming

The orchestrator is more important than any single framework.

### 2. Avoid unnecessary framework bloat
The project should favor:
- clear architecture
- lightweight abstractions
- explicit tool calling
- understandable code

Over:
- over-engineered agent frameworks
- heavy abstractions for their own sake
- unnecessary “AI hype” stack choices

Use frameworks only when they add genuine value.

### 3. Build for extensibility early
Even before RAG and external tools are implemented, the repository should include clean extension points for:
- tool registry / tool execution
- retriever / RAG layer
- external action providers / integrations
- client implementations

### 4. Production-minded, but staged
The project should show awareness of production best practices without forcing premature complexity.

This means:
- reproducible environments matter
- deployment matters
- service boundaries matter
- logging matters
- stable interfaces matter

But it is acceptable to delay optional complexity such as Docker until the core assistant works.

---

## Technology Preferences
These are current preferred directions, not absolute rules.

### Preferred API/orchestrator stack
- **Python**
- **FastAPI** for HTTP API
- structured internal modules for:
  - llm
  - stt
  - tts
  - tools
  - rag
  - memory
  - client integration

### Preferred LLM runtime
- **Ollama** is the current preferred local LLM runtime.
- The orchestrator should talk to Ollama over its local API.
- Tool calling should be orchestrator-controlled.

### Preferred STT direction
Candidate options include:
- `faster-whisper`
- `whisper.cpp`

Choice should depend on GPU support and hardware compatibility.

### Preferred TTS direction
Candidate options include:
- `Piper`
- other lightweight local TTS systems only if justified

### Wake-word direction
Candidate option:
- `openWakeWord`

Wake-word detection is expected to be lightweight enough to run on a Raspberry Pi or similar edge client.

### Deployment direction
- Linux server on old PC
- `systemd` for always-on service management
- Docker for the API layer may be considered later, but is **not mandatory in the first implementation**

### Client direction
- first: Python client on Windows laptop
- later: Raspberry Pi mic/speaker client

---

## Architectural Boundaries to Preserve
Future prompts should keep these boundaries clear.

### External API boundary
There should be one clear server API boundary for the client to call.

Examples:
- `/chat`
- `/assistant/respond`
- `/transcribe`
- `/speak`

### Internal service boundaries
Inside the server application, keep clean separations between:
- API layer
- orchestrator logic
- LLM wrapper
- STT wrapper
- TTS wrapper
- tool registry and tool execution
- memory
- retrieval

These can live in the **same repository and same application**, but should remain logically separated.

### Client/server split
The mic client should remain a separate runtime from the server.

The client should not own heavy inference.
The server should not own microphone hardware directly.

---

## Skills This Project Is Intended to Demonstrate
Future prompts should help reinforce these skills where possible.

### Software / production engineering
- API design
- service architecture
- modular code structure
- reproducible deployment
- Linux service management
- logging and debugging
- networking on local infrastructure
- environment management

### AI / ML systems engineering
- local LLM inference
- tool calling
- orchestration loops
- retrieval-augmented generation
- voice pipeline design
- latency trade-offs
- model/runtime trade-offs
- streaming responses

### Systems design
- client/server separation
- edge vs central compute allocation
- hardware-aware architecture
- incremental roadmap design
- future-proof interfaces

### Product thinking
- build usable milestones
- prioritize low-latency UX
- preserve extensibility
- avoid unnecessary complexity

---

## Non-Goals / Things to Avoid
Future prompts should avoid pushing the project in these directions unless explicitly requested.

- Do **not** default to an over-complicated multi-agent architecture.
- Do **not** force LangChain or similar frameworks unless there is a clear reason.
- Do **not** assume Docker is mandatory for every component.
- Do **not** prematurely optimize for internet exposure; current default target is **local network only**.
- Do **not** move heavy inference onto the Raspberry Pi.
- Do **not** propose cloud-first designs unless explicitly requested.

---

## How Future Prompts Should Respond
When generating code, plans, or suggestions for this repository:

1. **Respect the staged roadmap.**
   Prefer the next milestone, not the final fully-complex system all at once.

2. **Preserve extensibility.**
   Even simple code should be written so RAG, tools, streaming, or a different client can be added later.

3. **Be explicit about trade-offs.**
   If suggesting a tool, framework, or runtime, explain why it fits this project.

4. **Prefer lightweight, production-sensible choices.**
   The goal is credible engineering, not maximal stack complexity.

5. **Assume the project is both a real build and a learning exercise.**
   Explanations should help the owner build understanding and ownership of the architecture.

---

## Short Summary for Quick Reference
This repository is for building a **local AI voice assistant** with:
- Linux server on an old PC
- Python orchestrator/API
- local STT + LLM + TTS
- client/server voice architecture
- future tool calling, MCP, and RAG
- laptop mic client first, Raspberry Pi client later
- always-on service on the local network
- production-minded but incrementally implemented design

