"""
Temperature variance test — Phase 2, step 6.
Runs a small subset of prompts multiple times at temperature 0 and 0.7
for each model, so you can compare output consistency.

Usage:
    python temperature_test.py
"""

from config import MODELS, TEMPERATURE_RESULTS_CSV, TEMPERATURE_RESULTS_JSON
from prompts import TEMPERATURE_TEST_PROMPTS
from model_runner import run_model
from storage import save_to_csv, save_to_json

TEMPERATURES = (0, 0.7)
RUNS_PER_TEMPERATURE = 3


def main():
    all_results = []

    for model in MODELS:
        for prompt in TEMPERATURE_TEST_PROMPTS:
            for temp in TEMPERATURES:
                for run_number in range(1, RUNS_PER_TEMPERATURE + 1):
                    try:
                        result = run_model(model, prompt["text"], temperature=temp)
                        result["prompt_id"] = prompt["id"]
                        result["run_number"] = run_number

                        save_to_csv(result, filepath=TEMPERATURE_RESULTS_CSV)
                        all_results.append(result)
                        print(f"[ok] {model} | {prompt['id']} | temp={temp} | run={run_number}")

                    except Exception as e:
                        print(f"[error] {model} | {prompt['id']} | temp={temp} | run={run_number}: {e}")

    save_to_json(all_results, filepath=TEMPERATURE_RESULTS_JSON)
    print(f"\nDone. {len(all_results)} results saved to {TEMPERATURE_RESULTS_CSV} and {TEMPERATURE_RESULTS_JSON}")


if __name__ == "__main__":
    main()
