# Autonomous Decision Auditor (ADA)

An AI-powered multi-agent system that evaluates the logical strength of a reasoning paragraph, cross-references it against injected policies, and produces a final verdict with confidence, human-readable explanations, and granular breakdowns.

The system simulates a structured reasoning pipeline using multiple specialized agents coordinated through LangGraph, exposed via a FastAPI backend, and supported by persistence and explanation layers. Recent architecture upgrades include **Granular Explainability**, **Policy Injection**, and a **Human-in-the-Loop (HITL)** workflow.

## Features

- **Multi-Agent Logical Reasoning**: 6 distinct agents for extracting claims, mapping evidence, checking consistency, evaluating policies, and stress-testing reasoning.
- **Policy Injection**: Dynamically validate reasoning and evidence against injected, custom rules.
- **Granular Explainability**: Provides a robust breakdown including rule violations, stability checks, and counterfactual results alongside high-level verdicts.
- **Human-in-the-Loop (HITL) Resolution**: Escalates borderline or unresolvable claims to a human reviewer to finalize the verdict.
- **Conditional Routing & Retry Logic**: Uses LangGraph for complex conditional branching and retries to handle inadequate evidence mappings.
- **Confidence-Based Verdict Engine**: Evaluates evidence strength to accurately emit `ACCEPT`, `REJECT`, or `ESCALATE` verdicts.
- **Audit History Persistence**: Automatically stores reasoning, generated verdicts, confidence, explanations, breakdowns, and human review history to PostgreSQL.
- **LLM Caching**: Uses Redis for caching responses to optimize for latency and limit API cost.

## Project Structure

```
│
├── app/
│   └── main.py                  # FastAPI entry point
│
├── api/
│   ├── routes.py                # API endpoints (/audit, /audit/{id}/resolve)
│   └── schemas.py               # Pydantic input/output & HITL models
│
├── core/
│   ├── config.py                # Environment variables, thresholds
│   ├── constants.py             # Verdict enums & retry limits
│   └── logger.py                # Logging configuration
│
├── agents/
│   ├── state.py                 # Shared LangGraph state
│   ├── claim_extractor.py       # Agent 1: Extract claims
│   ├── evidence_mapper.py       # Agent 2: Map evidence
│   ├── consistency_checker.py   # Agent 3: Logical gap detection
│   ├── policy_checker.py        # Agent 4: Policy rule validation
│   ├── counterfactual.py        # Agent 5: Stress test reasoning
│   ├── confidence_scorer.py     # Agent 6: Confidence calculation
│   └── retry_handler.py         # Handles graph retry loops
│
├── graph/
│   ├── audit_graph.py           # LangGraph workflow definition
│   └── routing.py               # Conditional branching logic
│
├── rules/
│   └── verdict_engine.py        # Final ACCEPT / REJECT / ESCALATE rules
│
├── services/
│   ├── normalizer.py            # Input cleanup & preprocessing
│   ├── explanation.py           # Human-readable reasoning output
│   ├── persistence.py           # Database save logic
│   └── redis_cache.py           # In-memory caching
│
├── db/
│   ├── session.py               # Database connection
│   └── models.py                # Audit & HITL DB table definitions
│
├── utils/
│   ├── llm.py                   # LLM wrapper
│   └── helpers.py               # Reusable utility functions
│
├── frontend/                    # Vite + React Interface
├── tests/                       # Unit & integration tests
├── .env.example                 # Environment variable template
├── requirements.txt             # Dependencies
├── Dockerfile                   # Container configuration
└── README.md                    # Project documentation
```

## System Workflow

```
Reasoning Paragraph + Evidence + Policies
                   ↓
            Claim Extractor
                   ↓
            Evidence Mapper  ← (Retry Loop)
                   ↓
          Consistency Checker
                   ↓
            Policy Checker
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
                   ↓
       (Optional) HITL Resolution
```

## API Endpoints

### 1. `POST /audit`
Run an audit on a reasoning paragraph with optional evidence and custom policies.

**Request:**
```json
{
  "reasoning": "We should deploy to production today because the build passed.",
  "evidence": ["Build 403 passed successfully."],
  "policies": ["No Friday deployments allowed unless hotfix."]
}
```

**Response:**
```json
{
  "verdict": "ESCALATE",
  "confidence": 0.45,
  "explanation": {
    "summary": "Reasoning conflicts with Friday deployment policy."
  },
  "breakdown": {
    "rule_violations": [
      {
         "rule_name": "Friday Deployment Policy",
         "description": "Deployment requested on a Friday without hotfix justification."
      }
    ],
    "counterfactual": {
      "changed": true,
      "details": "If it were not Friday, it would be deployed."
    }
  },
  "audit_id": 105
}
```

### 2. `POST /audit/{audit_id}/resolve`
For scenarios where the audit engine returns an `ESCALATE` verdict, use this endpoint for Human-In-The-Loop resolution.

**Request:**
```json
{
  "final_verdict": "REJECT",
  "reviewer_notes": "Confirmed it is Friday and this is not a hotfix. Denied."
}
```


## Setup & Installation

**1. Clone Repository**
```bash
git clone https://github.com/Kunal-t20/Autonomous_Decision_Auditor.git
cd Autonomous_Decision_Auditor
```

**2. Local Environments Setup**
- **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configurations (`.env`)**
Copy `.env.example` to `.env` and set parameters up. The system optionally connects to PostgreSQL for audits and Redis for caching.

- **PostgreSQL**: Set `DATABASE_URL` (local or managed like Neon)
- **Redis Cache (Optional)**: Set `REDIS_ENABLED=true` and provide a `REDIS_URL`. If `true`, the system caches LLM outputs and applies rate-limiting logic.

**5. Run the Engine locally**
```bash
uvicorn app.main:app --reload
```
View REST endpoints on [Swagger UI](http://127.0.0.1:8000/docs).


## Frontend (`frontend/`)

The repository includes a modern React + Vite application tailored for an AI decision workflow viewing detailed break-downs.

```bash
cd frontend
npm install
# Set VITE_API_URL if needed
npm run dev
```

Run http://localhost:5173 to access the dashboard where you can request audits and resolve pending `ESCALATE` verdicts.


## Docker Usage

To run the backend server and its dependencies (Redis) with Docker:
```bash
docker compose up --build
```

You can seamlessly connect it to your external Neon Postgres DB by exporting the `DATABASE_URL` in `.env`.

## CI/CD Workflow
Tests are configured using pytest, orchestrated by GitHub Actions across `ci.yml`. Tests include API validation, Graph conditional routing verifications, logic handlers, and Redis + Postgres spin ups.
