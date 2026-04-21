from typing import Dict, List, TypedDict


class AgentState(TypedDict, total=False):
    messages: List[Dict[str, str]]
    intent: str
    name: str
    email: str
    platform: str
    lead_captured: bool
    lead_stage: str
    user_message: str
    response: str
