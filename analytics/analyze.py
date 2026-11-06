"""
Analytics Layer:
Aggregates benchmark CSV metrics into per-model comparison tables and performance summaries.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path when executed directly
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd
from core.config import RESULTS_CSV, TEMPERATURE_RESULTS_CSV


def summarize_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate speed, latency, and memory metrics grouped by model."""
    summary = df.groupby("model").agg(
        avg_latency=("latency", "mean"),
        avg_tokens_per_second=("tokens_per_second", "mean"),
        avg_memory_mb=("memory_mb", "mean"),
        prompts_run=("prompt_id", "count"),
    ).round(2)
    return summary


def summarize_validity(df: pd.DataFrame) -> pd.Series | None:
    """Calculate percentage of valid JSON schema outputs for structured prompts."""
    structured = df[df["prompt_type"] == "structured"]
    if structured.empty:
        return None
    return structured.groupby("model")["valid_json"].mean().round(3) * 100


def run_analysis(
    results_csv: str = RESULTS_CSV,
    temp_results_csv: str = TEMPERATURE_RESULTS_CSV,
) -> None:
    """Execute analysis and output formatted comparison tables."""
    if not Path(results_csv).exists():
        print(f"Results file '{results_csv}' not found. Run benchmark first.")
        return

    df = pd.read_csv(results_csv)

    print("=== Speed & Memory Summary ===")
    print(summarize_performance(df))

    print("\n=== Structured Output Valid JSON Rate (%) ===")
    validity = summarize_validity(df)
    if validity is not None:
        print(validity)
    else:
        print("No structured-type rows found.")

    if Path(temp_results_csv).exists():
        temp_df = pd.read_csv(temp_results_csv)
        print("\n=== Temperature Test: rows collected per model/temperature ===")
        print(temp_df.groupby(["model", "temperature"]).size())
    else:
        print(f"\n(No {Path(temp_results_csv).name} found yet — run temperature test first.)")


def main():
    run_analysis()


if __name__ == "__main__":
    main()
