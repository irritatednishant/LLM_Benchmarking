"""
Orchestration Layer — Temperature Variance Suite Runner.
Runs a subset of prompts across varying temperature settings for each model
to evaluate generation stability and output variance.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path when executed directly
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.config import MODELS, TEMPERATURE_RESULTS_CSV, TEMPERATURE_RESULTS_JSON
from core.prompts import TEMPERATURE_TEST_PROMPTS
from engine.runner import run_model
from persistence.storage import save_to_csv, save_to_json

DEFAULT_TEMPERATURES = (0, 0.7)
DEFAULT_RUNS_PER_TEMPERATURE = 3


def run_temperature_test(
    models=None,
    prompts=None,
    temperatures=DEFAULT_TEMPERATURES,
    runs_per_temperature=DEFAULT_RUNS_PER_TEMPERATURE,
    results_csv=TEMPERATURE_RESULTS_CSV,
    results_json=TEMPERATURE_RESULTS_JSON,
) -> list[dict]:
    """Execute temperature variance benchmark suite."""
    models = models or MODELS
    prompts = prompts or TEMPERATURE_TEST_PROMPTS
    all_results = []

    print(
        f"Starting temperature test: {len(models)} models, "
        f"{len(prompts)} prompts, temperatures={temperatures}, "
        f"runs_per_temp={runs_per_temperature}..."
    )

    for model in models:
        for prompt in prompts:
            for temp in temperatures:
                for run_number in range(1, runs_per_temperature + 1):
                    try:
                        result = run_model(model, prompt["text"], temperature=temp)
                        result["prompt_id"] = prompt["id"]
                        result["run_number"] = run_number

                        save_to_csv(result, filepath=results_csv)
                        all_results.append(result)
                        print(f"[ok] {model} | {prompt['id']} | temp={temp} | run={run_number}")

                    except Exception as e:
                        print(f"[error] {model} | {prompt['id']} | temp={temp} | run={run_number}: {e}")

    save_to_json(all_results, filepath=results_json)
    print(f"\nDone. {len(all_results)} results saved to {results_csv} and {results_json}")
    return all_results


def main():
    run_temperature_test()


if __name__ == "__main__":
    main()
