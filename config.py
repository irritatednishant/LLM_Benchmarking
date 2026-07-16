"""
Central configuration for the local LLM benchmark project.
Edit this file to change which models are compared and where results are saved.
"""

MODELS = [
    "llama3.2:3b",
    "phi4-mini",
    "mistral:7b",
]

RESULTS_CSV = "results/results.csv"
RESULTS_JSON = "results/results.json"
TEMPERATURE_RESULTS_CSV = "results/temperature_results.csv"
TEMPERATURE_RESULTS_JSON = "results/temperature_results.json"
