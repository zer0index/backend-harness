#!/usr/bin/env python3
"""
Demo script to showcase the enhanced console output
"""
import time
from console_output import agent_console, print_banner, print_phase_start, print_step

def demo():
    """Run a demo of the enhanced console output."""
    
    # Banner
    print_banner(
        "claude-sonnet-4-5-20250929",
        "./generations/demo_project",
        "medium"
    )
    
    time.sleep(0.5)
    
    # Phase with steps
    with print_phase_start("Environment Setup"):
        time.sleep(0.3)
        print_step("Project directory created", "success")
        time.sleep(0.3)
        print_step("Git repository initialized", "success")
        time.sleep(0.3)
        print_step("Configuration loaded", "info")
        time.sleep(0.3)
        print_step(".gitignore created", "success")
    
    time.sleep(0.5)
    
    # Iteration header
    agent_console.start_iteration(1, 5)
    
    time.sleep(0.3)
    agent_console.update_tool_call("read_file", "success")
    time.sleep(0.2)
    agent_console.update_tool_call("write_file", "success")
    time.sleep(0.2)
    agent_console.update_tool_call("bash", "success")
    
    time.sleep(0.5)
    
    # Iteration summary
    agent_console.print_iteration_summary(
        duration=45.2,
        tokens_used=12450,
        files_modified=["src/main.py", "requirements.txt", "README.md"],
        tool_calls=3
    )
    
    time.sleep(0.5)
    
    # Warning example
    agent_console.print_warning(
        "Long Operation",
        "Tool execution took longer than expected",
        "Tool: bash (pytest tests/)\nDuration: 45s (threshold: 30s)"
    )
    
    time.sleep(0.5)
    
    # Error example
    agent_console.print_error(
        "Tool Execution Failed",
        "pip install failed",
        "ERROR: Could not find a version that satisfies the requirement invalid-package"
    )
    
    time.sleep(0.5)
    
    # Thinking example
    agent_console.print_thinking(
        "I need to first check the current dependencies in requirements.txt "
        "before adding the new package..."
    )
    
    time.sleep(0.5)
    
    # Final summary
    agent_console.print_final_summary(
        total_duration=942.5,
        iterations=5,
        total_tokens=156890,
        cost_estimate=0.78,
        files_created=12,
        files_modified=8,
        git_commits=5,
        test_results={"total": 156, "passed": 154}
    )

if __name__ == "__main__":
    demo()
