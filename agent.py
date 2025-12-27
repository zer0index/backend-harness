"""
Agent Session Logic
===================

Core agent interaction functions for running autonomous coding sessions.
"""

import asyncio
from pathlib import Path
from typing import Optional

from claude_code_sdk import ClaudeSDKClient
from rich import box
from rich.panel import Panel
from rich.text import Text

from client import create_client
from console_output import agent_console, console
from progress import print_session_header, print_progress_summary
from prompts import get_initializer_prompt, get_coding_prompt, copy_spec_to_project, copy_templates_to_project
from logger import SessionLogger

# Import git_commit function (will be available after autonomous_agent_demo loads)
# We use a late import to avoid circular dependency
def _git_commit(project_dir, message):
    """Wrapper for git_commit to handle import."""
    try:
        from autonomous_agent_demo import git_commit
        return git_commit(project_dir, message)
    except ImportError:
        return False


# Configuration
AUTO_CONTINUE_DELAY_SECONDS = 3


async def run_agent_session(
    client: ClaudeSDKClient,
    message: str,
    project_dir: Path,
    session_logger: Optional[SessionLogger] = None,
) -> tuple[str, str]:
    """
    Run a single agent session using Claude Agent SDK.

    Args:
        client: Claude SDK client
        message: The prompt to send
        project_dir: Project directory path
        session_logger: Optional session logger for detailed logging

    Returns:
        (status, response_text) where status is:
        - "continue" if agent should continue working
        - "error" if an error occurred
    """
    # Dashboard will show activity - no need for extra messages

    try:
        # Send the query
        await client.query(message)

        # Collect response text and show tool use
        response_text = ""
        current_tool_name = None
        last_was_text = False
        
        async for msg in client.receive_response():
            msg_type = type(msg).__name__
            
            # Try to extract usage from message if available
            if hasattr(msg, 'usage') and msg.usage:
                usage = msg.usage

                # Usage can be either an object with attributes or a dict
                input_tokens = 0
                output_tokens = 0

                try:
                    if isinstance(usage, dict):
                        # Dict format (common with Azure Foundry)
                        input_tokens = usage.get('input_tokens', 0) or usage.get('prompt_tokens', 0) or 0
                        output_tokens = usage.get('output_tokens', 0) or usage.get('completion_tokens', 0) or 0
                    else:
                        # Object format (direct Anthropic API)
                        input_tokens = getattr(usage, 'input_tokens', 0) or 0
                        output_tokens = getattr(usage, 'output_tokens', 0) or 0

                    # Also check for cache-related fields that Azure Foundry might use
                    if isinstance(usage, dict):
                        cache_creation = usage.get('cache_creation_input_tokens', 0) or 0
                        cache_read = usage.get('cache_read_input_tokens', 0) or 0
                        if cache_creation > 0 or cache_read > 0:
                            input_tokens += cache_creation + cache_read

                    if input_tokens > 0 or output_tokens > 0:
                        agent_console.add_tokens(input_tokens, output_tokens)

                        # Log token usage
                        if session_logger:
                            session_logger.log_token_usage(input_tokens, output_tokens)

                        # Debug: show token tracking is working
                        if agent_console.verbosity == "verbose":
                            console.print(f"[dim]📊 Tokens: +{input_tokens}↑ +{output_tokens}↓[/]")
                except Exception as e:
                    # If token extraction fails, log in verbose mode but don't crash
                    if agent_console.verbosity == "verbose":
                        console.print(f"[dim yellow]⚠️  Failed to extract tokens: {e}[/]")

            # Handle AssistantMessage (text and tool use)
            if msg_type == "AssistantMessage" and hasattr(msg, "content"):
                for block in msg.content:
                    block_type = type(block).__name__

                    if block_type == "TextBlock" and hasattr(block, "text"):
                        response_text += block.text

                        # Agent is thinking - capture and display appropriately
                        text = block.text.strip()

                        # Log agent message
                        if session_logger and text:
                            session_logger.log_agent_message(text)

                        if text and agent_console.verbosity != "quiet":
                            # End tool batch when agent starts thinking
                            if agent_console.current_batch and agent_console.current_batch.tools:
                                agent_console.end_tool_batch()

                            # Show thinking in normal/verbose mode
                            if len(text) > 100:
                                # Long thoughts - show first sentence only in normal mode
                                if agent_console.verbosity == "normal":
                                    first_sentence = text.split('.')[0] + '...'
                                    agent_console.add_agent_thought(first_sentence[:150])
                                else:
                                    console.print(f"[magenta]{text}[/]")
                            else:
                                # Short thoughts - show in both modes
                                agent_console.add_agent_thought(text)

                        last_was_text = True
                        
                    elif block_type == "ToolUseBlock" and hasattr(block, "name"):
                        # Start a tool batch if this is the first tool after text
                        if last_was_text or not agent_console.current_batch:
                            agent_console.start_tool_batch()
                            last_was_text = False

                        current_tool_name = block.name

                        # Log tool start
                        if session_logger:
                            tool_input = {}
                            if hasattr(block, "input"):
                                # Convert to dict if it's an object
                                if isinstance(block.input, dict):
                                    tool_input = block.input
                                elif hasattr(block.input, '__dict__'):
                                    tool_input = block.input.__dict__
                                else:
                                    tool_input = {"value": str(block.input)}

                            tool_use_id = getattr(block, "id", None)
                            session_logger.log_tool_start(block.name, tool_input, tool_use_id)
                        
                        # Extract tool details for display
                        tool_details = None
                        if hasattr(block, "input") and block.input:
                            input_data = block.input
                            
                            # Convert to dict if it's an object
                            if not isinstance(input_data, dict) and hasattr(input_data, '__dict__'):
                                input_data = input_data.__dict__
                            
                            # Extract meaningful details based on tool type
                            if block.name in ["Read", "Write", "Edit", "Glob", "Grep"]:
                                # File operations - show the path
                                if isinstance(input_data, dict):
                                    if "path" in input_data:
                                        tool_details = str(input_data["path"])
                                    elif "pattern" in input_data:
                                        tool_details = str(input_data["pattern"])
                                    elif "file" in input_data:
                                        tool_details = str(input_data["file"])
                                    elif "filePath" in input_data:
                                        tool_details = str(input_data["filePath"])
                                else:
                                    # Fallback: try to extract path from string representation
                                    input_str = str(input_data)
                                    if len(input_str) > 10 and len(input_str) < 200:
                                        tool_details = input_str[:60]
                            elif block.name == "Bash":
                                # Bash commands - show the command
                                if isinstance(input_data, dict) and "command" in input_data:
                                    cmd = str(input_data["command"])
                                    # Truncate very long commands
                                    tool_details = cmd if len(cmd) <= 60 else cmd[:57] + "..."
                                else:
                                    # Fallback for command in string format
                                    input_str = str(input_data)
                                    if len(input_str) > 0:
                                        tool_details = input_str[:60] if len(input_str) <= 60 else input_str[:57] + "..."
                        
                        # In verbose mode, show tool details
                        if agent_console.verbosity == "verbose":
                            console.print(f"\n[bold cyan]🔧 Tool:[/] [yellow]{block.name}[/]")
                            if hasattr(block, "input"):
                                input_str = str(block.input)
                                if len(input_str) > 200:
                                    console.print(f"   [dim]Input: {input_str[:200]}...[/]")
                                else:
                                    console.print(f"   [dim]Input: {input_str}[/]")
                        
                        agent_console.update_tool_call(block.name, "running", details=tool_details)

            # Handle UserMessage (tool results)
            elif msg_type == "UserMessage" and hasattr(msg, "content"):
                for block in msg.content:
                    block_type = type(block).__name__

                    if block_type == "ToolResultBlock":
                        result_content = getattr(block, "content", "")
                        is_error = getattr(block, "is_error", False)

                        # Log tool result
                        if session_logger:
                            session_logger.log_tool_end(result_content, is_error)

                        # Check if command was blocked by security hook
                        if "blocked" in str(result_content).lower():
                            # Log security block
                            if session_logger and current_tool_name:
                                # Extract command and reason from result
                                result_str = str(result_content)
                                session_logger.log_security_block(
                                    current_tool_name,
                                    result_str,
                                    "Security hook blocked command"
                                )

                            agent_console.update_tool_call(
                                current_tool_name or "unknown",
                                "error",
                                f"BLOCKED: {result_content}"
                            )
                            if agent_console.verbosity == "verbose":
                                console.print(f"   [bold red]🚫 BLOCKED[/] [dim]{result_content}[/]")
                        elif is_error:
                            # Show errors
                            error_str = str(result_content)[:500]
                            agent_console.update_tool_call(
                                current_tool_name or "unknown",
                                "error",
                                error_str
                            )
                            if agent_console.verbosity == "verbose":
                                console.print(f"   [red]✗ Error:[/] [dim]{error_str}[/]")
                        else:
                            # Tool succeeded
                            output = str(result_content).strip()
                            agent_console.update_tool_call(
                                current_tool_name or "unknown",
                                "success",
                                output if len(output) < 100 else output[:100] + "..."
                            )

                            if agent_console.verbosity == "verbose":
                                if output and len(output) > 0:
                                    if len(output) > 300:
                                        console.print(f"   [green]✓ Done:[/] [dim]{output[:300]}...[/]")
                                    else:
                                        console.print(f"   [green]✓ Done:[/] [dim]{output}[/]")
                                else:
                                    console.print("   [green]✓ Done[/]")

        # End any remaining tool batch
        if agent_console.current_batch:
            agent_console.end_tool_batch()
        
        # Token usage is tracked during message loop (each msg may have usage)
        # If we still want to check for final usage on client:
        if hasattr(client, 'usage') and client.usage:
            try:
                usage = client.usage
                input_tokens = 0
                output_tokens = 0

                if isinstance(usage, dict):
                    input_tokens = usage.get('input_tokens', 0) or usage.get('prompt_tokens', 0) or 0
                    output_tokens = usage.get('output_tokens', 0) or usage.get('completion_tokens', 0) or 0
                else:
                    input_tokens = getattr(usage, 'input_tokens', 0) or 0
                    output_tokens = getattr(usage, 'output_tokens', 0) or 0

                if input_tokens > 0 or output_tokens > 0:
                    agent_console.add_tokens(input_tokens, output_tokens)

                    # Log final token usage
                    if session_logger:
                        session_logger.log_token_usage(input_tokens, output_tokens)
            except Exception as e:
                # Token tracking is optional, don't crash if it fails
                if agent_console.verbosity == "verbose":
                    console.print(f"[dim yellow]⚠️  Failed to get final token count: {e}[/]")

        console.print()
        return "continue", response_text

    except Exception as e:
        console.print(f"[red]Error during agent session: {e}[/]")
        return "error", str(e)


