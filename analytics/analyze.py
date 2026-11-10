"""
Analytics Layer:
Aggregates benchmark metrics into statistical comparison tables,
renders a comprehensive Rich terminal dashboard, and exports evaluation reports.
"""

import sys
from pathlib import Path
from typing import Optional

# Ensure project root is in sys.path when executed directly
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from core.config import RESULTS_CSV, TEMPERATURE_RESULTS_CSV
from analytics.metrics import (
    compute_comprehensive_metrics,
    generate_markdown_report,
    BENCHMARK_REPORT_MD,
)


def summarize_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Legacy helper: aggregate speed, latency, and memory metrics grouped by model."""
    summary = df.groupby("model").agg(
        avg_latency=("latency", "mean"),
        avg_tokens_per_second=("tokens_per_second", "mean"),
        avg_memory_mb=("memory_mb", "mean"),
        prompts_run=("prompt_id", "count"),
    ).round(2)
    return summary


def summarize_validity(df: pd.DataFrame) -> Optional[pd.Series]:
    """Legacy helper: calculate percentage of valid JSON schema outputs for structured prompts."""
    structured = df[df["prompt_type"] == "structured"]
    if structured.empty:
        return None
    return structured.groupby("model")["valid_json"].mean().round(3) * 100


def display_rich_dashboard(
    metrics: dict,
    report_path: Optional[Path] = None,
) -> None:
    """Render a multi-panel visual CLI dashboard with Rich."""
    console = Console()
    telemetry = metrics.get("telemetry", {})
    leaderboard = metrics.get("leaderboard", [])
    temp_stability = metrics.get("temperature_stability", [])
    recommendation = metrics.get("executive_recommendation", "")

    # Header Panel
    header_text = Text()
    header_text.append("SLM BENCHMARK PLATFORM ", style="bold cyan")
    header_text.append("— Diagnostic & Telemetry Suite\n", style="bold white")
    header_text.append(f"• Host OS: {telemetry.get('os')} ({telemetry.get('total_ram_gb')} GB RAM)  ", style="dim")
    header_text.append(f"• Ollama Status: {'Online' if telemetry.get('ollama_running') else 'Offline'}  ", style="green" if telemetry.get('ollama_running') else "red")
    header_text.append(f"• Total Data Points: {metrics.get('total_datapoints', 0)}  ", style="dim")
    header_text.append(f"• Timestamp: {telemetry.get('timestamp')}", style="dim")

    console.print()
    console.print(Panel(header_text, border_style="cyan", box=box.ROUNDED))

    # Leaderboard Table
    lb_table = Table(
        title="🏆 MODEL PERFORMANCE LEADERBOARD & COMPOSITE RANKINGS",
        box=box.ROUNDED,
        header_style="bold magenta",
        title_style="bold yellow",
    )
    lb_table.add_column("Rank", justify="center", style="bold")
    lb_table.add_column("Model", style="bold white")
    lb_table.add_column("Score", justify="center", style="bold green")
    lb_table.add_column("Speed", justify="right")
    lb_table.add_column("P95 Latency", justify="right")
    lb_table.add_column("RAM Usage", justify="right")
    lb_table.add_column("JSON Validity", justify="center")
    lb_table.add_column("Accolades", style="italic cyan")

    for item in leaderboard:
        rank_badge = "🥇 1" if item["rank"] == 1 else ("🥈 2" if item["rank"] == 2 else ("🥉 3" if item["rank"] == 3 else f"#{item['rank']}"))
        score_color = "bright_green" if item["composite_score"] >= 80 else ("yellow" if item["composite_score"] >= 50 else "red")
        score_str = f"[{score_color}]{item['composite_score']} / 100[/{score_color}]"

        validity_color = "green" if item["schema_validity_pct"] == 100.0 else "yellow"
        validity_str = f"[{validity_color}]{item['schema_validity_pct']}%[/{validity_color}]"

        badges_str = " | ".join(item.get("badges", [])) or "Standard"

        lb_table.add_row(
            rank_badge,
            item["model"],
            score_str,
            f"{item['avg_tokens_per_sec']} tps",
            f"{item['p95_latency']}s",
            f"{item['avg_memory_mb']} MB",
            validity_str,
            badges_str,
        )

    console.print(lb_table)

    # Detailed Latency & Throughput Distribution Table
    lat_table = Table(
        title="⏱️ INFERENCE LATENCY & THROUGHPUT DISTRIBUTION",
        box=box.SIMPLE_HEAD,
        header_style="bold blue",
        title_style="bold blue",
        expand=True,
    )
    lat_table.add_column("Model", style="bold", no_wrap=True)
    lat_table.add_column("Min Latency", justify="right")
    lat_table.add_column("Median (P50)", justify="right")
    lat_table.add_column("P95 Latency", justify="right")
    lat_table.add_column("Max Latency", justify="right")
    lat_table.add_column("Prompt Eval Speed", justify="right")
    lat_table.add_column("Memory Efficiency", justify="right", style="bold green")

    for item in leaderboard:
        lat_table.add_row(
            item["model"],
            f"{item['min_latency']}s",
            f"{item['p50_latency']}s",
            f"{item['p95_latency']}s",
            f"{item['max_latency']}s",
            f"{item['avg_prompt_tokens_per_sec']} tok/s",
            f"{item['tokens_per_gb_ram']} tok/s/GB",
        )

    console.print(lat_table)

    # Temperature Variance Table (if data exists)
    if temp_stability:
        temp_table = Table(
            title="🌡️ TEMPERATURE SENSITIVITY & OUTPUT STABILITY",
            box=box.SIMPLE_HEAD,
            header_style="bold red",
            title_style="bold red",
            expand=True,
        )
        temp_table.add_column("Model", style="bold", no_wrap=True)
        temp_table.add_column("Temp", justify="center")
        temp_table.add_column("Runs", justify="center")
        temp_table.add_column("Mean Tokens", justify="right")
        temp_table.add_column("Std Dev (Token Variance)", justify="right")
        temp_table.add_column("Observed Behavior", style="italic")

        for row in temp_stability:
            temp_table.add_row(
                row["model"],
                str(row["temperature"]),
                str(row["runs_recorded"]),
                f"{row['mean_tokens']} tok",
                f"±{row['token_std_dev']}",
                row["behavior"],
            )

        console.print(temp_table)

    # Hardware Deployment Feasibility Table
    hw_table = Table(
        title="🖥️ HARDWARE & EDGE DEPLOYMENT FEASIBILITY",
        box=box.ROUNDED,
        header_style="bold purple",
        title_style="bold purple",
        expand=True,
    )
    hw_table.add_column("Model", style="bold")
    hw_table.add_column("RAM Footprint", justify="right")
    hw_table.add_column("Recommended Minimum Hardware", style="bold white")
    hw_table.add_column("Host Headroom Assessment", style="dim")

    for item in leaderboard:
        hw_table.add_row(
            item["model"],
            f"{item['avg_memory_mb']} MB",
            item["deploy_tier"],
            item["headroom"],
        )

    console.print(hw_table)

    # Executive Recommendation Panel
    rec_panel = Panel(
        Text(recommendation, style="bold white"),
        title="💡 EXECUTIVE VERDICT & DEPLOYMENT RECOMMENDATION",
        title_align="left",
        border_style="green",
        box=box.ROUNDED,
    )
    console.print(rec_panel)

    # Generated Report Info
    if report_path:
        console.print(
            f"[bold green]✔ Full diagnostic report exported to:[/bold green] [underline cyan]{report_path}[/underline cyan]\n"
        )


def run_analysis(
    results_csv: str = RESULTS_CSV,
    temp_results_csv: str = TEMPERATURE_RESULTS_CSV,
    generate_report: bool = True,
) -> None:
    """Execute analysis, render Rich dashboard, and export evaluation report."""
    metrics = compute_comprehensive_metrics(
        results_csv=results_csv,
        temp_results_csv=temp_results_csv,
    )

    if "error" in metrics:
        print(f"Error: {metrics['error']}")
        return

    report_path = None
    if generate_report:
        report_path = generate_markdown_report(metrics)

    display_rich_dashboard(metrics, report_path=report_path)


def main():
    run_analysis()


if __name__ == "__main__":
    main()
