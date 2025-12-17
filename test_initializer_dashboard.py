#!/usr/bin/env python3
"""Test dashboard for INITIALIZER agent (Session 1, no tests yet)"""
import time
import asyncio
from pathlib import Path
from console_output import agent_console

async def test_initializer():
    """Simulate initializer agent session"""
    
    # Create temp project WITHOUT feature_list.json
    temp_project = Path("demo_temp_init")
    temp_project.mkdir(exist_ok=True)
    
    # Make sure feature_list.json does NOT exist
    feature_list_file = temp_project / "feature_list.json"
    if feature_list_file.exists():
        feature_list_file.unlink()
    
    agent_console.set_verbosity("normal")
    
    print("\n" + "="*80)
    print("  🚀 INITIALIZER AGENT - Session 1")
    print("  Dashboard should show 'Generating test suite...' not test progress")
    print("="*80 + "\n")
    
    # Session 1 (initializer)
    with agent_console.live_session(iteration=1, max_iterations=5, project_dir=temp_project):
        # Initial thinking and planning
        agent_console.add_agent_thought("Reading application specification and understanding requirements...")
        agent_console.add_tokens(12000, 2000)
        
        await asyncio.sleep(3)
        
        # Reading spec files
        agent_console.start_tool_batch()
        agent_console.update_tool_call("read_file: app_spec.txt", "running")
        await asyncio.sleep(0.5)
        agent_console.update_tool_call("read_file: app_spec.txt", "success")
        agent_console.add_tokens(3000, 500)
        agent_console.end_tool_batch()
        
        await asyncio.sleep(2)
        
        agent_console.add_agent_thought("Analyzing requirements and designing comprehensive test suite...")
        agent_console.add_tokens(8000, 15000)  # Big thinking - creating tests
        
        await asyncio.sleep(3)
        
        # Creating test suite
        agent_console.start_tool_batch()
        agent_console.update_tool_call("write_file: feature_list.json", "running")
        await asyncio.sleep(1)
        agent_console.update_tool_call("write_file: feature_list.json", "success")
        agent_console.add_tokens(2000, 8000)
        agent_console.end_tool_batch()
        
        await asyncio.sleep(2)
        
        agent_console.add_agent_thought("Creating project structure and initial implementation...")
        agent_console.add_tokens(5000, 12000)
        
        await asyncio.sleep(3)
        
        # Creating initial files
        agent_console.start_tool_batch()
        files = [
            "write_file: app/main.py",
            "write_file: app/models.py",
            "write_file: requirements.txt",
            "write_file: init.sh"
        ]
        for f in files:
            agent_console.update_tool_call(f, "running")
            await asyncio.sleep(0.4)
            agent_console.update_tool_call(f, "success")
            agent_console.add_tokens(800, 3500)
        agent_console.end_tool_batch()
        
        await asyncio.sleep(2)
    
    print("\n" + "="*80)
    print("  ✅ Initializer dashboard test complete!")
    print("  Should have shown: 'Generating test suite...' not test progress")
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(test_initializer())
