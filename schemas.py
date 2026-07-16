"""
Pydantic schemas used to validate structured (JSON) model output.
Add new schemas here as you test additional structured task types.
"""

from pydantic import BaseModel
from typing import Literal


class TicketAnalysisSchema(BaseModel):
    category: Literal["billing", "technical", "account", "other"]
    priority: Literal["low", "medium", "high"]
    summary: str
    requires_escalation: bool
