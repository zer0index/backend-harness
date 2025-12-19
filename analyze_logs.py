#!/usr/bin/env python3
"""
Log Analysis Tool for Autonomous Agent
=======================================

Analyzes session logs to identify issues, patterns, and performance bottlenecks.
Helps debug long-running sessions and understand agent behavior.

Usage:
    # Analyze specific session
    python analyze_logs.py project_dir/logs/run_20231219_103045/session_001.json

    # Analyze entire run
    python analyze_logs.py project_dir/logs/run_20231219_103045

    # Compare sessions
    python analyze_logs.py project_dir/logs/run_20231219_103045 --compare

    # Show detailed timeline
    python analyze_logs.py project_dir/logs/run_20231219_103045/session_001.json --timeline
"""

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


def load_session(session_file: Path) -> dict:
    """Load a session JSON file."""
    with open(session_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_run_summary(run_dir: Path) -> dict:
    """Load run summary JSON file."""
    summary_file = run_dir / "run_summary.json"
    if summary_file.exists():
        with open(summary_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def analyze_session(session_data: dict) -> dict:
    """
    Analyze a single session and return insights.

    Returns:
        Dictionary with analysis results
    """
    analysis = {
        "session_number": session_data.get("session_number", "unknown"),
        "duration_minutes": session_data.get("duration_minutes", 0),
        "total_tool_calls": len(session_data.get("tool_calls", [])),
        "total_errors": len(session_data.get("errors", [])),
        "total_security_blocks": len(session_data.get("security_blocks", [])),
        "token_usage": session_data.get("token_usage", {}),
        "slowest_tools": [],
        "most_used_tools": {},
        "repeated_operations": [],
        "long_gaps": [],
        "stuck_indicators": []
    }

    tool_calls = session_data.get("tool_calls", [])

    if not tool_calls:
        return analysis

    # Find slowest tool calls
    sorted_tools = sorted(
        tool_calls,
        key=lambda t: t.get("duration_seconds", 0) or 0,
        reverse=True
    )
    analysis["slowest_tools"] = [
        {
            "tool_name": t["tool_name"],
            "duration_seconds": t.get("duration_seconds", 0),
            "duration_minutes": (t.get("duration_seconds", 0) or 0) / 60,
            "input": str(t.get("input", {}))[:100],
        }
        for t in sorted_tools[:10]  # Top 10
    ]

    # Count tool usage
    tool_counter = Counter(t["tool_name"] for t in tool_calls)
    analysis["most_used_tools"] = dict(tool_counter.most_common(10))

    # Find repeated operations (same file edited many times)
    file_operations = defaultdict(list)
    for t in tool_calls:
        if t["tool_name"] in ["Edit", "Write", "Read"]:
            input_data = t.get("input", {})
            if isinstance(input_data, dict):
                file_path = input_data.get("file_path") or input_data.get("path") or input_data.get("filePath")
                if file_path:
                    file_operations[file_path].append(t)

    # Find files with many operations
    repeated = [
        {
            "file": file,
            "operations": len(ops),
            "tools": Counter(op["tool_name"] for op in ops)
        }
        for file, ops in file_operations.items()
        if len(ops) >= 5  # 5+ operations on same file
    ]
    analysis["repeated_operations"] = sorted(repeated, key=lambda x: x["operations"], reverse=True)

    # Detect long gaps between tool calls (possible stuck)
    for i in range(1, len(tool_calls)):
        prev_end = tool_calls[i-1].get("end_time")
        curr_start = tool_calls[i].get("start_time")

        if prev_end and curr_start:
            try:
                prev_dt = datetime.fromisoformat(prev_end)
                curr_dt = datetime.fromisoformat(curr_start)
                gap_seconds = (curr_dt - prev_dt).total_seconds()

                # Flag gaps > 60 seconds
                if gap_seconds > 60:
                    analysis["long_gaps"].append({
                        "after_tool": tool_calls[i-1]["tool_name"],
                        "before_tool": tool_calls[i]["tool_name"],
                        "gap_seconds": gap_seconds,
                        "gap_minutes": gap_seconds / 60
                    })
            except (ValueError, TypeError):
                pass

    # Detect stuck indicators
    # 1. Many errors on same tool
    error_tools = [err.get("tool_name") for err in session_data.get("errors", [])]
    error_counter = Counter(error_tools)
    for tool, count in error_counter.items():
        if count >= 3:
            analysis["stuck_indicators"].append(
                f"Tool '{tool}' failed {count} times"
            )

    # 2. Very long single tool call (> 30 minutes)
    for t in tool_calls:
        duration = t.get("duration_seconds", 0) or 0
        if duration > 1800:  # 30 minutes
            analysis["stuck_indicators"].append(
                f"Tool '{t['tool_name']}' took {duration/60:.1f} minutes"
            )

    # 3. Many operations on same file
    for rep in analysis["repeated_operations"]:
        if rep["operations"] > 20:
            analysis["stuck_indicators"].append(
                f"File '{Path(rep['file']).name}' modified {rep['operations']} times"
            )

    return analysis


def print_session_analysis(session_file: Path):
    """Print detailed analysis of a session."""
    console.print(f"\n[bold cyan]Analyzing Session: {session_file.name}[/]\n")

    session_data = load_session(session_file)
    analysis = analyze_session(session_data)

    # Session overview
    overview = Table(title="Session Overview", box=box.ROUNDED)
    overview.add_column("Metric", style="cyan")
    overview.add_column("Value", style="yellow")

    overview.add_row("Session Number", str(analysis["session_number"]))
    overview.add_row("Duration", f"{analysis['duration_minutes']:.1f} minutes")
    overview.add_row("Tool Calls", str(analysis["total_tool_calls"]))
    overview.add_row("Errors", str(analysis["total_errors"]))
    overview.add_row("Security Blocks", str(analysis["total_security_blocks"]))

    tokens = analysis["token_usage"]
    overview.add_row("Input Tokens", f"{tokens.get('input_tokens', 0):,}")
    overview.add_row("Output Tokens", f"{tokens.get('output_tokens', 0):,}")
    overview.add_row("Total Tokens", f"{tokens.get('total_tokens', 0):,}")

    console.print(overview)
    console.print()

    # Slowest tool calls
    if analysis["slowest_tools"]:
        console.print("[bold yellow]⏱️  Slowest Tool Calls[/]\n")
        slowest_table = Table(box=box.SIMPLE)
        slowest_table.add_column("Tool", style="cyan")
        slowest_table.add_column("Duration", style="yellow", justify="right")
        slowest_table.add_column("Input Preview", style="dim")

        for tool in analysis["slowest_tools"][:10]:
            duration = tool["duration_minutes"]
            color = "red" if duration > 5 else "yellow" if duration > 1 else "white"
            slowest_table.add_row(
                tool["tool_name"],
                f"[{color}]{duration:.1f}m[/]",
                tool["input"][:60] + "..." if len(tool["input"]) > 60 else tool["input"]
            )

        console.print(slowest_table)
        console.print()

    # Most used tools
    if analysis["most_used_tools"]:
        console.print("[bold cyan]🔧 Most Used Tools[/]\n")
        tools_table = Table(box=box.SIMPLE)
        tools_table.add_column("Tool", style="cyan")
        tools_table.add_column("Count", style="yellow", justify="right")

        for tool, count in analysis["most_used_tools"].items():
            tools_table.add_row(tool, str(count))

        console.print(tools_table)
        console.print()

    # Repeated operations
    if analysis["repeated_operations"]:
        console.print("[bold yellow]🔄 Repeated File Operations[/]\n")
        repeated_table = Table(box=box.SIMPLE)
        repeated_table.add_column("File", style="cyan")
        repeated_table.add_column("Operations", style="yellow", justify="right")
        repeated_table.add_column("Tools Used", style="dim")

        for rep in analysis["repeated_operations"][:15]:
            file_name = Path(rep["file"]).name
            tools_used = ", ".join(f"{tool}({count})" for tool, count in rep["tools"].items())
            color = "red" if rep["operations"] > 20 else "yellow" if rep["operations"] > 10 else "white"
            repeated_table.add_row(
                file_name,
                f"[{color}]{rep['operations']}[/]",
                tools_used
            )

        console.print(repeated_table)
        console.print()

    # Long gaps (possible stuck)
    if analysis["long_gaps"]:
        console.print("[bold red]⚠️  Long Gaps Between Tool Calls[/]\n")
        gaps_table = Table(box=box.SIMPLE)
        gaps_table.add_column("After Tool", style="cyan")
        gaps_table.add_column("Before Tool", style="cyan")
        gaps_table.add_column("Gap", style="red", justify="right")

        for gap in sorted(analysis["long_gaps"], key=lambda x: x["gap_seconds"], reverse=True)[:10]:
            gaps_table.add_row(
                gap["after_tool"],
                gap["before_tool"],
                f"{gap['gap_minutes']:.1f}m"
            )

        console.print(gaps_table)
        console.print()

    # Stuck indicators
    if analysis["stuck_indicators"]:
        console.print("[bold red]🚨 Potential Issues[/]\n")
        for indicator in analysis["stuck_indicators"]:
            console.print(f"  • {indicator}")
        console.print()

    # Errors
    if session_data.get("errors"):
        console.print("[bold red]❌ Errors[/]\n")
        errors_table = Table(box=box.SIMPLE)
        errors_table.add_column("Tool", style="cyan")
        errors_table.add_column("Error Preview", style="red")

        for err in session_data["errors"][:10]:
            tool = err.get("tool_name", "unknown")
            error_msg = str(err.get("error", ""))
            # Try to extract meaningful error from the result
            if isinstance(err.get("error"), dict):
                error_content = err["error"].get("content", "")
                if isinstance(error_content, str):
                    error_msg = error_content
            errors_table.add_row(tool, error_msg[:80])

        console.print(errors_table)
        console.print()

    # Progress
    progress = session_data.get("progress", {})
    if progress:
        passing = progress.get("passing_tests", 0)
        total = progress.get("total_tests", 0)
        percentage = progress.get("percentage", 0)

        progress_text = Text()
        progress_text.append("Tests: ", style="bold")
        progress_text.append(f"{passing}/{total}", style="cyan")
        progress_text.append(f" ({percentage:.1f}%)", style="green" if percentage == 100 else "yellow")

        console.print(Panel(progress_text, title="[bold]Progress", border_style="green", box=box.ROUNDED))
        console.print()


def print_run_comparison(run_dir: Path):
    """Compare all sessions in a run."""
    console.print(f"\n[bold cyan]Run Comparison: {run_dir.name}[/]\n")

    # Load all session files
    session_files = sorted(run_dir.glob("session_*.json"))

    if not session_files:
        console.print("[red]No session files found[/]")
        return

    # Load run summary if available
    summary = load_run_summary(run_dir)
    if summary:
        console.print(f"[bold]Run ID:[/] {summary.get('run_id', 'unknown')}")
        console.print(f"[bold]Model:[/] {summary.get('model', 'unknown')}")
        console.print(f"[bold]Total Duration:[/] {summary.get('duration_minutes', 0):.1f} minutes")
        console.print()

    # Create comparison table
    table = Table(title="Session Comparison", box=box.ROUNDED)
    table.add_column("Session", style="cyan", justify="center")
    table.add_column("Duration", style="yellow", justify="right")
    table.add_column("Tools", style="white", justify="right")
    table.add_column("Errors", style="red", justify="right")
    table.add_column("Tokens", style="green", justify="right")
    table.add_column("Progress", style="magenta")

    for session_file in session_files:
        session_data = load_session(session_file)

        session_num = session_data.get("session_number", "?")
        duration = session_data.get("duration_minutes", 0)
        tool_calls = len(session_data.get("tool_calls", []))
        errors = len(session_data.get("errors", []))
        tokens = session_data.get("token_usage", {}).get("total_tokens", 0)

        progress = session_data.get("progress", {})
        passing = progress.get("passing_tests", 0)
        total = progress.get("total_tests", 0)
        progress_str = f"{passing}/{total}" if total > 0 else "N/A"

        # Color code duration (red if > 60 min, yellow if > 30 min)
        duration_color = "red" if duration > 60 else "yellow" if duration > 30 else "white"

        table.add_row(
            str(session_num),
            f"[{duration_color}]{duration:.1f}m[/]",
            str(tool_calls),
            str(errors) if errors > 0 else "[dim]0[/]",
            f"{tokens:,}",
            progress_str
        )

    console.print(table)
    console.print()

    # Highlight longest session
    longest_file = max(session_files, key=lambda f: load_session(f).get("duration_minutes", 0))
    longest_session = load_session(longest_file)
    longest_duration = longest_session.get("duration_minutes", 0)

    if longest_duration > 60:
        console.print(f"\n[bold yellow]⚠️  Longest session: Session {longest_session.get('session_number')} "
                     f"({longest_duration:.1f} minutes)[/]")
        console.print(f"   Analyze with: python analyze_logs.py {longest_file}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze autonomous agent session logs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze specific session
  python analyze_logs.py project/logs/run_20231219_103045/session_001.json

  # Compare all sessions in a run
  python analyze_logs.py project/logs/run_20231219_103045 --compare

  # Show timeline
  python analyze_logs.py project/logs/run_20231219_103045/session_001.json --timeline
        """
    )

    parser.add_argument(
        "path",
        type=Path,
        help="Path to session file or run directory"
    )

    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare all sessions in a run"
    )

    parser.add_argument(
        "--timeline",
        action="store_true",
        help="Show detailed event timeline"
    )

    args = parser.parse_args()

    if not args.path.exists():
        console.print(f"[red]Error: Path not found: {args.path}[/]")
        return

    # Determine if path is a file or directory
    if args.path.is_file():
        # Analyze single session
        print_session_analysis(args.path)

        # Show timeline if requested
        if args.timeline:
            session_data = load_session(args.path)
            console.print("\n[bold cyan]Event Timeline[/]\n")

            events = session_data.get("events", [])
            for event in events[:100]:  # Limit to first 100 events
                timestamp = event.get("timestamp", "unknown")
                event_type = event.get("event_type", "unknown")
                console.print(f"[dim]{timestamp}[/] [{event_type}]")

            if len(events) > 100:
                console.print(f"\n[dim]... and {len(events) - 100} more events[/]")

    elif args.path.is_dir():
        # Check if it's a run directory
        if args.compare or (args.path / "run_summary.json").exists():
            print_run_comparison(args.path)
        else:
            # Try to find session files
            session_files = list(args.path.glob("session_*.json"))
            if session_files:
                console.print(f"[yellow]Found {len(session_files)} sessions. Use --compare to compare them.[/]")
                print_run_comparison(args.path)
            else:
                console.print(f"[red]No session files found in {args.path}[/]")
    else:
        console.print(f"[red]Invalid path: {args.path}[/]")


if __name__ == "__main__":
    main()
