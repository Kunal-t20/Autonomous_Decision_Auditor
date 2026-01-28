from typing import TypedDict,List,Dict,Optional,Literal

class AuditState(TypedDict,total=False): # because it default take all entities but initially some entities like claim not present 
    #INPUT
    decision : str
    reasoning : str
    evidence : List[str]

    #AGENT GENERATED
    claims : List[str]
    evidence_map : Dict[str,Dict[str,List[str]]]
    inconsistencies : List[str]
    fragility_score : Optional[float]

    #FIANAL OUTPUT 
    confidence : Optional[float]
    verdict :Optional[Literal["ACCEPT","REJECT","ESCALATE"]]
    explaination : Optional[str]

