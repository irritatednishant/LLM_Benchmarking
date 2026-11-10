"""
SLM Benchmark Application — Main CLI Entry Point.

Unified interface to run benchmarks, execute temperature tests, or perform analytics.

Usage:
    python main.py benchmark      Run the primary multi-model benchmark suite
    python main.py temperature    Run the temperature variance tests
    python main.py analyze        Generate comprehensive Rich comparison dashboard & academic report
    python main.py serve          Launch FastAPI server and interactive web telemetry dashboard
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
        help="Compute speed, memory, latency percentiles, and schema validity aggregations",
    )

    # Command: serve
    serve_parser = subparsers.add_parser(
        "serve",
        help="Launch the FastAPI web server and interactive telemetry dashboard",
    )
    serve_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface to bind (default: 127.0.0.1)",
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number to listen on (default: 8000)",
    )
    serve_parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code change",
    )

    args = parser.parse_args()

    if args.command == "benchmark":
        run_benchmark(models=args.models)
    elif args.command == "temperature":
        run_temperature_test(models=args.models, runs_per_temperature=args.runs)
    elif args.command == "analyze":
        run_analysis()
    elif args.command == "serve":
        import uvicorn
        print(f"\n🚀 Starting SLM Benchmark Web Platform at http://{args.host}:{args.port}/dashboard")
        print(f"📖 Interactive Swagger API Docs at: http://{args.host}:{args.port}/docs\n")
        uvicorn.run("api.app:app", host=args.host, port=args.port, reload=args.reload)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()

