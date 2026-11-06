"""
Orchestration Layer — Main Benchmark Suite Runner.
Runs every configured prompt against every candidate model,
routing structured prompts through schema validation and general
prompts through the standard path, saving results to CSV + JSON via Persistence Layer.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path when executed directly
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.config import MODELS, RESULTS_CSV, RESULTS_JSON
from core.prompts import PROMPTS
from engine.runner import structured_prompt, general_prompt
from persistence.storage import save_to_csv, save_to_json


def run_benchmark(
    models=None,
    prompts=None,
    results_csv=RESULTS_CSV,
    results_json=RESULTS_JSON,
) -> list[dict]:
    """Execute the full benchmark matrix across models and prompts."""
    models = models or MODELS
    prompts = prompts or PROMPTS
    all_results = []

    print(f"Starting benchmark: {len(models)} models, {len(prompts)} prompts...")

    for model in models:
        for prompt in prompts:
            try:
                if prompt.get("type") == "structured":
                    response = structured_prompt(model, prompt["text"])
                else:
                    response = general_prompt(model, prompt["text"])

                result = {
                    **response,
                    "model": model,
                    "prompt": prompt["text"],
                    "prompt_id": prompt["id"],
                }

                save_to_csv(result, filepath=results_csv)
                all_results.append(result)
                print(f"[ok] {model} | {prompt['id']}")

            except Exception as e:
                print(f"[error] {model} | {prompt['id']}: {e}")

    save_to_json(all_results, filepath=results_json)
    print(f"\nDone. {len(all_results)} results saved to {results_csv} and {results_json}")
    return all_results


def main():
    run_benchmark()


if __name__ == "__main__":
    main()