async def run_autonomous_agent(
    project_dir: Path,
    model: str,
    max_iterations: Optional[int] = None,
    config_name: str = 'medium',
    git_enabled: bool = True,
    run_logger: Optional['RunLogger'] = None,
) -> None:
    """
    Run the autonomous agent loop.

    Args:
        project_dir: Directory for the project
        model: Claude model to use
        max_iterations: Maximum number of iterations (None for unlimited)
        config_name: Configuration size (small, medium, large)
        git_enabled: Whether to commit changes after each iteration
        run_logger: Optional run logger for detailed logging
    """
    # Info panel
    info = Text()
    info.append("Project directory: ", style="dim")
    info.append(f"{project_dir}\n", style="cyan")
    info.append("Model: ", style="dim")
    info.append(f"{model}\n", style="green")
    info.append("Max iterations: ", style="dim")
    if max_iterations:
        info.append(f"{max_iterations}", style="yellow")
    else:
        info.append("Unlimited", style="yellow")
    
    console.print(Panel(info, title="[bold]Configuration[/]", border_style="blue", box=box.ROUNDED))
    console.print()

    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=True)

    # Check if this is a fresh start or continuation
    tests_file = project_dir / "feature_list.json"
    is_first_run = not tests_file.exists()

    if is_first_run:
        console.print("[bold green]Fresh start[/] - will use initializer agent\n")
        
        note = Text()
        note.append("⏱️  First session takes 10-20+ minutes!\n", style="bold yellow")
        note.append("\nThe agent is generating detailed test cases.\n", style="dim")
        note.append("This may appear to hang - it's working.\n", style="dim")
        note.append("Watch for ", style="dim")
        note.append("🔧 Tool", style="cyan")
        note.append(" output.", style="dim")
        
        console.print(Panel(note, title="[bold yellow]⚠️  Important[/]", border_style="yellow", box=box.ROUNDED))
        console.print()
        # Copy the app spec into the project directory for the agent to read
        copy_spec_to_project(project_dir, config_name)
        # Copy template files so the agent can use them
        copy_templates_to_project(project_dir)
    else:
        console.print("[bold blue]Continuing existing project[/]\n")
        print_progress_summary(project_dir)

    # Main loop
    iteration = 0

    while True:
        iteration += 1

        # Check max iterations
        if max_iterations and iteration > max_iterations:
            console.print()
            console.print(Panel(
                Text(f"Reached max iterations ({max_iterations})\n\nTo continue, run the script again without --max-iterations", justify="center"),
                title="[bold yellow]⏸️  Paused[/]",
                border_style="yellow",
                box=box.ROUNDED
            ))
            break

        # Print session header
        print_session_header(iteration, is_first_run)

        # Create client (fresh context)
        client = create_client(project_dir, model)

        # Choose prompt based on session type
        if is_first_run:
            prompt = get_initializer_prompt(config_name)
            is_first_run = False  # Only use initializer once
        else:
            prompt = get_coding_prompt(config_name)

        # Start session logger
        session_logger = None
        if run_logger:
            session_logger = run_logger.start_session(iteration)

        # Run session with async context manager and live dashboard
        async with client:
            with agent_console.live_session(iteration, max_iterations, project_dir):
                status, response = await run_agent_session(client, prompt, project_dir, session_logger)

        # Handle status
        if status == "continue":
            # Check if project is complete (all tests passing)
            from progress import count_passing_tests

            passing, total = count_passing_tests(project_dir)

            # Log progress
            if session_logger:
                session_logger.log_progress(passing, total)

            # End session logger
            if run_logger:
                run_logger.end_session()

            # Commit changes after each iteration
            if git_enabled:
                _git_commit(project_dir, f"Iteration {iteration}: agent progress")

            # If all tests pass, auto-stop
            if total > 0 and passing == total:
                success_text = Text()
                success_text.append("🎉 PROJECT COMPLETE\n\n", style="bold green")
                success_text.append(f"✅ All {total} features implemented\n", style="green")
                success_text.append(f"✅ All tests passing ({passing}/{total})\n\n", style="green")
                success_text.append("Project is production-ready!", style="bold cyan")
                
                console.print()
                console.print(Panel(success_text, border_style="bright_green", box=box.DOUBLE))
                print_progress_summary(project_dir)
                
                # Final commit
                if git_enabled:
                    _git_commit(project_dir, f"Project complete: all {total} tests passing")
                
                # Instructions
                instructions = Text()
                instructions.append("To continue working on this project:\n\n", style="bold cyan")
                instructions.append(f"  cd {project_dir.resolve()}\n", style="yellow")
                instructions.append("  ./init.sh\n\n", style="green")
                instructions.append("Or run the harness again to add more features", style="dim")
                
                console.print()
                console.print(Panel(instructions, border_style="cyan", box=box.ROUNDED))
                break  # Exit the while loop

            # Otherwise, continue to next session
            console.print(f"\n[dim]Agent will auto-continue in {AUTO_CONTINUE_DELAY_SECONDS}s...[/]")
            print_progress_summary(project_dir)
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)

        elif status == "error":
            # Log progress even on error
            from progress import count_passing_tests
            passing, total = count_passing_tests(project_dir)
            if session_logger:
                session_logger.log_progress(passing, total)

            # End session logger
            if run_logger:
                run_logger.end_session()

            console.print("\n[yellow]Session encountered an error[/]")
            console.print("[dim]Will retry with a fresh session...[/]")
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)

        # Small delay between sessions
        if max_iterations is None or iteration < max_iterations:
            console.print("\n[dim]Preparing next session...[/]\n")
            await asyncio.sleep(1)

    # Final summary
    summary = Text()
    summary.append("🏁 SESSION COMPLETE\n\n", style="bold green")
    summary.append("Project directory: ", style="dim")
    summary.append(f"{project_dir}\n\n", style="cyan")
    
    console.print()
    console.print(Panel(summary, border_style="green", box=box.ROUNDED))
    print_progress_summary(project_dir)

    # Print instructions for running the generated application
    instructions = Text()
    instructions.append("🚀 TO RUN THE GENERATED APPLICATION:\n\n", style="bold cyan")
    instructions.append(f"  cd {project_dir.resolve()}\n", style="yellow")
    instructions.append("  ./init.sh", style="green")
    instructions.append("           # Run the setup script\n", style="dim")
    instructions.append("  # Or manually:\n", style="dim")
    instructions.append("  npm install && npm run dev\n\n", style="green")
    instructions.append("  Then open ", style="dim")
    instructions.append("http://localhost:3000", style="blue underline")
    instructions.append(" (or check init.sh for the URL)", style="dim")
    
    console.print()
    console.print(Panel(instructions, border_style="cyan", box=box.ROUNDED))
    console.print("\n[bold green]Done![/]\n")
