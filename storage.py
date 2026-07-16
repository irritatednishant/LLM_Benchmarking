"""
Functions for persisting benchmark results to CSV (row-by-row, crash-safe)
and JSON (full dataset, written once at the end).
"""

import csv
import json
import os


def save_to_csv(result, filepath="results/results.csv"):
    """Append one result row to a CSV file. Drops 'response' and 'prompt' text
    to keep the file clean; full text is preserved in the JSON output."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    filtered_result = {k: v for k, v in result.items() if k not in ("response", "prompt")}

    file_exists = os.path.isfile(filepath)

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=filtered_result.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(filtered_result)


def save_to_json(results_list, filepath="results/results.json"):
    """Write the full results list (including response/prompt text) as JSON."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results_list, f, indent=2, ensure_ascii=False)
