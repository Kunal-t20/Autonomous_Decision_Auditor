### Project Structure
.
```
│
├── app/
│   ├── main.py                  # FastAPI entry point
│
│   ├── api/
│   │   ├── routes.py             # API endpoints (/audit)
│   │   └── schemas.py            # Pydantic input/output models
│
│   ├── core/
│   │   ├── config.py             # Env vars, model names, thresholds
│   │   ├── constants.py          # Verdict enums, retry limits
│   │   └── logger.py             # Logging setup
│
│   ├── agents/
│   │   ├── state.py              # LangGraph TypedDict state
│   │   ├── claim_extractor.py    # Agent 1: extract claims
│   │   ├── evidence_mapper.py    # Agent 2: map evidence to claims
│   │   ├── consistency_checker.py# Agent 3: logic gap detection
│   │   ├── counterfactual.py     # Agent 4: stress test logic
│   │   └── confidence_scorer.py  # Agent 5: confidence calculation
│
│   ├── graph/
│   │   ├── audit_graph.py        # LangGraph definition
│   │   └── routing.py            # Conditional edges & flow control
│
│   ├── rules/
│   │   └── verdict_engine.py     # Rule-based ACCEPT / REJECT / ESCALATE
│
│   ├── services/
│   │   ├── normalizer.py         # Input cleanup & preprocessing
│   │   ├── explanation.py        # Human-readable explanation
│   │   └── persistence.py        # Save audit result to DB
│
│   ├── db/
│   │   ├── session.py            # Database connection
│   │   └── models.py             # Audit tables
│
│   └── utils/
│       ├── llm.py                # LLM wrapper (OpenAI etc.)
│       └── helpers.py            # Small reusable helpers
│
├── tests/
│   ├── test_claim_extraction.py
│   ├── test_evidence_mapping.py
│   ├── test_logic_check.py
│   ├── test_counterfactual.py
│   └── test_end_to_end.py
│
├── .env.example                  # Environment variables template
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container setup
└── README.md                     # Project explanation & usage

```



#### Python Virtual Environment Setup:

- python3 -m venv venv

- source venv/bin/activate

