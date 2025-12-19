#!/usr/bin/env python3
"""
Autonomous Coding Agent Demo
============================

A minimal harness demonstrating long-running autonomous coding with Claude.
This script implements the two-agent pattern (initializer + coding agent) and
incorporates all the strategies from the long-running agents guide.

Example Usage:
    python autonomous_agent_demo.py --project-dir ./claude_clone_demo
    python autonomous_agent_demo.py --project-dir ./claude_clone_demo --max-iterations 5
"""

import argparse
import asyncio
import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

from agent import run_autonomous_agent
from console_output import agent_console, print_banner, print_phase_start, print_step
from logger import RunLogger


# Configuration
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"


# =============================================================================
# Git Helper Functions
# =============================================================================

def init_git_repo(project_dir: Path) -> tuple[bool, bool]:
    """Initialize a git repository in the project directory.

    Returns:
        (success: bool, newly_created: bool)
    """
    try:
        # Check if already a git repo
        git_dir = project_dir / ".git"
        if git_dir.exists():
            print_step(f"Git repository already exists in {project_dir}", "info")
            return True, False  # Success, but not newly created

        subprocess.run(
            ["git", "init"],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True
        )

        # Configure git user for this repo (in case global config is missing)
        subprocess.run(
            ["git", "config", "user.email", "agent@backend-harness.local"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        subprocess.run(
            ["git", "config", "user.name", "Backend Harness Agent"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        print_step(f"Initialized git repository in {project_dir}", "success")
        return True, True  # Success, and newly created
    except subprocess.CalledProcessError as e:
        print_step(f"Failed to initialize git repo: {e.stderr}", "error")
        return False, False
    except FileNotFoundError:
        print_step("Git not found. Skipping repository initialization.", "warning")
        return False, False


def git_commit(project_dir: Path, message: str, body: str = None) -> bool:
    """Stage all changes and create a commit with optional detailed body.
    
    Args:
        project_dir: Project directory path
        message: Commit subject line (first line)
        body: Optional detailed commit body with bullet points
    """
    try:
        # Stage all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True
        )

        # Check if there are changes to commit
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        if not result.stdout.strip():
            print_step("No changes to commit", "info")
            return False

        # Build full commit message
        if body:
            full_message = f"{message}\n\n{body}"
        else:
            full_message = message

        # Commit
        subprocess.run(
            ["git", "commit", "-m", full_message],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True
        )
        # Show only first line in success message
        print_step(f"Committed: {message}", "success")
        return True
    except subprocess.CalledProcessError as e:
        print_step(f"Git commit failed: {e.stderr}", "error")
        return False


def create_gitignore(project_dir: Path) -> None:
    """Create a .gitignore file for the project."""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Database
*.db
*.sqlite3

# Build
dist/
build/
*.egg-info/

# Logs
*.log
logs/

# Node (if any frontend)
node_modules/
"""
    gitignore_path = project_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text(gitignore_content)
        print_step("Created .gitignore", "success")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Autonomous Coding Agent Demo - Long-running agent harness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start fresh project
  python autonomous_agent_demo.py --project-dir ./claude_clone

  # Use a specific model
  python autonomous_agent_demo.py --project-dir ./claude_clone --model claude-sonnet-4-5-20250929

  # Limit iterations for testing
  python autonomous_agent_demo.py --project-dir ./claude_clone --max-iterations 5

  # Continue existing project
  python autonomous_agent_demo.py --project-dir ./claude_clone

Configuration:
  Create a .env file with your API key:
    ANTHROPIC_API_KEY=your-api-key-here

  Or set it as an environment variable:
    export ANTHROPIC_API_KEY='your-api-key-here'
        """,
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path("./autonomous_demo_project"),
        help="Directory for the project (default: generations/autonomous_demo_project). Relative paths automatically placed in generations/ directory.",
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of agent iterations (default: unlimited)",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )

    parser.add_argument(
        "--config",
        type=str,
        default="medium",
        choices=["small", "medium", "large", "test"],
        help="App size configuration (test=5-10 tests for pipeline validation, small=20-30 tests, medium=100-200 tests, large=300-500 tests). Default: medium",
    )

    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Skip git repository initialization and commits",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output including all tool calls and results",
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Minimal output - only phases, errors, and summaries",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    # Load environment variables from .env file
    load_dotenv()

    args = parse_args()
    
    # Set verbosity level globally
    if args.verbose:
        agent_console.set_verbosity("verbose")
    elif args.quiet:
        agent_console.set_verbosity("quiet")
    else:
        agent_console.set_verbosity("normal")

    # Check for API key - support both Anthropic and Azure Foundry
    has_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_azure = bool(os.environ.get("AZURE_FOUNDRY_API_KEY") and os.environ.get("AZURE_FOUNDRY_BASE_URL"))
    
    if not (has_anthropic or has_azure):
        agent_console.print_error(
            "Missing API Configuration",
            "No API credentials found in environment",
            "You need to configure either:\n\n"
            "Option 1 - Direct Anthropic API:\n"
            "  Set ANTHROPIC_API_KEY (get from https://console.anthropic.com/)\n"
            "  Example: ANTHROPIC_API_KEY=your-api-key-here\n\n"
            "Option 2 - Azure Foundry:\n"
            "  Set both AZURE_FOUNDRY_API_KEY and AZURE_FOUNDRY_BASE_URL\n"
            "  Example: AZURE_FOUNDRY_API_KEY=your-key\n"
            "           AZURE_FOUNDRY_BASE_URL=https://your-endpoint.inference.ai.azure.com\n\n"
            "Add these to a .env file or export as environment variables."
        )
        return

    # Automatically place projects in generations/ directory unless already specified
    project_dir = args.project_dir
    if not str(project_dir).startswith("generations/"):
        # Convert relative paths to be under generations/
        if project_dir.is_absolute():
            # If absolute path, use as-is
            pass
        else:
            # Prepend generations/ to relative paths
            project_dir = Path("generations") / project_dir

    # Print beautiful banner
    print_banner(args.model, str(project_dir), args.config)

    # Initialize git repository (unless --no-git flag is set)
    git_enabled = not args.no_git
    if git_enabled:
        with print_phase_start("Environment Setup"):
            project_dir.mkdir(parents=True, exist_ok=True)
            print_step("Project directory created", "success")

            success, newly_created = init_git_repo(project_dir)
            if success and newly_created:
                # Only create initial commit for newly created repos
                create_gitignore(project_dir)
                git_commit(
                    project_dir,
                    "Initial commit: project setup",
                    """- Created project directory structure
- Initialized git repository
- Added .gitignore for Python projects
- Ready for autonomous agent development"""
                )

    # Initialize run logger
    run_logger = RunLogger(project_dir, args.model, args.config)

    # Run the agent
    try:
        asyncio.run(
            run_autonomous_agent(
                project_dir=project_dir,
                model=args.model,
                max_iterations=args.max_iterations,
                config_name=args.config,
                git_enabled=git_enabled,
                run_logger=run_logger,
            )
        )
    except KeyboardInterrupt:
        agent_console.print_keyboard_interrupt()
        # Finalize logger on interrupt
        run_logger.finalize()
    except Exception as e:
        agent_console.print_error("Fatal Error", str(e))
        # Finalize logger on error
        run_logger.finalize()
        raise
    else:
        # Finalize logger on successful completion
        run_logger.finalize()


if __name__ == "__main__":
    main()
