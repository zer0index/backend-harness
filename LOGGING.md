# Logging System Documentation

## Overview

The autonomous agent harness now includes a comprehensive logging system that captures every detail of agent sessions. This helps you understand what happened during long-running sessions, identify bottlenecks, and debug issues.

## What Gets Logged

### Session-Level Logs
Each agent session generates a detailed JSON log containing:

- **Tool Calls**: Every tool call with timestamps, duration, input parameters, and results
- **Agent Messages**: All agent thoughts and reasoning
- **Token Usage**: Input/output token counts per message and cumulative totals
- **Errors**: Full error messages and stack traces
- **Security Blocks**: Commands blocked by security hooks with reasons
- **Progress**: Test counts and completion percentage
- **Timing**: Start/end times and duration for every operation

### Run-Level Logs
Each run (execution of autonomous_agent_demo.py) gets:

- **Run Summary**: Overall statistics across all sessions
- **Timeline**: Append-only event stream (JSONL format)
- **Metrics**: Aggregated token usage, tool counts, error rates

## Log Structure

```
project_dir/
  logs/
    run_20231219_103045/           # Timestamp-based run directory
      session_001.json             # Detailed session log
      session_002.json
      session_003.json
      run_summary.json             # Run-wide summary
      timeline.jsonl               # Append-only event stream
    run_20231219_150230/
      ...
```

## Sensitive Data Protection

The logging system automatically filters sensitive information:

- API keys (ANTHROPIC_API_KEY, AZURE_FOUNDRY_API_KEY)
- Environment variables with: KEY, TOKEN, SECRET, PASSWORD
- Bearer tokens
- Any credentials in command outputs

Filtered values are replaced with `[REDACTED]`.

## Using the Logs

### 1. Automatic Logging

Logging is enabled automatically when you run the harness:

```bash
python autonomous_agent_demo.py --project-dir ./my_project
```

You'll see output like:
```
📁 Logging to: my_project/logs/run_20231219_103045
   Run ID: run_20231219_103045
```

### 2. Analyzing Sessions

Use the `analyze_logs.py` script to analyze logs:

#### Analyze a Specific Session
```bash
python analyze_logs.py project/logs/run_20231219_103045/session_001.json
```

**Output:**
- Session overview (duration, tool counts, errors, tokens)
- Slowest tool calls (top 10)
- Most used tools
- Repeated file operations (potential stuck loops)
- Long gaps between tool calls (potential hangs)
- Potential issues (errors, anomalies)
- Progress summary

#### Compare All Sessions in a Run
```bash
python analyze_logs.py project/logs/run_20231219_103045 --compare
```

**Output:**
- Side-by-side session comparison table
- Highlights longest session
- Total run statistics

#### View Event Timeline
```bash
python analyze_logs.py project/logs/run_20231219_103045/session_001.json --timeline
```

Shows chronological event stream (first 100 events).

## Understanding the Analysis

### Key Metrics

**Session Duration**
- Red: > 60 minutes (investigate for stuck operations)
- Yellow: 30-60 minutes (may be normal for large projects)
- White: < 30 minutes

**Tool Call Duration**
- Individual tools taking > 30 minutes suggest:
  - Long-running tests
  - Database migrations
  - Package installations
  - Possible hangs

**Repeated Operations**
- Same file edited 20+ times may indicate:
  - Agent stuck in error loop
  - Refining implementation iteratively
  - Test-driven debugging

**Long Gaps**
- Gaps > 60 seconds between tool calls suggest:
  - Agent thinking/planning
  - Processing large context
  - Possible timeout or hang

### Anomaly Detection

The analyzer automatically flags:

1. **Tool failures**: Same tool failing 3+ times
2. **Long operations**: Single tool call > 30 minutes
3. **Repetitive edits**: File modified > 20 times
4. **Security blocks**: Commands blocked by security hooks

## Common Debugging Scenarios

### Scenario 1: Session Took 380 Minutes

**Steps:**
1. Analyze the session:
   ```bash
   python analyze_logs.py project/logs/run_XXXXXX/session_XXX.json
   ```

2. Look for:
   - **Slowest tool calls**: Identify which tool consumed most time
   - **Long gaps**: Check if agent was stuck thinking
   - **Repeated operations**: See if it was editing same file repeatedly
   - **Errors**: Check if retrying failed operations

3. Examine specific tool calls in JSON:
   ```python
   import json
   with open('session_001.json') as f:
       data = json.load(f)

   # Find tools that took > 10 minutes
   slow_tools = [
       t for t in data['tool_calls']
       if t.get('duration_seconds', 0) > 600
   ]
   ```

### Scenario 2: Agent Stuck on Same File

**Indicators:**
- Repeated operations table shows high count for one file
- Many errors on same tool (e.g., pytest failing repeatedly)

**Investigation:**
1. Check the repeated operations section
2. Review tool inputs/outputs in JSON for that file
3. Look at error messages to see what's failing

### Scenario 3: High Token Usage

**Analysis:**
1. Run comparison to see which session used most tokens
2. Check `token_usage` in session JSON:
   ```json
   {
     "token_usage": {
       "input_tokens": 45000,
       "output_tokens": 12000,
       "total_tokens": 57000
     }
   }
   ```
3. Cross-reference with tool calls to see if reading large files

## Log File Formats

### session_NNN.json Structure

