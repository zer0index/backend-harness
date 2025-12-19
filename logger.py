"""
Comprehensive Logging System for Autonomous Agent
==================================================

Provides detailed logging for debugging long-running sessions.
Logs are organized by run (each execution of the harness) and session.

Features:
- JSON-formatted structured logs
- Sensitive data filtering
- Per-run and per-session organization
- Timeline of all events (JSONL format)
- Detailed tool call tracking with timing
- Token usage tracking
- Error and anomaly capture
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


# Sensitive data patterns to filter
SENSITIVE_PATTERNS = [
    r'ANTHROPIC_API_KEY',
    r'AZURE_FOUNDRY_API_KEY',
    r'api[_-]?key',
    r'token',
    r'secret',
    r'password',
    r'bearer\s+\w+',
]


def filter_sensitive_data(data: Any, redact_value: str = "[REDACTED]") -> Any:
    """
    Recursively filter sensitive data from nested structures.

    Args:
        data: Data to filter (dict, list, str, or primitive)
        redact_value: Value to replace sensitive data with

    Returns:
        Filtered copy of the data
    """
    if isinstance(data, dict):
        return {k: filter_sensitive_data(v, redact_value) for k, v in data.items()}
    elif isinstance(data, list):
        return [filter_sensitive_data(item, redact_value) for item in data]
    elif isinstance(data, str):
        # Check for sensitive patterns
        filtered = data
        for pattern in SENSITIVE_PATTERNS:
            # Case-insensitive matching
            filtered = re.sub(
                f'({pattern})\\s*[=:]\\s*([^\\s,}}]+)',
                f'\\1={redact_value}',
                filtered,
                flags=re.IGNORECASE
            )
        return filtered
    else:
        return data


def truncate_large_string(s: str, max_length: int = 10000) -> dict:
    """
    Truncate large strings but preserve size information.

    Returns:
        Dict with 'content', 'truncated' flag, and 'original_size'
    """
    if len(s) <= max_length:
        return {
            "content": s,
            "truncated": False,
            "original_size": len(s)
        }
    else:
        return {
            "content": s[:max_length] + f"\n... [truncated {len(s) - max_length} chars]",
            "truncated": True,
            "original_size": len(s)
        }


class SessionLogger:
    """
    Logger for a single agent session.
    Captures all tool calls, agent messages, and timing information.
    """

    def __init__(self, run_dir: Path, session_num: int):
        """
        Initialize session logger.

        Args:
            run_dir: Directory for this run's logs
            session_num: Session number (1, 2, 3, ...)
        """
        self.run_dir = run_dir
        self.session_num = session_num
        self.session_file = run_dir / f"session_{session_num:03d}.json"
        self.timeline_file = run_dir / "timeline.jsonl"

        self.start_time = datetime.now()
        self.events = []
        self.tool_calls = []
        self.current_tool = None
        self.token_usage = {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0
        }

        # Session metadata
        self.session_data = {
            "session_number": session_num,
            "start_time": self.start_time.isoformat(),
            "end_time": None,
            "duration_seconds": None,
            "events": self.events,
            "tool_calls": self.tool_calls,
            "token_usage": self.token_usage,
            "errors": [],
            "security_blocks": [],
            "progress": {}
        }

    def log_event(self, event_type: str, data: dict):
        """
        Log a generic event with timestamp.

        Args:
            event_type: Type of event (e.g., 'tool_start', 'agent_message', 'error')
            data: Event data
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": filter_sensitive_data(data)
        }
        self.events.append(event)

        # Also append to timeline (append-only JSONL)
        self._append_to_timeline(event)

    def _append_to_timeline(self, event: dict):
        """Append event to timeline file (JSONL format)."""
        try:
            with open(self.timeline_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            # Don't crash if timeline write fails
            print(f"Warning: Failed to append to timeline: {e}")

    def log_tool_start(self, tool_name: str, tool_input: dict, tool_use_id: str = None):
        """
        Log the start of a tool call.

        Args:
            tool_name: Name of the tool
            tool_input: Tool input parameters
            tool_use_id: Optional tool use ID
        """
        self.current_tool = {
            "tool_name": tool_name,
            "tool_use_id": tool_use_id,
            "start_time": datetime.now().isoformat(),
            "input": filter_sensitive_data(tool_input),
            "duration_seconds": None,
            "result": None,
            "is_error": False
        }

        self.log_event("tool_start", {
            "tool_name": tool_name,
            "tool_use_id": tool_use_id,
            "input": filter_sensitive_data(tool_input)
        })

    def log_tool_end(self, result: Any, is_error: bool = False):
        """
        Log the completion of a tool call.

        Args:
            result: Tool result/output
            is_error: Whether this was an error
        """
        if self.current_tool is None:
            return

        # Calculate duration
        start_dt = datetime.fromisoformat(self.current_tool["start_time"])
        duration = (datetime.now() - start_dt).total_seconds()

        # Process result (truncate if large, filter sensitive data)
        filtered_result = filter_sensitive_data(result)
        if isinstance(filtered_result, str):
            processed_result = truncate_large_string(filtered_result)
        else:
            processed_result = filtered_result

        self.current_tool["duration_seconds"] = duration
        self.current_tool["result"] = processed_result
        self.current_tool["is_error"] = is_error
        self.current_tool["end_time"] = datetime.now().isoformat()

        # Add to tool calls list
        self.tool_calls.append(self.current_tool.copy())

        # Log event
        self.log_event("tool_end", {
            "tool_name": self.current_tool["tool_name"],
            "duration_seconds": duration,
            "is_error": is_error,
            "result_size": len(str(result)) if result else 0
        })

        # Track errors
        if is_error:
            self.session_data["errors"].append({
                "timestamp": datetime.now().isoformat(),
                "tool_name": self.current_tool["tool_name"],
                "error": processed_result
            })

        self.current_tool = None

    def log_security_block(self, tool_name: str, command: str, reason: str):
        """
        Log a security hook block.

        Args:
            tool_name: Name of blocked tool
            command: Command that was blocked
            reason: Reason for blocking
        """
        block_event = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "command": filter_sensitive_data(command),
            "reason": reason
        }

        self.session_data["security_blocks"].append(block_event)
        self.log_event("security_block", block_event)

    def log_agent_message(self, text: str, token_info: dict = None):
        """
        Log agent text output (thoughts/reasoning).

        Args:
            text: Agent text
            token_info: Optional token usage info
        """
        self.log_event("agent_message", {
            "text": truncate_large_string(text, max_length=5000),
            "token_info": token_info
        })

    def log_token_usage(self, input_tokens: int, output_tokens: int):
        """
        Log token usage for this turn.

        Args:
            input_tokens: Input tokens used
            output_tokens: Output tokens used
        """
        self.token_usage["input_tokens"] += input_tokens
        self.token_usage["output_tokens"] += output_tokens
        self.token_usage["total_tokens"] += input_tokens + output_tokens

        self.log_event("token_usage", {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cumulative_total": self.token_usage["total_tokens"]
        })

    def log_progress(self, passing_tests: int, total_tests: int):
        """
        Log progress checkpoint.

        Args:
            passing_tests: Number of passing tests
            total_tests: Total number of tests
        """
        self.session_data["progress"] = {
            "passing_tests": passing_tests,
            "total_tests": total_tests,
            "percentage": (passing_tests / total_tests * 100) if total_tests > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }

        self.log_event("progress", self.session_data["progress"])

    def finalize(self):
        """
        Finalize the session log and write to disk.
        """
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        self.session_data["end_time"] = end_time.isoformat()
        self.session_data["duration_seconds"] = duration
        self.session_data["duration_minutes"] = duration / 60

        # Add summary statistics
        self.session_data["summary"] = {
            "total_tool_calls": len(self.tool_calls),
            "total_events": len(self.events),
            "total_errors": len(self.session_data["errors"]),
            "total_security_blocks": len(self.session_data["security_blocks"]),
            "tools_used": list(set(tc["tool_name"] for tc in self.tool_calls)),
            "slowest_tool_call": self._get_slowest_tool_call(),
            "average_tool_duration": self._get_average_tool_duration()
        }

        # Write to file
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, indent=2)
            print(f"Session log saved: {self.session_file}")
        except Exception as e:
            print(f"Error saving session log: {e}")

    def _get_slowest_tool_call(self) -> Optional[dict]:
        """Get the slowest tool call in this session."""
        if not self.tool_calls:
            return None

        slowest = max(
            self.tool_calls,
            key=lambda tc: tc.get("duration_seconds", 0) or 0
        )
        return {
            "tool_name": slowest["tool_name"],
            "duration_seconds": slowest.get("duration_seconds", 0)
        }

    def _get_average_tool_duration(self) -> float:
        """Calculate average tool call duration."""
        if not self.tool_calls:
            return 0.0

        durations = [tc.get("duration_seconds", 0) or 0 for tc in self.tool_calls]
        return sum(durations) / len(durations) if durations else 0.0


