# Run All Demos in a venv

## Step 1 — Create and activate the venv

```bash
# From c:\Demo  (run in Command Prompt or PowerShell)
cd c:\Demo
python -m venv .venv
```

**Activate:**

```bash
# Command Prompt
.venv\Scripts\activate.bat

# PowerShell
.venv\Scripts\Activate.ps1

# Git Bash / WSL
source .venv/Scripts/activate
```

---

## Step 2 — Install all dependencies at once

```bash
pip install -r OmniAgent/requirements.txt
pip install -r chat_with_pdf/requirements.txt
pip install -r api_basics_demo/requirements.txt
pip install -r tokenization_demo/requirements.txt
pip install -r vector_algebra_demo/requirements.txt
```

---

## Step 3 — Set up your `.env`

Each demo reads from a `.env` file. Create one in `c:\Demo\` (or copy `OmniAgent\.env.example`):

```env
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

---

## Step 4 — Run each demo

| Demo | How to run |
|------|-----------|
| **OmniAgent** | Terminal 1: `python OmniAgent/services.py` → Terminal 2: `python OmniAgent/agent.py` |
| **chat_with_pdf** | `python chat_with_pdf/main_demo.py` |
| **api_basics_demo** | `python api_basics_demo/main_demo.py` |
| **tokenization_demo** | `python tokenization_demo/main_demo.py` |
| **vector_algebra_demo** | `python vector_algebra_demo/main_demo.py` |

---

## OmniAgent — two terminals required

```bash
# Terminal 1 (keep running)
python OmniAgent/services.py

# Terminal 2 (interactive agent)
python OmniAgent/agent.py
```

The agent auto-connects to the MCP server. Type requests like:

> `I'm a Gold member (test@email.com). Find me a flight to London tomorrow and a sci-fi movie tonight.`

---

> **Tip:** Always make sure the venv is activated (you'll see `(.venv)` in your prompt) before running any demo. The venv only needs to be created once; after that just activate and run.