```json
{
  "session_number": 1,
  "start_time": "2023-12-19T10:30:45.123456",
  "end_time": "2023-12-19T11:15:23.654321",
  "duration_seconds": 2678.5,
  "duration_minutes": 44.6,
  "events": [
    {
      "timestamp": "2023-12-19T10:30:45.234567",
      "event_type": "tool_start",
      "data": {
        "tool_name": "Read",
        "input": {"file_path": "app/main.py"}
      }
    },
    ...
  ],
  "tool_calls": [
    {
      "tool_name": "Bash",
      "start_time": "2023-12-19T10:30:50.123456",
      "end_time": "2023-12-19T10:30:52.345678",
      "duration_seconds": 2.22,
      "input": {"command": "pytest tests/"},
      "result": {
        "content": "===== 5 passed in 2.1s =====",
        "truncated": false,
        "original_size": 156
      },
      "is_error": false
    }
  ],
  "token_usage": {
    "input_tokens": 12500,
    "output_tokens": 3400,
    "total_tokens": 15900
  },
  "errors": [
    {
      "timestamp": "2023-12-19T10:35:12.123456",
      "tool_name": "Bash",
      "error": "Command failed: pytest failed with 2 errors"
    }
  ],
  "security_blocks": [
    {
      "timestamp": "2023-12-19T10:40:15.123456",
      "tool_name": "Bash",
      "command": "rm -rf /",
      "reason": "Command 'rm' is not in the allowed commands list"
    }
  ],
  "progress": {
    "passing_tests": 45,
    "total_tests": 150,
    "percentage": 30.0,
    "timestamp": "2023-12-19T11:15:23.000000"
  },
  "summary": {
    "total_tool_calls": 127,
    "total_events": 384,
    "total_errors": 3,
    "total_security_blocks": 1,
    "tools_used": ["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
    "slowest_tool_call": {
      "tool_name": "Bash",
      "duration_seconds": 180.5
    },
    "average_tool_duration": 21.1
  }
}
```

### timeline.jsonl Format

Append-only JSON Lines format (one JSON object per line):

```jsonl
{"timestamp": "2023-12-19T10:30:45.123456", "event_type": "tool_start", "data": {...}}
{"timestamp": "2023-12-19T10:30:47.234567", "event_type": "token_usage", "data": {...}}
{"timestamp": "2023-12-19T10:30:52.345678", "event_type": "tool_end", "data": {...}}
```

Useful for streaming analysis or importing into log aggregation tools.

### run_summary.json Structure

```json
{
  "run_id": "run_20231219_103045",
  "project_dir": "/path/to/project",
  "model": "claude-sonnet-4-5-20250929",
  "config": "medium",
  "start_time": "2023-12-19T10:30:45.123456",
  "end_time": "2023-12-19T14:25:15.654321",
  "duration_seconds": 14070.5,
  "duration_minutes": 234.5,
  "sessions": [
    {
      "session_number": 1,
      "start_time": "2023-12-19T10:30:45.123456",
      "end_time": "2023-12-19T11:15:23.654321",
      "duration_minutes": 44.6,
      "tool_calls": 127,
      "errors": 3,
      "security_blocks": 1,
      "tokens_used": 15900
    },
    ...
  ],
  "summary": {
    "total_sessions": 8,
    "total_tool_calls": 1024,
    "total_errors": 12,
    "total_security_blocks": 2,
    "total_tokens": 125000,
    "longest_session": {
      "session_number": 3,
      "duration_minutes": 380.2
    }
  }
}
```

## Advanced Analysis

### Custom Analysis Scripts

You can write custom Python scripts to analyze logs:

```python
import json
from pathlib import Path

# Load session
with open('logs/run_XXX/session_001.json') as f:
    session = json.load(f)

# Find all Bash commands run
bash_commands = [
    t['input']['command']
    for t in session['tool_calls']
    if t['tool_name'] == 'Bash'
]

# Find files modified most
from collections import Counter
files_edited = [
    t['input'].get('file_path', '')
    for t in session['tool_calls']
    if t['tool_name'] in ['Edit', 'Write']
]
print(Counter(files_edited).most_common(10))

# Calculate time spent on different tools
tool_times = {}
for t in session['tool_calls']:
    tool = t['tool_name']
    duration = t.get('duration_seconds', 0) or 0
    tool_times[tool] = tool_times.get(tool, 0) + duration

print(sorted(tool_times.items(), key=lambda x: x[1], reverse=True))
```

### Querying Timeline (JSONL)

```python
# Stream large timeline files efficiently
with open('logs/run_XXX/timeline.jsonl') as f:
    for line in f:
        event = json.loads(line)
        if event['event_type'] == 'security_block':
            print(f"Blocked: {event['data']['command']}")
```

## Best Practices

1. **Keep logs for debugging**: Don't delete logs until you've verified the run succeeded
2. **Analyze long sessions immediately**: If you notice a session taking > 1 hour, analyze it to catch issues early
3. **Review summary after each run**: Quick check for anomalies before continuing
4. **Archive old logs**: Move to `logs_archive/` folder to keep project directory clean

## Troubleshooting

### Logs not being created?

Check that the `logs/` directory was created in your project directory:
```bash
ls -la project_dir/logs/
```

If missing, ensure you're using the latest version of the harness.

### Log file is huge?

Large logs usually indicate:
- Many tool calls (normal for large projects)
- Large file outputs being logged (truncated at 10KB by default)
- Long session duration

You can safely delete the `timeline.jsonl` if you don't need event streaming.

### Can't find specific information?

The JSON logs are comprehensive. Use `jq` for advanced querying:

```bash
# Find all errors
jq '.errors' session_001.json

# Find tool calls longer than 60 seconds
jq '.tool_calls[] | select(.duration_seconds > 60)' session_001.json

# Count tool usage
jq '.tool_calls | group_by(.tool_name) | map({tool: .[0].tool_name, count: length})' session_001.json
```

## Future Enhancements

Potential improvements (contributions welcome):

- Real-time log streaming to web dashboard
- Automatic anomaly alerts during execution
- Export to common log formats (ELK, Splunk)
- Session replay/visualization
- Performance regression detection across runs
