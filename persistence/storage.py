"""
Persistence Layer for persisting benchmark results to CSV (row-by-row, crash-safe)
and JSON (full dataset, written once at the end).
"""

import csv
import json
import os
from pathlib import Path

from core.config import RESULTS_CSV, RESULTS_JSON


def save_to_csv(result, filepath=RESULTS_CSV):
    """Append one result row to a CSV file. Drops 'response' and 'prompt' text
    to keep the file clean; full text is preserved in the JSON output."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    filtered_result = {k: v for k, v in result.items() if k not in ("response", "prompt")}
    file_exists = path.is_file()

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=filtered_result.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(filtered_result)


def save_to_json(results_list, filepath=RESULTS_JSON):
    """Write the full results list (including response/prompt text) as JSON."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(results_list, f, indent=2, ensure_ascii=False)

