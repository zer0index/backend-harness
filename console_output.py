"""
Enhanced Console Output for Autonomous Agent
============================================

Beautiful, animated console output using Rich library.
"""

from datetime import datetime
from typing import Optional, Dict, List, Any
from contextlib import contextmanager
import time

from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TaskID,
)
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich import box
from rich.style import Style


# Console instance
console = Console()


class AgentConsole:
    """Enhanced console output manager for the autonomous agent."""

    def __init__(self):
        self.start_time = datetime.now()
        self.iteration_count = 0
        self.total_tokens = 0
        self.files_created = 0
        self.files_modified = 0
        self.tools_called = 0
        self.tool_stats: Dict[str, Dict[str, int]] = {}
        self.current_phase = "Initializing"
        
    def print_banner(self, model: str, project_dir: str, config: str):
        """Print animated startup banner."""
        banner_text = Text()
        banner_text.append("🤖 ", style="bold cyan")
        banner_text.append("Autonomous Coding Agent\n\n", style="bold magenta")
        banner_text.append(f"Model: ", style="dim")
        banner_text.append(f"{model}\n", style="cyan")
        banner_text.append(f"Project: ", style="dim")
        banner_text.append(f"{project_dir}\n", style="green")
        banner_text.append(f"Config: ", style="dim")
        banner_text.append(f"{config}\n", style="yellow")
        banner_text.append(f"Started: ", style="dim")
        banner_text.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="blue")

        panel = Panel(
            Align.center(banner_text),
            box=box.DOUBLE,
            border_style="bright_magenta",
            padding=(1, 2),
        )
        
        console.print()
        console.print(panel)
        console.print()

    @contextmanager
    def phase(self, name: str):
        """Context manager for phases with spinner animation."""
        self.current_phase = name
        
        with Progress(
            SpinnerColumn(spinner_name="dots"),
            TextColumn("[bold blue]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"[bold cyan]Phase:[/] {name}", total=None)
            start = time.time()
            
            try:
                yield progress
                duration = time.time() - start
                progress.update(task, description=f"[bold cyan]Phase:[/] {name} ✓")
                console.print(f"[dim]  Completed in {duration:.1f}s[/]\n")
            except Exception as e:
                progress.update(task, description=f"[bold cyan]Phase:[/] {name} ✗")
                console.print(f"[red]  Failed: {e}[/]\n")
                raise

    def print_phase_step(self, message: str, status: str = "success"):
        """Print a step within a phase."""
        icons = {
            "success": "✓",
            "info": "ℹ",
            "warning": "⚠",
            "error": "✗",
            "running": "⚙",
        }
        colors = {
            "success": "green",
            "info": "blue",
            "warning": "yellow",
            "error": "red",
            "running": "cyan",
        }
        
        icon = icons.get(status, "•")
        color = colors.get(status, "white")
        console.print(f"[{color}]{icon}[/] {message}")

    def start_iteration(self, iteration: int, max_iterations: Optional[int] = None):
        """Start a new iteration with animated header."""
        self.iteration_count = iteration
        
        iter_text = f"{iteration}" if max_iterations is None else f"{iteration}/{max_iterations}"
        
        header = Text()
        header.append("╭─ ", style="bright_cyan")
        header.append("Iteration ", style="bold white")
        header.append(iter_text, style="bold yellow")
        header.append(" ─" + "─" * 50, style="bright_cyan")
        
        console.print()
        console.print(header)

    def create_live_dashboard(self, iteration: int, max_iterations: Optional[int] = None) -> Live:
        """Create a live updating dashboard for the current iteration."""
        layout = Layout()
        
        def make_dashboard() -> Panel:
            # Status table
            status_table = Table(show_header=False, box=None, padding=(0, 1))
            status_table.add_column(style="dim")
            status_table.add_column(style="bold")
            
            iter_text = f"{iteration}" if max_iterations is None else f"{iteration}/{max_iterations}"
            elapsed = (datetime.now() - self.start_time).total_seconds()
            elapsed_str = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}"
            
            status_table.add_row("Status:", "[cyan]🔄 Active[/]")
            status_table.add_row("Elapsed:", f"[yellow]{elapsed_str}[/]")
            status_table.add_row("Iteration:", f"[magenta]{iter_text}[/]")
            status_table.add_row("Tokens:", f"[green]{self.total_tokens:,}[/]")
            status_table.add_row("Tools Called:", f"[blue]{self.tools_called}[/]")
            
            return Panel(
                status_table,
                title="[bold cyan]Agent Dashboard[/]",
                border_style="cyan",
                box=box.ROUNDED,
            )
        
        return Live(make_dashboard(), console=console, refresh_per_second=4)

    def update_tool_call(self, tool_name: str, status: str = "running"):
        """Update tool call status."""
        icons = {
            "running": "🔄",
            "success": "✓",
            "error": "✗",
        }
        colors = {
            "running": "cyan",
            "success": "green",
            "error": "red",
        }
        
        icon = icons.get(status, "•")
        color = colors.get(status, "white")
        
        console.print(f"  [{color}]{icon}[/] [dim]{tool_name}[/]")
        
        # Update stats
        if tool_name not in self.tool_stats:
            self.tool_stats[tool_name] = {"count": 0, "success": 0, "error": 0}
        
        self.tool_stats[tool_name]["count"] += 1
        if status == "success":
            self.tool_stats[tool_name]["success"] += 1
        elif status == "error":
            self.tool_stats[tool_name]["error"] += 1
        
        self.tools_called += 1

    def print_iteration_summary(
        self,
        duration: float,
        tokens_used: int,
        files_modified: List[str],
        tool_calls: int,
    ):
        """Print beautiful summary after each iteration."""
        # Update totals
        self.total_tokens += tokens_used
        
        # Create summary table
        summary = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        summary.add_column(style="dim", justify="right")
        summary.add_column(style="bold")
        
        summary.add_row("Duration:", f"[yellow]{duration:.1f}s[/]")
        summary.add_row("Tokens Used:", f"[green]{tokens_used:,}[/]")
        summary.add_row("Tools Called:", f"[blue]{tool_calls}[/]")
        summary.add_row("Files Modified:", f"[magenta]{len(files_modified)}[/]")
        
        # Tool breakdown if we have stats
        tool_table = None
        if self.tool_stats:
            tool_table = Table(show_header=True, box=box.SIMPLE_HEAD, padding=(0, 1))
            tool_table.add_column("Tool", style="cyan")
            tool_table.add_column("Count", justify="right", style="yellow")
            tool_table.add_column("Success Rate", justify="right", style="green")
            
            for tool, stats in sorted(self.tool_stats.items()):
                success_rate = (
                    (stats["success"] / stats["count"] * 100) if stats["count"] > 0 else 0
                )
                tool_table.add_row(
                    tool,
                    str(stats["count"]),
                    f"{success_rate:.0f}%",
                )
        
        # Files list
        files_text = None
        if files_modified:
            files_text = Text()
            for i, file in enumerate(files_modified[:5], 1):
                files_text.append(f"  {i}. ", style="dim")
                files_text.append(f"{file}\n", style="cyan")
            if len(files_modified) > 5:
                files_text.append(f"  ... and {len(files_modified) - 5} more", style="dim")
        
        # Combine everything
        content_parts = [
            summary,
            Text(),
            Text("Tool Breakdown:", style="bold dim"),
            tool_table if self.tool_stats else Text("  No tools called yet", style="dim"),
            Text(),
            Text("Files Modified:", style="bold dim"),
            files_text if files_modified else Text("  No files modified", style="dim"),
        ]
        
        content = Group(*content_parts)
        
        panel = Panel(
            content,
            title=f"[bold]Iteration {self.iteration_count} Summary[/]",
            border_style="green",
            box=box.ROUNDED,
        )
        
        console.print(panel)
        console.print()

    def print_warning(self, title: str, message: str, details: Optional[str] = None):
        """Print warning panel."""
        content = Text(message, style="yellow")
        if details:
            content.append("\n\n")
            content.append(details, style="dim")
        
        panel = Panel(
            content,
            title=f"[bold yellow]⚠️  {title}[/]",
            border_style="yellow",
            box=box.ROUNDED,
        )
        console.print(panel)
        console.print()

    def print_error(self, title: str, message: str, details: Optional[str] = None):
        """Print error panel."""
        content = Text(message, style="red")
        if details:
            content.append("\n\n")
            content.append("Details:", style="bold dim")
            content.append(f"\n{details}", style="dim")
        
        panel = Panel(
            content,
            title=f"[bold red]❌ {title}[/]",
            border_style="red",
            box=box.DOUBLE,
        )
        console.print(panel)
        console.print()

    def print_thinking(self, text: str):
        """Print agent's thinking with special formatting."""
        thinking_panel = Panel(
            Text(text, style="italic magenta"),
            title="[bold magenta]💭 Agent Thinking[/]",
            border_style="magenta",
            box=box.ROUNDED,
        )
        console.print(thinking_panel)

    def print_final_summary(
        self,
        total_duration: float,
        iterations: int,
        total_tokens: int,
        cost_estimate: float,
        files_created: int,
        files_modified: int,
        git_commits: int,
        test_results: Optional[Dict[str, Any]] = None,
    ):
        """Print beautiful final summary."""
        minutes = int(total_duration // 60)
        seconds = int(total_duration % 60)
        duration_str = f"{minutes}m {seconds}s"
        
        # Main stats
        stats = Table(show_header=False, box=None, padding=(0, 2))
        stats.add_column(style="dim", justify="right")
        stats.add_column(style="bold")
        
        stats.add_row("Total Duration:", f"[yellow]{duration_str}[/]")
        stats.add_row("Iterations:", f"[cyan]{iterations}[/]")
        stats.add_row("Total Tokens:", f"[green]{total_tokens:,}[/]")
        stats.add_row("Estimated Cost:", f"[blue]${cost_estimate:.2f}[/]")
        stats.add_row("", "")
        stats.add_row("Files Created:", f"[magenta]{files_created}[/]")
        stats.add_row("Files Modified:", f"[magenta]{files_modified}[/]")
        stats.add_row("Git Commits:", f"[cyan]{git_commits}[/]")
        
        # Test results if available
        if test_results:
            stats.add_row("", "")
            total = test_results.get("total", 0)
            passed = test_results.get("passed", 0)
            pass_rate = (passed / total * 100) if total > 0 else 0
            stats.add_row("Tests Generated:", f"[green]{total}[/]")
            stats.add_row("Test Pass Rate:", f"[green]{pass_rate:.1f}%[/] ({passed}/{total})")
        
        content = Group(
            Text("🎉 Agent Execution Complete", style="bold green", justify="center"),
            Text(),
            stats,
        )
        
        panel = Panel(
            content,
            border_style="bright_green",
            box=box.DOUBLE,
            padding=(1, 2),
        )
        
        console.print()
        console.print(panel)
        console.print()

    def print_keyboard_interrupt(self):
        """Print message for keyboard interrupt."""
        console.print()
        console.print(
            Panel(
                Text("⏸️  Execution paused by user\n\nTo resume, run the same command again.", justify="center"),
                border_style="yellow",
                box=box.ROUNDED,
            )
        )
        console.print()


# Global instance
agent_console = AgentConsole()


# Convenience functions for backward compatibility
def print_banner(model: str, project_dir: str, config: str):
    """Print startup banner."""
    agent_console.print_banner(model, project_dir, config)


def print_phase_start(name: str):
    """Start a phase."""
    return agent_console.phase(name)


def print_step(message: str, status: str = "success"):
    """Print a phase step."""
    agent_console.print_phase_step(message, status)