class RunLogger:
    """
    Logger for an entire autonomous agent run.
    Manages session loggers and run-level summary.
    """

    def __init__(self, project_dir: Path, model: str, config_name: str):
        """
        Initialize run logger.

        Args:
            project_dir: Project directory
            model: Model name being used
            config_name: Configuration name (small/medium/large)
        """
        self.project_dir = project_dir
        self.model = model
        self.config_name = config_name

        # Create run directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = project_dir / "logs" / f"run_{timestamp}"
        self.run_dir.mkdir(parents=True, exist_ok=True)

        self.start_time = datetime.now()
        self.sessions = []
        self.current_session_logger = None

        # Run metadata
        self.run_data = {
            "run_id": f"run_{timestamp}",
            "project_dir": str(project_dir),
            "model": model,
            "config": config_name,
            "start_time": self.start_time.isoformat(),
            "end_time": None,
            "duration_seconds": None,
            "sessions": []
        }

        print(f"\n📁 Logging to: {self.run_dir}")
        print(f"   Run ID: run_{timestamp}\n")

    def start_session(self, session_num: int) -> SessionLogger:
        """
        Start a new session and return its logger.

        Args:
            session_num: Session number

        Returns:
            SessionLogger instance
        """
        self.current_session_logger = SessionLogger(self.run_dir, session_num)
        return self.current_session_logger

    def end_session(self):
        """End the current session and finalize its log."""
        if self.current_session_logger:
            self.current_session_logger.finalize()

            # Add session summary to run data
            session_summary = {
                "session_number": self.current_session_logger.session_num,
                "start_time": self.current_session_logger.session_data["start_time"],
                "end_time": self.current_session_logger.session_data["end_time"],
                "duration_minutes": self.current_session_logger.session_data.get("duration_minutes", 0),
                "tool_calls": len(self.current_session_logger.tool_calls),
                "errors": len(self.current_session_logger.session_data["errors"]),
                "security_blocks": len(self.current_session_logger.session_data["security_blocks"]),
                "tokens_used": self.current_session_logger.token_usage["total_tokens"]
            }
            self.run_data["sessions"].append(session_summary)

            self.current_session_logger = None

    def finalize(self):
        """
        Finalize the run log and write summary.
        """
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        self.run_data["end_time"] = end_time.isoformat()
        self.run_data["duration_seconds"] = duration
        self.run_data["duration_minutes"] = duration / 60

        # Add summary statistics
        total_tool_calls = sum(s["tool_calls"] for s in self.run_data["sessions"])
        total_errors = sum(s["errors"] for s in self.run_data["sessions"])
        total_blocks = sum(s["security_blocks"] for s in self.run_data["sessions"])
        total_tokens = sum(s["tokens_used"] for s in self.run_data["sessions"])

        self.run_data["summary"] = {
            "total_sessions": len(self.run_data["sessions"]),
            "total_tool_calls": total_tool_calls,
            "total_errors": total_errors,
            "total_security_blocks": total_blocks,
            "total_tokens": total_tokens,
            "longest_session": self._get_longest_session()
        }

        # Write run summary
        summary_file = self.run_dir / "run_summary.json"
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(self.run_data, f, indent=2)
            print(f"\n✅ Run summary saved: {summary_file}")
            print(f"   Total duration: {duration / 60:.1f} minutes")
            print(f"   Total sessions: {len(self.run_data['sessions'])}")
            print(f"   Total tool calls: {total_tool_calls}")
        except Exception as e:
            print(f"Error saving run summary: {e}")

    def _get_longest_session(self) -> Optional[dict]:
        """Get the longest session in this run."""
        if not self.run_data["sessions"]:
            return None

        longest = max(
            self.run_data["sessions"],
            key=lambda s: s.get("duration_minutes", 0) or 0
        )
        return {
            "session_number": longest["session_number"],
            "duration_minutes": longest.get("duration_minutes", 0)
        }
