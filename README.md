# 🧭 Career AI Assistant

A production-grade, multi-agent career analysis system built with **CrewAI** and **OpenAI's GPT-4o-mini**. Sign up, upload a resume PDF, and get an automated skill analysis, job recommendations, personalized interview questions, a 30/60/90-day learning roadmap, and a polished Markdown career report — all through a Streamlit UI, with authentication and report history persisted per account.

🔗 **[Live Demo](https://career-ai-assistant-afndomydsbgyp9gazfanqb.streamlit.app/)**

## Demo

**Landing page** — sign up or log in to get started:

![Login screen](docs/screenshots/01_upload.png)

**Resume summary, generated from the uploaded PDF:**

![Resume summary](docs/screenshots/02_resume_summary.png)

**Recommended jobs** — genuinely field-adaptive: this candidate's resume is for a Senior Aesthetic Doctor, and the Job Matching Agent correctly recommends *Aesthetic Medicine Consultant*, *Clinical Director of Aesthetic Services*, and similar roles - not generic tech titles:

![Recommended jobs](docs/screenshots/03_recommended_jobs.png)

**Personalized 30/60/90-day learning roadmap:**

![Learning roadmap](docs/screenshots/04_learning_roadmap.png)

**Overall resume score with justification:**

![Overall resume score](docs/screenshots/05_overall_score.png)

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
Career Report Writer Agent  → final Markdown report
```

Every agent adapts to the candidate's actual field rather than assuming a technical background — a non-technical resume gets non-technical job recommendations, skill categories, and interview questions (see the screenshots above).

The report is returned directly from CrewAI's in-memory result rather than round-tripped through disk, so the app works reliably even on hosting environments with restricted filesystem behavior. Resume text is extracted with `pypdf` and injected directly into the first agent's prompt - no RAG/vector-embedding step is used, which keeps the pipeline fast and lightweight enough to run on free-tier hosting.

Once generated, each report is saved to a SQLite database, scoped to the logged-in user's account, and browsable from the **History** page.

## Authentication

Accounts are secured with **bcrypt** password hashing - passwords are never stored in plaintext. Each user's resumes and reports are strictly isolated: no user can see another user's history, enforced at the database query level, not just the UI.

## Project structure

```
career-ai-assistant/
├── agents/              # One CrewAI Agent definition per file
├── tasks/               # One CrewAI Task definition per agent, wired with context
├── tools/                # Resume text extraction (pypdf)
├── database/             # SQLAlchemy models, session setup, auth, and CRUD functions
├── pages/                # Streamlit multi-page app - History page
├── docs/screenshots/      # README screenshots
├── data/                 # Scratch space for uploaded resumes (gitignored)
├── reports/               # Local report copies (gitignored)
├── tests/                # Pytest unit tests
├── app.py                 # Streamlit UI (main page, auth-gated)
├── auth_ui.py              # Login/signup UI components
├── styles.py               # Shared custom CSS, hero section, feature cards
├── crew.py                 # Crew orchestration (wires agents + tasks together, saves to DB)
├── config.py                # Centralized environment-variable configuration
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
OPENAI_MODEL_NAME=gpt-4o-mini
CREWAI_TOOLS_ALLOW_UNSAFE_PATHS=true
```

`gpt-4o-mini` is used by default - it comfortably fits typical account rate limits for this multi-agent pipeline while being significantly cheaper than larger models. Swap in a different model once your OpenAI account's usage tier supports it, if you want to compare quality.

### 3. Run the app

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (typically `http://localhost:8501`). Sign up for an account, upload a resume PDF, and click **Analyze**. Past reports are saved automatically and browsable from the **History** page in the sidebar.

## Deployment (Streamlit Community Cloud)

This app is deployed for free at [share.streamlit.io](https://share.streamlit.io):

1. Push this repo to GitHub (make sure `.env` is **not** committed - it's already gitignored).
2. Go to share.streamlit.io, sign in with GitHub, and click "New app".
3. Select this repo, branch `main`, and set the main file path to `app.py`.
4. Under **"Advanced settings" → "Python version"**, select **3.12** explicitly (newer Python versions can break some dependencies' compatibility layers).
5. Under **"Secrets"**, paste your environment variables in TOML format:
   ```toml
   OPENAI_API_KEY = "sk-proj-your-key-here"
   OPENAI_MODEL_NAME = "gpt-4o-mini"
   LLM_TEMPERATURE = "0.3"
   MAX_RESUME_FILE_MB = "10"
   REPORT_FILENAME = "career_report.md"
   CREWAI_TOOLS_ALLOW_UNSAFE_PATHS = "true"
   ```
6. Click **Deploy**.

**Known limitation:** Streamlit Community Cloud's filesystem is ephemeral - the SQLite database (`career_assistant.db`), registered accounts, and uploaded resumes are wiped whenever the app restarts or redeploys. This is expected for a free-tier portfolio demo. For persistent accounts and history in a production setting, swap SQLite for a hosted database (e.g. Supabase or Neon Postgres) by changing `DATABASE_URL` in `database/db.py` - no other code changes required.

## Running tests

```bash
pytest tests/ -v
```

The included tests exercise the PDF-parsing utilities without requiring an API key or network access.

## Design principles

- **Single Responsibility** — each agent, task, and database concern lives in its own file with one clear job.
- **No hardcoded values** — every credential, model name, and path comes from `config.py`, which reads environment variables.
- **Field-adaptive analysis** — agents identify the candidate's actual professional field before recommending jobs, skill categories, or interview topics, rather than defaulting to tech/AI roles for every resume.
- **Deterministic, lightweight resume reading** — resume text is extracted with `pypdf` and passed directly to agents as plain text, avoiding a RAG/vector-embedding step that proved unreliable on constrained hosting.
- **Result-in-memory over file I/O** — the generated report is taken directly from CrewAI's return value rather than read back from disk, avoiding filesystem quirks on some hosting platforms.
- **Secure by default** — passwords are hashed with bcrypt; every database query that touches resumes or reports is scoped to the requesting user's id.
- **Exception handling** — the UI layer (`app.py`) catches and surfaces file, config, and pipeline errors distinctly rather than crashing.
- **Extensibility** — swapping in a different LLM provider only requires changing `config.py` and the `LLM(...)` instantiation in `agents/__init__.py`.

## Extending this project

- Add a new agent by creating a file in `agents/`, registering it in `agents/__init__.py`, and adding a matching task in `tasks/`.
- Add skill-radar or bar charts to the Streamlit UI using `matplotlib` or `plotly` fed from the Skill Analysis Agent's output.
- Swap SQLite for PostgreSQL by changing `DATABASE_URL` in `database/db.py` — useful if deploying somewhere with persistent storage.
- Add email verification and password reset flows on top of the existing `database/auth.py` module.
- Containerize with Docker for deployment outside Streamlit Community Cloud.

## License

MIT — use freely for portfolio or production purposes.
