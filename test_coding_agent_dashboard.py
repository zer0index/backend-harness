#!/usr/bin/env python3
"""Test dashboard for CODING agent with diverse tool usage"""
import time
import asyncio
import json
from pathlib import Path
from console_output import agent_console

async def test_coding_agent():
    """Simulate coding agent session with lots of different tools"""
    
    # Create temp project WITH feature_list.json
    temp_project = Path("demo_temp_coding")
    temp_project.mkdir(exist_ok=True)
    
    # Create feature_list.json with progress
    feature_list = [
        {"feature": f"Feature {i}", "passes": i <= 45} 
        for i in range(1, 101)
    ]
    with open(temp_project / "feature_list.json", "w") as f:
        json.dump(feature_list, f)
    
    agent_console.set_verbosity("normal")
    
    print("\n" + "="*80)
    print("  🚀 CODING AGENT - Session 3 (with Tool Breakdown)")
    print("="*80 + "\n")
    
    # Session 3 (coding agent)
    with agent_console.live_session(iteration=3, max_iterations=5, project_dir=temp_project):
        # Reading phase
        agent_console.add_agent_thought("Analyzing current code and test failures...")
        agent_console.add_tokens(5000, 800)
        await asyncio.sleep(2)
        
        agent_console.start_tool_batch()
        for i in range(8):
            agent_console.update_tool_call("read_file: app/main.py", "running")
            await asyncio.sleep(0.3)
            agent_console.update_tool_call("read_file: app/main.py", "success")
            agent_console.add_tokens(800, 200)
        agent_console.end_tool_batch()
        
        await asyncio.sleep(2)
        
        # Grep/search phase
        agent_console.add_agent_thought("Searching for authentication patterns...")
        agent_console.add_tokens(2000, 400)
        await asyncio.sleep(2)
        
        agent_console.start_tool_batch()
        for i in range(5):
            agent_console.update_tool_call("grep: def login", "running")
            await asyncio.sleep(0.2)
            agent_console.update_tool_call("grep: def login", "success")
            agent_console.add_tokens(500, 150)
        agent_console.end_tool_batch()
        
        await asyncio.sleep(1)
        
        # Writing phase
        agent_console.add_agent_thought("Implementing new endpoints and fixing bugs...")
        agent_console.add_tokens(3000, 8000)
        await asyncio.sleep(2)
        
        agent_console.start_tool_batch()
        for i in range(6):
            agent_console.update_tool_call("write_file: app/routes.py", "running")
            await asyncio.sleep(0.4)
            agent_console.update_tool_call("write_file: app/routes.py", "success")
            agent_console.add_tokens(600, 2500)
        agent_console.end_tool_batch()
        
        await asyncio.sleep(1)
        
        # Editing phase
        agent_console.start_tool_batch()
        for i in range(12):
            agent_console.update_tool_call("edit_file: app/main.py", "running")
            await asyncio.sleep(0.3)
            agent_console.update_tool_call("edit_file: app/main.py", "success")
            agent_console.add_tokens(500, 1800)
        agent_console.end_tool_batch()
        
        await asyncio.sleep(1)
        
        # Testing phase
        agent_console.add_agent_thought("Running test suite...")
        agent_console.add_tokens(1000, 500)
        await asyncio.sleep(2)
        
        agent_console.start_tool_batch()
        for i in range(8):
            agent_console.update_tool_call("bash: pytest -xvs", "running")
            await asyncio.sleep(0.5)
            agent_console.update_tool_call("bash: pytest -xvs", "success")
            agent_console.add_tokens(400, 1200)
        agent_console.end_tool_batch()
        
        await asyncio.sleep(2)
    
    print("\n" + "="*80)
    print("  ✅ Coding agent test complete!")
    print("  Tool breakdown shows: Read, Write, Edit, Grep, Bash")
    print("  Test progress bar visible at bottom")
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(test_coding_agent())
