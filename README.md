# 🧭 Career AI Assistant

A production-grade, multi-agent career analysis system built with **CrewAI** and **OpenAI GPT-4**. Upload a resume PDF and get an automated skill analysis, job recommendations, personalized interview questions, a 30/60/90-day learning roadmap, and a polished Markdown career report — all through a Streamlit UI.

## Architecture

Six specialized agents run as a sequential CrewAI pipeline, each depending on the outputs of the ones before it:

```
Resume PDF
   │
   ▼
Resume Analysis Agent      → structured resume summary
   │
   ▼
Skill Analysis Agent        → strengths, weaknesses, missing skills
   │
   ▼
Job Matching Agent          → ranked job recommendations
   │
   ▼
Interview Preparation Agent → tailored interview questions
   │
   ▼
Learning Roadmap Agent      → 30/60/90-day plan
   │
   ▼
Career Report Writer Agent  → career_report.md
```

## Project structure

```
career-ai-assistant/
├── agents/            # One CrewAI Agent definition per file
├── tasks/              # One CrewAI Task definition per agent, wired with context
├── tools/              # PDFSearchTool wrapper + raw text extraction
├── data/                # Scratch space for uploaded resumes (gitignored)
├── reports/             # Generated career_report.md files (gitignored)
├── tests/               # Pytest unit tests
├── app.py                # Streamlit UI
├── crew.py               # Crew orchestration (wires agents + tasks together)
├── config.py             # Centralized environment-variable configuration
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Clone and install

```bash
git clone <your-repo-url>
cd career-ai-assistant
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set your OpenAI API key:

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL_NAME=gpt-4o
```

### 3. Run the app

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (typically `http://localhost:8501`), upload a resume PDF, and click **Analyze**.

## Running tests

```bash
pytest tests/ -v
```

The included tests exercise the PDF-parsing utilities without requiring an API key or network access. For agent-level testing, mock the `LLM` and `PDFSearchTool` objects to avoid live API calls in CI.

## Design principles

- **Single Responsibility** — each agent and task lives in its own file with one clear job.
- **No hardcoded values** — every credential, model name, and path comes from `config.py`, which reads environment variables.
- **Deterministic fallback** — resume text is extracted with `pypdf` directly (not just RAG search) so the pipeline always has ground-truth text, even if semantic search misses a detail.
- **Exception handling** — the UI layer (`app.py`) catches and surfaces file, config, and pipeline errors distinctly rather than crashing.
- **Extensibility** — swapping in a different LLM provider only requires changing `config.py` and the `LLM(...)` instantiation in `agents/__init__.py`.

## Extending this project

- Add a new agent by creating a file in `agents/`, registering it in `agents/__init__.py`, and adding a matching task in `tasks/`.
- Add skill-radar or bar charts to the Streamlit UI using `matplotlib` or `plotly` fed from the Skill Analysis Agent's output.
- Swap `PDFSearchTool`'s embedder/LLM config in `tools/pdf_tool.py` to use a different provider (e.g. a local embedding model) without touching any other file.

## License

MIT — use freely for portfolio or production purposes.
