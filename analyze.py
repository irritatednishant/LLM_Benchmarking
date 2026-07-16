"""
Aggregates results.csv into per-model comparison tables for the final report.
Run after benchmark.py (and optionally temperature_test.py) have completed.

Usage:
    python analyze.py
"""

import pandas as pd
from config import RESULTS_CSV, TEMPERATURE_RESULTS_CSV


def summarize_performance(df):
    summary = df.groupby("model").agg(
        avg_latency=("latency", "mean"),
        avg_tokens_per_second=("tokens_per_second", "mean"),
        avg_memory_mb=("memory_mb", "mean"),
        prompts_run=("prompt_id", "count"),
    ).round(2)
    return summary


def summarize_validity(df):
    structured = df[df["prompt_type"] == "structured"]
    if structured.empty:
        return None
    return structured.groupby("model")["valid_json"].mean().round(3) * 100


def main():
    df = pd.read_csv(RESULTS_CSV)

    print("=== Speed & Memory Summary ===")
    print(summarize_performance(df))

    print("\n=== Structured Output Valid JSON Rate (%) ===")
    validity = summarize_validity(df)
    if validity is not None:
        print(validity)
    else:
        print("No structured-type rows found.")

    try:
        temp_df = pd.read_csv(TEMPERATURE_RESULTS_CSV)
        print("\n=== Temperature Test: rows collected per model/temperature ===")
        print(temp_df.groupby(["model", "temperature"]).size())
    except FileNotFoundError:
        print("\n(No temperature_results.csv found yet — run temperature_test.py first.)")


if __name__ == "__main__":
    main()
