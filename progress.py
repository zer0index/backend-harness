"""
Progress Tracking Utilities
===========================

Functions for tracking and displaying progress of the autonomous coding agent.
"""

import json
from pathlib import Path


def count_passing_tests(project_dir: Path) -> tuple[int, int]:
    """
    Count passing and total tests in feature_list.json.

    Args:
        project_dir: Directory containing feature_list.json

    Returns:
        (passing_count, total_count)
    """
    tests_file = project_dir / "feature_list.json"

    if not tests_file.exists():
        return 0, 0

    try:
        with open(tests_file, "r", encoding='utf-8') as f:
            tests = json.load(f)

        total = len(tests)
        passing = sum(1 for test in tests if test.get("passes", False))

        return passing, total
    except (json.JSONDecodeError, IOError):
        return 0, 0


def print_session_header(session_num: int, is_initializer: bool) -> None:
    """Print a formatted header for the session."""
    from console_output import console
    from rich.text import Text
    from rich import box
    from rich.panel import Panel
    
    session_type = "INITIALIZER" if is_initializer else "CODING AGENT"
    
    header = Text()
    header.append(f"🤖 SESSION {session_num}: ", style="bold cyan")
    header.append(session_type, style="bold yellow")
    
    console.print()
    console.print(Panel(header, border_style="cyan", box=box.DOUBLE))
    console.print()


def print_progress_summary(project_dir: Path) -> None:
    """Print a summary of current progress."""
    from console_output import console
    from rich.progress import Progress, BarColumn, TextColumn
    from rich.text import Text
    
    passing, total = count_passing_tests(project_dir)

    if total > 0:
        percentage = (passing / total) * 100
        
        # Create a visual progress bar
        progress_text = Text()
        progress_text.append(f"Progress: ", style="bold")
        progress_text.append(f"{passing}/{total}", style="cyan")
        progress_text.append(f" tests passing (", style="dim")
        progress_text.append(f"{percentage:.1f}%", style="green" if percentage == 100 else "yellow")
        progress_text.append(")", style="dim")
        
        console.print()
        console.print(progress_text)
        
        # Visual bar
        bar_length = 50
        filled = int(bar_length * passing / total)
        bar = "█" * filled + "░" * (bar_length - filled)
        console.print(f"[green]{bar}[/]")
    else:
        console.print("\n[dim]Progress: feature_list.json not yet created[/]")
