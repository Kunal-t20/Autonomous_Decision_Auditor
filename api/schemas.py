from pydantic import BaseModel,Field
from typing  import List,Literal

class AuditRequest(BaseModel):
    decision : str
    resoning : str
    evidence :List[str]=Field(...,min,items=1) #minimum element must be one 

class AuditResponse(BaseModel):
    verdict : Literal["ACCEPT","REJECT","ESCALATE"]
    confidence : float=Field(...,ge=0.0,le=1.0)  #greater tha or equal 0 and less than or equal to 1 i.e range(0 to 1)
    explaination : str



