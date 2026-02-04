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
│        # check all agent and engine also end to end project text 
│
├── .env.example                  # Environment variables template
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container setup
└── README.md                     # Project explanation & usage

```
#### Agents
- Extractor = reasoning into sentence claims
- evidence mapper = find proof for each claim
- consistency cheaker = check wheather the evidence or proof is True or False
- counterfactual = stress test/strenght of claim; check wheather claim strong or not
- confidence score = gives mathamatical proof 

#### Project flow
.
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
Verdict Engine (final decision)
```


#### Python Virtual Environment Setup:

- python3 -m venv venv

- source venv/bin/activate

