# Details

Date : 2026-04-28 09:20:35

Directory c:\\Users\\Admin\\Documents\\Projects\\Local-AI-Assistant\\local-assistant-server

Total : 58 files,  1445 codes, 124 comments, 333 blanks, all 1902 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [README.md](/README.md) | Markdown | 91 | 0 | 32 | 123 |
| [assets/README.md](/assets/README.md) | Markdown | 5 | 0 | 2 | 7 |
| [assets/architecture.md](/assets/architecture.md) | Markdown | 56 | 0 | 1 | 57 |
| [clients/README.md](/clients/README.md) | Markdown | 4 | 0 | 3 | 7 |
| [clients/raspberry-pi-client/README.md](/clients/raspberry-pi-client/README.md) | Markdown | 5 | 0 | 2 | 7 |
| [clients/windows-mic-client/README.md](/clients/windows-mic-client/README.md) | Markdown | 5 | 0 | 2 | 7 |
| [clients/windows-mic-client/requirements.txt](/clients/windows-mic-client/requirements.txt) | pip requirements | 5 | 0 | 1 | 6 |
| [clients/windows-mic-client/src/windows\_mic\_client/\_\_init\_\_.py](/clients/windows-mic-client/src/windows_mic_client/__init__.py) | Python | 0 | 1 | 1 | 2 |
| [clients/windows-mic-client/src/windows\_mic\_client/audio/audio\_utils.py](/clients/windows-mic-client/src/windows_mic_client/audio/audio_utils.py) | Python | 12 | 0 | 2 | 14 |
| [clients/windows-mic-client/src/windows\_mic\_client/audio/player.py](/clients/windows-mic-client/src/windows_mic_client/audio/player.py) | Python | 32 | 1 | 11 | 44 |
| [clients/windows-mic-client/src/windows\_mic\_client/audio/recorder.py](/clients/windows-mic-client/src/windows_mic_client/audio/recorder.py) | Python | 89 | 17 | 30 | 136 |
| [clients/windows-mic-client/src/windows\_mic\_client/client/\_\_init\_\_.py](/clients/windows-mic-client/src/windows_mic_client/client/__init__.py) | Python | 0 | 1 | 0 | 1 |
| [clients/windows-mic-client/src/windows\_mic\_client/client/assistant\_api\_client.py](/clients/windows-mic-client/src/windows_mic_client/client/assistant_api_client.py) | Python | 56 | 2 | 18 | 76 |
| [clients/windows-mic-client/src/windows\_mic\_client/config.py](/clients/windows-mic-client/src/windows_mic_client/config.py) | Python | 15 | 4 | 7 | 26 |
| [clients/windows-mic-client/src/windows\_mic\_client/main.py](/clients/windows-mic-client/src/windows_mic_client/main.py) | Python | 25 | 0 | 13 | 38 |
| [clients/windows-mic-client/src/windows\_mic\_client/orchestrator/\_\_init\_\_.py](/clients/windows-mic-client/src/windows_mic_client/orchestrator/__init__.py) | Python | 0 | 1 | 0 | 1 |
| [clients/windows-mic-client/src/windows\_mic\_client/orchestrator/orchestrator.py](/clients/windows-mic-client/src/windows_mic_client/orchestrator/orchestrator.py) | Python | 0 | 0 | 1 | 1 |
| [clients/windows-mic-client/tests/test\_config.py](/clients/windows-mic-client/tests/test_config.py) | Python | 35 | 0 | 13 | 48 |
| [deployment/README.md](/deployment/README.md) | Markdown | 4 | 0 | 3 | 7 |
| [models/tts/en\_GB-alan-medium.onnx.json](/models/tts/en_GB-alan-medium.onnx.json) | JSON | 493 | 0 | 0 | 493 |
| [requirements.txt](/requirements.txt) | pip requirements | 125 | 0 | 0 | 125 |
| [scripts/README.md](/scripts/README.md) | Markdown | 13 | 0 | 10 | 23 |
| [scripts/bootstrap.ps1](/scripts/bootstrap.ps1) | PowerShell | 9 | 7 | 5 | 21 |
| [scripts/run\_client.ps1](/scripts/run_client.ps1) | PowerShell | 3 | 0 | 0 | 3 |
| [scripts/run\_server.ps1](/scripts/run_server.ps1) | PowerShell | 1 | 0 | 1 | 2 |
| [src/assistant\_server/\_\_init\_\_.py](/src/assistant_server/__init__.py) | Python | 0 | 3 | 1 | 4 |
| [src/assistant\_server/api/\_\_init\_\_.py](/src/assistant_server/api/__init__.py) | Python | 0 | 1 | 2 | 3 |
| [src/assistant\_server/api/router.py](/src/assistant_server/api/router.py) | Python | 54 | 5 | 21 | 80 |
| [src/assistant\_server/api/schemas.py](/src/assistant_server/api/schemas.py) | Python | 11 | 1 | 9 | 21 |
| [src/assistant\_server/core/\_\_init\_\_.py](/src/assistant_server/core/__init__.py) | Python | 0 | 4 | 0 | 4 |
| [src/assistant\_server/core/config.py](/src/assistant_server/core/config.py) | Python | 18 | 4 | 7 | 29 |
| [src/assistant\_server/core/logging.py](/src/assistant_server/core/logging.py) | Python | 9 | 3 | 4 | 16 |
| [src/assistant\_server/main.py](/src/assistant_server/main.py) | Python | 12 | 0 | 7 | 19 |
| [src/assistant\_server/memory/\_\_init\_\_.py](/src/assistant_server/memory/__init__.py) | Python | 0 | 1 | 2 | 3 |
| [src/assistant\_server/memory/store.py](/src/assistant_server/memory/store.py) | Python | 16 | 2 | 7 | 25 |
| [src/assistant\_server/orchestrator/\_\_init\_\_.py](/src/assistant_server/orchestrator/__init__.py) | Python | 0 | 1 | 2 | 3 |
| [src/assistant\_server/orchestrator/pipeline.py](/src/assistant_server/orchestrator/pipeline.py) | Python | 71 | 19 | 30 | 120 |
| [src/assistant\_server/orchestrator/state.py](/src/assistant_server/orchestrator/state.py) | Python | 34 | 6 | 11 | 51 |
| [src/assistant\_server/rag/\_\_init\_\_.py](/src/assistant_server/rag/__init__.py) | Python | 0 | 1 | 2 | 3 |
| [src/assistant\_server/rag/retriever.py](/src/assistant_server/rag/retriever.py) | Python | 4 | 1 | 3 | 8 |
| [src/assistant\_server/services/\_\_init\_\_.py](/src/assistant_server/services/__init__.py) | Python | 0 | 1 | 2 | 3 |
| [src/assistant\_server/services/audio.py](/src/assistant_server/services/audio.py) | Python | 0 | 1 | 0 | 1 |
| [src/assistant\_server/services/llm/\_\_init\_\_.py](/src/assistant_server/services/llm/__init__.py) | Python | 0 | 1 | 0 | 1 |
| [src/assistant\_server/services/llm/base.py](/src/assistant_server/services/llm/base.py) | Python | 12 | 4 | 6 | 22 |
| [src/assistant\_server/services/llm/ollama\_client.py](/src/assistant_server/services/llm/ollama_client.py) | Python | 18 | 0 | 3 | 21 |
| [src/assistant\_server/services/stt/\_\_init\_\_.py](/src/assistant_server/services/stt/__init__.py) | Python | 0 | 1 | 0 | 1 |
| [src/assistant\_server/services/stt/base.py](/src/assistant_server/services/stt/base.py) | Python | 7 | 1 | 7 | 15 |
| [src/assistant\_server/services/stt/fasterWhisper\_client.py](/src/assistant_server/services/stt/fasterWhisper_client.py) | Python | 10 | 2 | 6 | 18 |
| [src/assistant\_server/services/tts/\_\_init\_\_.py](/src/assistant_server/services/tts/__init__.py) | Python | 0 | 1 | 1 | 2 |
| [src/assistant\_server/services/tts/base.py](/src/assistant_server/services/tts/base.py) | Python | 9 | 1 | 7 | 17 |
| [src/assistant\_server/services/tts/piper\_client.py](/src/assistant_server/services/tts/piper_client.py) | Python | 19 | 4 | 7 | 30 |
| [src/assistant\_server/tools/\_\_init\_\_.py](/src/assistant_server/tools/__init__.py) | Python | 0 | 1 | 2 | 3 |
| [src/assistant\_server/tools/base.py](/src/assistant_server/tools/base.py) | Python | 12 | 5 | 8 | 25 |
| [src/assistant\_server/tools/implementations/time.py](/src/assistant_server/tools/implementations/time.py) | Python | 7 | 3 | 3 | 13 |
| [src/assistant\_server/tools/registry.py](/src/assistant_server/tools/registry.py) | Python | 32 | 1 | 8 | 41 |
| [src/assistant\_server/utils/\_\_init\_\_.py](/src/assistant_server/utils/__init__.py) | Python | 0 | 1 | 0 | 1 |
| [tests/conftest.py](/tests/conftest.py) | Python | 0 | 10 | 1 | 11 |
| [tests/test\_health.py](/tests/test_health.py) | Python | 7 | 0 | 6 | 13 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)