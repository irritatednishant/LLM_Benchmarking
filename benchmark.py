"""
Main benchmark runner — Phase 1 & 2.
Runs every prompt in PROMPTS against every model in MODELS,
routing structured prompts through schema validation and general
prompts through the plain path, then saves results to CSV + JSON.

Usage:
    python benchmark.py
"""

from config import MODELS, RESULTS_CSV, RESULTS_JSON
from prompts import PROMPTS
from model_runner import structured_prompt, general_prompt
from storage import save_to_csv, save_to_json


def main():
    all_results = []

    for model in MODELS:
        for prompt in PROMPTS:
            try:
                if prompt["type"] == "structured":
                    response = structured_prompt(model, prompt["text"])
                else:
                    response = general_prompt(model, prompt["text"])

                result = {**response, "model": model, "prompt": prompt["text"], "prompt_id": prompt["id"]}

                save_to_csv(result, filepath=RESULTS_CSV)
                all_results.append(result)
                print(f"[ok] {model} | {prompt['id']}")

            except Exception as e:
                print(f"[error] {model} | {prompt['id']}: {e}")

    save_to_json(all_results, filepath=RESULTS_JSON)
    print(f"\nDone. {len(all_results)} results saved to {RESULTS_CSV} and {RESULTS_JSON}")


if __name__ == "__main__":
    main()
