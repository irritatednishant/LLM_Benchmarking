"""
Pydantic schemas used to validate structured (JSON) model output.
Add new schemas here as you test additional structured task types.
"""

from typing import Literal
from pydantic import BaseModel


class TicketAnalysisSchema(BaseModel):
    category: Literal["billing", "technical", "account", "other"]
    priority: Literal["low", "medium", "high"]
    summary: str
    requires_escalation: bool

