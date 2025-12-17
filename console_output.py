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


class ToolBatch:
    """Manages a batch of tool calls for grouped display."""
    
    def __init__(self):
        self.tools: List[Dict[str, Any]] = []
        self.start_time = time.time()
        self.completed = 0
        self.total = 0
        
    def add_tool(self, name: str, status: str = "pending", output: Optional[str] = None):
        """Add a tool to the batch."""
        self.tools.append({
            "name": name,
            "status": status,
            "output": output,
            "timestamp": time.time()
        })
        self.total += 1
        
    def mark_complete(self, success: bool = True, output: Optional[str] = None):
        """Mark the last tool as complete."""
        if self.tools:
            self.tools[-1]["status"] = "success" if success else "error"
            self.tools[-1]["output"] = output
            self.completed += 1
            
    def get_duration(self) -> float:
        """Get batch duration in seconds."""
        return time.time() - self.start_time
        
    def get_summary(self) -> str:
        """Get a summary of tool names."""
        tool_names = [t["name"] for t in self.tools]
        # Group consecutive duplicates
        grouped = []
        for name in tool_names:
            if grouped and grouped[-1].startswith(name):
                # Increment count
                if "(" in grouped[-1]:
                    count = int(grouped[-1].split("(")[1].split("x")[0]) + 1
                    grouped[-1] = f"{name} ({count}x)"
                else:
                    grouped[-1] = f"{name} (2x)"
            else:
                grouped.append(name)
        return ", ".join(grouped[:5]) + (f" ... +{len(grouped)-5} more" if len(grouped) > 5 else "")


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
        self.verbosity = "normal"  # quiet, normal, verbose
        self.current_batch: Optional[ToolBatch] = None
        self.agent_thinking: List[str] = []
        self.live_dashboard_active = False
        self.current_live_dashboard: Optional[Live] = None
        self.session_start_time = time.time()
        self.session_errors: List[str] = []
        self.session_thinking: List[str] = []
        self.session_iteration = 0
        self.session_max_iterations: Optional[int] = None
        self.project_dir: Optional[Any] = None  # Track for test progress
        self._update_dashboard = None  # Function to update live dashboard
        
        # Token tracking
        self.session_input_tokens = 0
        self.session_output_tokens = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        
    def set_verbosity(self, level: str):
        """Set verbosity level: quiet, normal, or verbose."""
        self.verbosity = level
        
    def start_tool_batch(self):
        """Start a new batch of tool calls."""
        if self.current_batch:
            self.end_tool_batch()
        self.current_batch = ToolBatch()
        
    def end_tool_batch(self):
        """End the current batch and display summary."""
        if not self.current_batch or not self.current_batch.tools:
            return
            
        batch = self.current_batch
        duration = batch.get_duration()
        
        # If live dashboard is active, don't print anything - it's in the dashboard
        if self.live_dashboard_active:
            self.current_batch = None
            return
        
        # In verbose mode, tools are already shown individually
        if self.verbosity == "verbose":
            self.current_batch = None
            return
            
        # In normal mode without dashboard, show a nice summary
        if self.verbosity == "normal":
            success_count = sum(1 for t in batch.tools if t["status"] == "success")
            error_count = sum(1 for t in batch.tools if t["status"] == "error")
            
            # Progress bar
            filled = int(40 * success_count / batch.total) if batch.total > 0 else 0
            bar = "━" * filled + ("━" if filled == 40 else "╸" + "─" * (39 - filled))
            
            summary = Text()
            summary.append("\n🔧 Running tools: ", style="cyan")
            summary.append(bar, style="green" if error_count == 0 else "yellow")
            summary.append(f" {batch.total}/{batch.total} completed\n", style="bold")
            summary.append(f"   {batch.get_summary()}", style="dim")
            
            console.print(summary)
            
            # Show errors if any
            if error_count > 0:
                console.print()
                for tool in batch.tools:
                    if tool["status"] == "error" and tool.get("output"):
                        error_msg = tool["output"]
                        if len(error_msg) > 100:
                            error_msg = error_msg[:100] + "..."
                        console.print(f"   [red]✗ {tool['name']}: {error_msg}[/]")
            
            console.print()
        
        self.current_batch = None
        
    def add_agent_thought(self, text: str):
        """Add agent thinking text."""
        self.agent_thinking.append(text)
        self.session_thinking.append(text)
        
        # Update dashboard if active
        if self.live_dashboard_active and hasattr(self, '_update_dashboard') and self._update_dashboard:
            self._update_dashboard()
        
        # In verbose mode or when no dashboard, show thinking
        if self.verbosity == "verbose" and not self.live_dashboard_active:
            # End any active tool batch before showing thinking
            if self.current_batch and self.current_batch.tools:
                self.end_tool_batch()
            
            console.print()
            console.print(f"[italic dim]💭 {text}[/]")
            console.print()
        # Otherwise it's shown in the live dashboard
    
    def add_tokens(self, input_tokens: int, output_tokens: int):
        """Track token usage."""
        self.session_input_tokens += input_tokens
        self.session_output_tokens += output_tokens
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        
        # Update dashboard if active
        if self.live_dashboard_active and hasattr(self, '_update_dashboard') and self._update_dashboard:
            self._update_dashboard()
        
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
        """Context manager for phases with animated header."""
        self.current_phase = name
        
        # Always show phases (even in quiet mode)
        # Print phase header
        header = Text()
        header.append("╭─ ", style="bright_cyan")
        header.append("Phase: ", style="bold cyan")
        header.append(name, style="bold white")
        header.append(" " + "─" * (60 - len(name)), style="bright_cyan")
        header.append("╮", style="bright_cyan")
        console.print(header)
        
        start = time.time()
        
        try:
            yield
            duration = time.time() - start
            
            # Print phase footer
            footer = Text()
            footer.append("╰─ ", style="bright_cyan")
            footer.append("✓ Completed in ", style="green")
            footer.append(f"{duration:.1f}s", style="bold yellow")
            footer.append(" " + "─" * (47 - len(f"{duration:.1f}s")), style="bright_cyan")
            footer.append("╯", style="bright_cyan")
            console.print(footer)
            console.print()
        except Exception as e:
            duration = time.time() - start
            footer = Text()
            footer.append("╰─ ", style="bright_cyan")
            footer.append("✗ Failed after ", style="red")
            footer.append(f"{duration:.1f}s", style="bold yellow")
            footer.append(" " + "─" * (45 - len(f"{duration:.1f}s")), style="bright_cyan")
            footer.append("╯", style="bright_cyan")
            console.print(footer)
            console.print(f"[red]Error: {e}[/]\n")
            raise

    def print_phase_step(self, message: str, status: str = "success"):
        """Print a step within a phase."""
        # In quiet mode, only show errors and warnings
        if self.verbosity == "quiet" and status not in ["error", "warning"]:
            return
            
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
        console.print(f"│ [{color}]{icon}[/] {message}")

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

    @contextmanager
    def live_session(self, iteration: int, max_iterations: Optional[int] = None, project_dir = None):
        """Context manager for a live updating session dashboard."""
        if self.verbosity == "quiet":
            # No live dashboard in quiet mode
            yield None
            return
            
        iter_text = f"{iteration}" if max_iterations is None else f"{iteration}/{max_iterations}"
        self.session_start_time = time.time()
        self.live_dashboard_active = True
        self.session_iteration = iteration
        self.session_max_iterations = max_iterations
        self.session_errors: List[str] = []
        self.session_thinking: List[str] = []
        self.project_dir = project_dir
        self.session_input_tokens = 0
        self.session_output_tokens = 0
        
        def make_dashboard() -> Layout:
            # Create layout with multiple sections
            layout = Layout()
            layout.split_column(
                Layout(name="breadcrumb", size=3),
                Layout(name="status", size=8),
                Layout(name="activity", size=6),
            )
            
            # Breadcrumbs with test progress - simplified, no future sessions
            
            # Build session text
            if max_iterations:
                session_text = f"[bold cyan]▶ Session {iteration}[/] [dim](max: {max_iterations})[/]"
            else:
                session_text = f"[bold cyan]▶ Session {iteration}[/]"
            
            # Get test progress if project_dir available
            test_info = ""
            if self.project_dir:
                try:
                    from progress import count_passing_tests
                    passing, total = count_passing_tests(self.project_dir)
                    if total > 0:
                        percentage = int((passing / total) * 100)
                        test_info = f"  [dim]│[/]  Tests: [cyan]{passing}[/]/[dim]{total}[/] [yellow]({percentage}%)[/]"
                except:
                    pass
            
            breadcrumb_text = session_text + test_info
            
            layout["breadcrumb"].update(Panel(
                Align.center(Text.from_markup(breadcrumb_text)),
                border_style="bright_black",
                box=box.SIMPLE
            ))
            
            # Status panel
            elapsed = time.time() - self.session_start_time
            elapsed_str = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}"
            
            status_grid = Table.grid(padding=(0, 2))
            status_grid.add_column(style="dim", justify="right")
            status_grid.add_column(style="bold")
            status_grid.add_column(style="dim", justify="right")
            status_grid.add_column(style="bold")
            
            # Calculate stats
            tools_completed = self.tools_called
            success_count = sum(stats.get("success", 0) for stats in self.tool_stats.values())
            error_count = sum(stats.get("error", 0) for stats in self.tool_stats.values())
            
            status_grid.add_row(
                "⏱ Time:", f"[yellow]{elapsed_str}[/]",
                "🔧 Tools:", f"[cyan]{tools_completed}[/]"
            )
            status_grid.add_row(
                "✓ Success:", f"[green]{success_count}[/]",
                "✗ Errors:", f"[red]{error_count}[/]" if error_count > 0 else "[dim]0[/]"
            )
            
            # Add token usage and cost
            total_tokens = self.session_input_tokens + self.session_output_tokens
            if total_tokens > 0:
                # Claude Sonnet 4.5 pricing (as of Dec 2024): $3/MTok input, $15/MTok output
                input_cost = (self.session_input_tokens / 1_000_000) * 3.0
                output_cost = (self.session_output_tokens / 1_000_000) * 15.0
                total_cost = input_cost + output_cost
                
                # Format tokens (K for thousands)
                def format_tokens(n):
                    if n >= 1000:
                        return f"{n/1000:.1f}K"
                    return str(n)
                
                status_grid.add_row(
                    "📊 Tokens:", f"[cyan]{format_tokens(total_tokens)}[/] [dim]({format_tokens(self.session_input_tokens)}↑ {format_tokens(self.session_output_tokens)}↓)[/]",
                    "💰 Cost:", f"[yellow]${total_cost:.4f}[/]"
                )
            
            # Add test progress bar if available
            if self.project_dir:
                try:
                    from progress import count_passing_tests
                    passing, total = count_passing_tests(self.project_dir)
                    if total > 0:
                        progress_pct = passing / total
                        bar_width = 40
                        filled = int(bar_width * progress_pct)
                        bar = "█" * filled + "░" * (bar_width - filled)
                        status_grid.add_row(
                            "", "",
                            "📊 Tests:", f"[green]{bar}[/] [cyan]{passing}[/]/[dim]{total}[/]"
                        )
                except:
                    pass
            
            layout["status"].update(Panel(
                status_grid,
                title="[bold]Status",
                border_style="cyan",
                box=box.ROUNDED
            ))
            
            # Activity panel
            activity_text = Text()
            
            # Show current batch status
            if self.current_batch and self.current_batch.tools:
                batch = self.current_batch
                completed = sum(1 for t in batch.tools if t["status"] != "pending")
                
                # Progress bar
                progress = completed / batch.total if batch.total > 0 else 0
                bar_width = 30
                filled = int(bar_width * progress)
                bar = "█" * filled + "░" * (bar_width - filled)
                
                activity_text.append(f"Tools: ", style="dim")
                activity_text.append(f"{bar} {completed}/{batch.total}\n", style="cyan")
                
                # Current tool
                if batch.tools:
                    last_tool = batch.tools[-1]
                    if last_tool["status"] == "pending":
                        activity_text.append("\n🔄 ", style="cyan")
                        activity_text.append(f"{last_tool['name']}...", style="bold cyan")
                    elif last_tool["status"] == "success":
                        activity_text.append("\n✓ ", style="green")
                        activity_text.append(f"{last_tool['name']}", style="dim green")
                    elif last_tool["status"] == "error":
                        activity_text.append("\n✗ ", style="red")
                        activity_text.append(f"{last_tool['name']}", style="dim red")
            else:
                # Show last thinking
                if self.session_thinking:
                    last_thought = self.session_thinking[-1]
                    if len(last_thought) > 60:
                        last_thought = last_thought[:57] + "..."
                    activity_text.append("💭 ", style="magenta")
                    activity_text.append(last_thought, style="italic dim")
                else:
                    activity_text.append("⏳ Processing...", style="dim")
            
            layout["activity"].update(Panel(
                activity_text,
                title="[bold]Current Activity",
                border_style="blue",
                box=box.ROUNDED
            ))
            
            return layout
        
        # Always show live dashboard (except in quiet mode)
        with Live(make_dashboard(), console=console, refresh_per_second=4, transient=False) as live:
            self.current_live_dashboard = live
            
            # Store the make_dashboard function so we can update it
            def update_dashboard():
                if self.current_live_dashboard:
                    self.current_live_dashboard.update(make_dashboard())
            
            self._update_dashboard = update_dashboard
            
            try:
                yield live
            finally:
                self.current_live_dashboard = None
                self.live_dashboard_active = False
                self._update_dashboard = None
                
                # Show errors if any
                if self.session_errors:
                    console.print()
                    error_panel = Panel(
                        "\n".join(f"[red]✗[/] {err}" for err in self.session_errors[-3:]),
                        title=f"[bold red]⚠ Errors ({len(self.session_errors)})[/]",
                        border_style="red",
                        box=box.ROUNDED
                    )
                    console.print(error_panel)

    def update_tool_call(self, tool_name: str, status: str = "running", output: Optional[str] = None):
        """Update tool call status."""
        # Update stats
        if tool_name not in self.tool_stats:
            self.tool_stats[tool_name] = {"count": 0, "success": 0, "error": 0}
        
        self.tool_stats[tool_name]["count"] += 1
        if status == "success":
            self.tool_stats[tool_name]["success"] += 1
        elif status == "error":
            self.tool_stats[tool_name]["error"] += 1
            # Track errors for display
            if output:
                self.session_errors.append(f"{tool_name}: {output[:100]}")
        
        self.tools_called += 1
        
        # Add to current batch
        if self.current_batch:
            if status == "running":
                self.current_batch.add_tool(tool_name, "pending")
            else:
                self.current_batch.mark_complete(status == "success", output)
        
        # Update dashboard if active
        if self.live_dashboard_active and hasattr(self, '_update_dashboard') and self._update_dashboard:
            self._update_dashboard()
        
        # Only show individual tools in verbose mode when no dashboard
        if self.verbosity == "verbose" and not self.live_dashboard_active:
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
            
            # Show output for errors or if explicitly provided and short
            if output:
                if status == "error":
                    console.print(f"     [red]{output[:200]}{'...' if len(output) > 200 else ''}[/]")
                elif len(output) < 100:
                    console.print(f"     [dim]{output}[/]")
        # Otherwise, the dashboard shows current progress

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
