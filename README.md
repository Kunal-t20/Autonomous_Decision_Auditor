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

Default: SQLite

Automatically stores audit history:

Reasoning

Verdict

Confidence

Explanation

Timestamp