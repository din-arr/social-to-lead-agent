from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    intent: str
    name: str
    email: str
    platform: str
    lead_captured: bool