# Autonomous Decision Auditor

An AI-powered multi-agent system that evaluates the logical strength of a reasoning paragraph and produces a final verdict with confidence and human-readable explanation.

The system simulates a structured reasoning pipeline using multiple specialized agents coordinated through LangGraph, exposed via a FastAPI backend, and supported by persistence and explanation layers.

## Features

Multi-Agent Logical Reasoning

Conditional Routing & Retry Logic

Confidence-Based Verdict Engine

Human-Readable Explanations

Audit History Persistence (Database)

REST API Interface

Modular & Scalable Architecture

### Project Structure
```
│
├── app/
│   ├── main.py                  # FastAPI entry point
│
│   ├── api/
│   │   ├── routes.py            # API endpoints (/audit)
│   │   └── schemas.py           # Pydantic input/output models
│
│   ├── core/
│   │   ├── config.py            # Environment variables, thresholds
│   │   ├── constants.py         # Verdict enums & retry limits
│   │   └── logger.py            # Logging configuration
│
│   ├── agents/
│   │   ├── state.py             # Shared LangGraph state
│   │   ├── claim_extractor.py   # Agent 1: Extract claims
│   │   ├── evidence_mapper.py   # Agent 2: Map evidence
│   │   ├── consistency_checker.py # Agent 3: Logical gap detection
│   │   ├── counterfactual.py    # Agent 4: Stress test reasoning
│   │   └── confidence_scorer.py # Agent 5: Confidence calculation
│
│   ├── graph/
│   │   ├── audit_graph.py       # LangGraph workflow definition
│   │   └── routing.py           # Conditional branching logic
│
│   ├── rules/
│   │   └── verdict_engine.py    # Final ACCEPT / REJECT / ESCALATE decision
│
│   ├── services/
│   │   ├── normalizer.py        # Input cleanup & preprocessing
│   │   ├── explanation.py       # Human-readable reasoning output
│   │   └── persistence.py       # Database save logic
│
│   ├── db/
│   │   ├── session.py           # Database connection
│   │   └── models.py            # Audit table definitions
│
│   └── utils/
│       ├── llm.py               # LLM wrapper
│       └── helpers.py           # Reusable utility functions
│
├── tests/                       # Unit & integration tests
├── .env.example                 # Environment variable template
├── requirements.txt             # Dependencies
├── Dockerfile                   # Container configuration
└── README.md                    # Project documentation
```


### Agents Overview
Agent	Responsibility
Claim Extractor	Breaks reasoning into individual claims
Evidence Mapper	Finds supporting proof for each claim
Consistency Checker	Detects logical contradictions
Counterfactual	Stress-tests the claim strength
Confidence Scorer	Produces a numerical confidence score

#### System Workflow
```
Reasoning Paragraph
      ↓
Claim Extractor
      ↓
Evidence Mapper
      ↓
Consistency Checker
      ↓
Counterfactual
      ↓
Confidence Scorer
      ↓
Verdict Engine
      ↓
Explanation Builder
      ↓
Database Persistence
      ↓
API Response
```

#### API Endpoint
POST /audit

- Request

{
  "reasoning": "AI improves productivity by automating repetitive tasks."
}


- Response

{
  "verdict": "ACCEPT",
  "confidence": 0.82,
  "explanation": "Strong supporting evidence and consistent logic detected."
}

#### Setup & Installation
1. Clone Repository
git clone https://github.com/Kunal-t20/Autonomous_Decision_Auditor.git
cd Autonomous_Decision_Auditor

2. Create Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate


Mac/Linux

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
- pip install -r requirements.txt

4. Run Server
- uvicorn app.main:app --reload


- Open Swagger UI:

http://127.0.0.1:8000/docs

#### Database

Uses **PostgreSQL** (e.g. **Neon**). Set `DATABASE_URL` in `.env` (see [`.env.example`](.env.example)).

Automatically stores audit history:

Reasoning

Verdict

Confidence

Explanation

Timestamp

#### Redis (optional)

Redis caches **LLM responses** (same model + temperature + prompt) to reduce latency and API cost. It does **not** replace PostgreSQL.

| Variable | Description |
|----------|-------------|
| `REDIS_ENABLED` | `true` / `false` (default: off for local dev without Redis) |
| `REDIS_URL` | e.g. `redis://localhost:6379/0` or managed Redis URL |
| `LLM_CACHE_TTL_SECONDS` | TTL for cached LLM text (default `86400`) |
| `LLM_CACHE_KEY_PREFIX` | Key namespace prefix (default `llm:v1:`) |
| `RATE_LIMIT_ENABLED` | `true` to rate-limit `POST /audit` (requires Redis) |
| `RATE_LIMIT_PER_MINUTE` | Max requests per client IP per minute |

- **`GET /health`** — reports `database` and `redis` status (`redis` is `disabled` when `REDIS_ENABLED=false`).

#### Frontend (`frontend/`)

The UI is **React + Vite** (JSX) with **TanStack Query**, themed for an AI/decision workflow (dark slate, cyan/violet accents).

```bash
cd frontend
npm install
copy .env.example .env   # optional: set VITE_API_URL (default http://127.0.0.1:8000)
npm run dev
```

Open **http://localhost:5173** with the API running on port **8000**. CORS allows the Vite dev origin.

- **`POST /audit`** — form submits reasoning, evidence lines, policy lines.
- **`POST /audit/{audit_id}/resolve`** — shown when verdict is **ESCALATE** (uses **`audit_id`** from the audit response).

Production build: `npm run build` → static files in `frontend/dist/`.

#### Docker

```bash
docker compose up --build
```

Set `DATABASE_URL` in `.env` (Neon or local Postgres). Compose wires **`REDIS_URL=redis://redis:6379/0`** for the app service.

#### CI/CD

GitHub Actions (`.github/workflows/ci.yml`):

- **test** job: Postgres + Redis services, `TEST_MODE=true`, `pytest`
- **docker-build** job: builds the Docker image (no push; add registry login + `push: true` when you deploy)
