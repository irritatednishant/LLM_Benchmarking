"""
Core module containing configuration, prompts, and data validation schemas.
"""

from core.config import (
    BASE_DIR,
    MODELS,
    RESULTS_DIR,
    RESULTS_CSV,
    RESULTS_JSON,
    TEMPERATURE_RESULTS_CSV,
    TEMPERATURE_RESULTS_JSON,
)
from core.schemas import TicketAnalysisSchema
from core.prompts import PROMPTS, TEMPERATURE_TEST_PROMPTS

__all__ = [
    "BASE_DIR",
    "MODELS",
    "RESULTS_DIR",
    "RESULTS_CSV",
    "RESULTS_JSON",
    "TEMPERATURE_RESULTS_CSV",
    "TEMPERATURE_RESULTS_JSON",
    "TicketAnalysisSchema",
    "PROMPTS",
    "TEMPERATURE_TEST_PROMPTS",
]

