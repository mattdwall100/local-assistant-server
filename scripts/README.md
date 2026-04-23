"""This is where all the scripts for setting up dev environment, testing etc will go"""

## `scripts/dev.ps1`

PowerShell helper for development setup.

Typical contents:

- activate venv
- install dependencies
- run lint/tests

## `scripts/run_server.ps1`

PowerShell command wrapper to run the server.

Typical contents:

- set env vars if needed
- run Uvicorn

This makes setup easier and more repeatable.
