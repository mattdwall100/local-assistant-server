# Windows-specific bootstrap script for local development.
# When you switch to Linux, replace activation and interpreter paths with `.venv/bin/...`.

# Prefer the Windows launcher so we explicitly request a supported interpreter.
py -3.13 -m venv .venv

# Windows-specific virtual environment activation path.
.\.venv\Scripts\Activate.ps1

# Fail early if the launcher still produced an unsupported interpreter.
$pythonVersion = & .\.venv\Scripts\python.exe -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ($pythonVersion -notin @("3.11", "3.12", "3.13")) {
    throw "Unsupported Python version in .venv: $pythonVersion. Install Python 3.11-3.13 and rerun bootstrap."
}

# Use the venv interpreter directly because `pip install --upgrade pip` can fail when
# pip is upgrading itself on Windows.
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
