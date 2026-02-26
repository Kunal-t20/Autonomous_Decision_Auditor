from agents.claim_extractor import claim_extractor
from agents.evidence_mapper import evidence_mapper
from agents.consistency_checker import consistency_checker
from agents.counterfactual import counterfactual
from agents.confidence_scorer import confidence_score
from agents.state import AuditState

from agents.retry_handler import increment_retry


from langgraph.graph import StateGraph, END
from rules.verdict_engine import verdict_engine

from graph.routing import (
    route_after_evidence,
    route_after_consistency,
)

# ---------------- INIT GRAPH ----------------
graph = StateGraph(AuditState)

# ---------------- NODES ----------------
graph.add_node("claim_extractor", claim_extractor)
graph.add_node("evidence_mapper", evidence_mapper)

graph.add_node("retry_claim_extractor", increment_retry)

graph.add_node("consistency_checker", consistency_checker)
graph.add_node("counterfactual", counterfactual)
graph.add_node("confidence_scorer", confidence_score)
graph.add_node("verdict_engine", verdict_engine)

# ---------------- ENTRY ----------------
graph.set_entry_point("claim_extractor")

# ---------------- BASE FLOW ----------------
graph.add_edge("claim_extractor", "evidence_mapper")

graph.add_edge("retry_claim_extractor", "claim_extractor")
# ---------------- EVIDENCE ROUTER ----------------
graph.add_conditional_edges(
    "evidence_mapper",
    route_after_evidence,
    {
        "claim_extractor": "claim_extractor",
        "consistency_checker": "consistency_checker",
    },
)

# ---------------- CONSISTENCY ROUTER ----------------
graph.add_conditional_edges(
    "consistency_checker",
    route_after_consistency,
    {
        "counterfactual": "counterfactual",
        "confidence_scorer": "confidence_scorer",
    },
)

# ---------------- LINEAR FLOW ----------------
graph.add_edge("counterfactual", "confidence_scorer")
graph.add_edge("confidence_scorer", "verdict_engine")

# ---------------- END ----------------
graph.add_edge("verdict_engine", END)

# ---------------- COMPILE ----------------
audit_app = graph.compile()

