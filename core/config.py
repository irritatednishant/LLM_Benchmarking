"""
Central configuration for the local LLM benchmark project.
Edit this file to change which models are compared and where results are saved.
"""

from pathlib import Path

# Base project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

MODELS = [
    "llama3.2:3b",
    "phi4-mini",
    "mistral:7b",
]

RESULTS_DIR = BASE_DIR / "results"
RESULTS_CSV = str(RESULTS_DIR / "results.csv")
RESULTS_JSON = str(RESULTS_DIR / "results.json")
TEMPERATURE_RESULTS_CSV = str(RESULTS_DIR / "temperature_results.csv")
TEMPERATURE_RESULTS_JSON = str(RESULTS_DIR / "temperature_results.json")

