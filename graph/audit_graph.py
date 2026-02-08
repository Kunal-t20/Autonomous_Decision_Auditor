from agents.claim_extractor import claim_extractor
from agents.evidence_mapper import evidence_mapper
from agents.consistency_checker import consistency_checker
from agents.counterfactual import counterfactual
from agents.confidence_scorer import confidence_score
from agents.state import AuditState

from langgraph.graph import StateGraph,END
from rules.verdict_engine import verdict_engine


# INIT GRAPH
graph = StateGraph(AuditState)

# NODES
graph.add_node("claim_extractor", claim_extractor)
graph.add_node("evidence_mapper", evidence_mapper)
graph.add_node("consistency_checker", consistency_checker)
graph.add_node("counterfactual", counterfactual)
graph.add_node("confidence_scorer", confidence_score)
graph.add_node("verdict_engine", verdict_engine)

# ENTRY
graph.set_entry_point("claim_extractor")

# EDGES
graph.add_edge("claim_extractor","evidence_mapper")
graph.add_edge("evidence_mapper","consistency_checker")
graph.add_edge("consistency_checker","counterfactual")
graph.add_edge("counterfactual","confidence_scorer")
graph.add_edge("confidence_scorer","verdict_engine")
graph.add_edge("verdict_engine",END)

# COMPILE ONCE
audit_app = graph.compile()
