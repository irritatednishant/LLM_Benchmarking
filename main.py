"""
SLM Benchmark Application — Main CLI Entry Point.

Unified interface to run benchmarks, execute temperature tests, or perform analytics.

Usage:
    python main.py benchmark      Run the primary multi-model benchmark suite
    python main.py temperature    Run the temperature variance tests
    python main.py analyze        Generate summary comparison tables from collected data
"""

import argparse
import sys

from orchestration.benchmark import run_benchmark
from orchestration.temperature import run_temperature_test
from analytics.analyze import run_analysis


def main():
    parser = argparse.ArgumentParser(
        prog="slm-app",
        description="Local Small Language Model (SLM) Performance & Reliability Benchmark Platform",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: benchmark
    benchmark_parser = subparsers.add_parser(
        "benchmark",
        help="Run full benchmark matrix across configured models and prompts",
    )
    benchmark_parser.add_argument(
        "--models",
        nargs="+",
        help="Specific model(s) to benchmark (overrides core/config.py default)",
    )

    # Command: temperature
    temp_parser = subparsers.add_parser(
        "temperature",
        help="Run temperature variance tests across models",
    )
    temp_parser.add_argument(
        "--models",
        nargs="+",
        help="Specific model(s) to test",
    )
    temp_parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of iterations per temperature setting (default: 3)",
    )

    # Command: analyze
    subparsers.add_parser(
        "analyze",
        help="Compute speed, memory, and schema validity aggregations",
    )

    args = parser.parse_args()

    if args.command == "benchmark":
        run_benchmark(models=args.models)
    elif args.command == "temperature":
        run_temperature_test(models=args.models, runs_per_temperature=args.runs)
    elif args.command == "analyze":
        run_analysis()
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()

