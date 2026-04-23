local-assistant-server/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── assets/
│ └── README.md
├── clients/
│ ├── README.md
│ ├── raspberry-pi-client/
│ │ └── README.md
│ └── windows-mic-client/
│ └── README.md
├── deployment/
│ ├── README.md
│ └── systemd/
│ └── local-assistant.service
├── scripts/
│ └── bootstrap.ps1
├── src/
│ └── assistant_server/
│ ├── **init**.py
│ ├── main.py
│ ├── api/
│ │ ├── **init**.py
│ │ ├── router.py
│ │ └── schemas.py
│ ├── core/
│ │ ├── **init**.py
│ │ ├── logging.py
│ │ └── config.py
│ ├── memory/
│ │ ├── **init**.py
│ │ └── store.py
│ ├── orchestrator/
│ │ ├── **init**.py
│ │ └── pipeline.py
│ ├── rag/
│ │ ├── **init**.py
│ │ └── retriever.py
│ ├── services/
│ │ ├── **init**.py
│ │ ├── llm.py
│ │ ├── stt.py
│ │ └── tts.py
│ ├── tools/
│ │ ├── **init**.py
│ │ └── registry.py
│ └── utils/
│ ├── **init**.py
│ └── time.py
└── tests/
└── test_health.py
