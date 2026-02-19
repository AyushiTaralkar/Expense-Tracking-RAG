<!-- Copilot instructions for local AI coding agents -->
# Copilot instructions — ytrag

Quick summary
- Small Python data/LLM project using `langchain`, vectorstores (`chromadb`, `faiss-cpu`) and embeddings (`sentence-transformers`).
- Exploratory analysis lives in the notebook `notebook/Expenses.ipynb` and data in `data/Personal_Finance_Dataset.csv`.

Setup & run (discovered from this repo)
- Requires Python >= 3.11 (see `pyproject.toml`).
- Recommended quick setup (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If using the pyproject-based install:

```powershell
pip install -e .
```

Notebooks & data
- `notebook/Expenses.ipynb` is the exploratory interface; it reads `data/Personal_Finance_Dataset.csv` for examples. Prefer editing/adding code in small modules rather than stuffing logic only in notebooks.
- To run notebooks locally, ensure `ipykernel` is installed and optionally add a kernel for the venv:

```powershell
python -m ipykernel install --user --name=ytrag
jupyter notebook
```

Key patterns and conventions (from repository)
- Project is small and dependency-driven: check `pyproject.toml` for the canonical dependency list and `requirements.txt` for quick installs.
- LLM & vector patterns to expect: embeddings via `sentence-transformers`, persistent/vector storage via `chromadb` or `faiss-cpu`, orchestrated with `langchain` integrations (OpenAI & Google GenAI adapters are present in dependencies). Look for code that:
  - builds embeddings from text
  - indexes them into a vectorstore (`Chromadb`, `FAISS`)
  - uses a LangChain agent or chains to query those stores
- External connectors: OpenAI, Google GenAI (setup will require corresponding API keys in the environment; search for `OPENAI`, `GOOGLE` or similar env var usage if added).

Where to look first
- `main.py` — project entrypoint (currently minimal). Use it as a simple CLI/runner if you add lightweight scripts.
- `pyproject.toml` — authoritative dependency and metadata source.
- `notebook/Expenses.ipynb` and `data/Personal_Finance_Dataset.csv` — canonical examples to reproduce locally.

Agent guidance (concise, actionable)
- When adding code, keep LLM keys out of the repo and read them from env vars.
- Prefer small importable modules (e.g., `src/` or `ytrag/`) rather than only notebook cells; add tests next to modules when logic is non-trivial.
- Use the existing dependency list; add new heavy dependencies only when necessary and update `pyproject.toml`.
- When creating vector indexes, document which vectorstore backend is being used (Chromadb vs FAISS) and include reproducible init code (embedding model name, vectorstore path/config).

Examples from this repo
- Load dataset: `pd.read_csv('data/Personal_Finance_Dataset.csv')` (used in `notebook/Expenses.ipynb`).
- Environment: follow `pyproject.toml` for Python version and packages.

Missing / not present
- No CI workflows, tests, or existing `.github` instructions were found — this file initializes basic guidance.

If anything above is unclear or you want more detail (example snippets for LangChain chains, a project layout suggestion, or a small test harness), tell me which part to expand.
