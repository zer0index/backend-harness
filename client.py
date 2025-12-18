"""
Claude SDK Client Configuration
===============================

Functions for creating and configuring the Claude Agent SDK client.
"""

import json
import os
from pathlib import Path

from claude_code_sdk import ClaudeCodeOptions, ClaudeSDKClient
from claude_code_sdk.types import HookMatcher

from security import bash_security_hook


# Built-in tools for backend development
BUILTIN_TOOLS = [
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "Bash",
]


def create_client(project_dir: Path, model: str) -> ClaudeSDKClient:
    """
    Create a Claude Agent SDK client with multi-layered security.

    Args:
        project_dir: Directory for the project
        model: Claude model to use

    Returns:
        Configured ClaudeSDKClient

    Security layers (defense in depth):
    1. Sandbox - OS-level bash command isolation prevents filesystem escape
    2. Permissions - File operations restricted to project_dir only
    3. Security hooks - Bash commands validated against an allowlist
       (see security.py for ALLOWED_COMMANDS)
    
    API Configuration:
    - Use ANTHROPIC_API_KEY for direct Anthropic API access
    - OR use AZURE_FOUNDRY_API_KEY + AZURE_FOUNDRY_BASE_URL for Azure Foundry
    """
    # Check for Azure Foundry configuration first
    azure_api_key = os.environ.get("AZURE_FOUNDRY_API_KEY")
    azure_base_url = os.environ.get("AZURE_FOUNDRY_BASE_URL")
    azure_model_name = os.environ.get("AZURE_FOUNDRY_MODEL_NAME")
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

    # Determine which API configuration to use
    if azure_api_key and azure_base_url:
        api_key = azure_api_key

        # Normalize base URL for Azure Foundry
        # Should end with /anthropic (not /anthropic/v1/messages)
        base_url = azure_base_url.rstrip('/')

        # Remove /v1/messages or /anthropic/v1/messages if present
        if '/v1/messages' in base_url:
            if '/anthropic/v1/messages' in base_url:
                base_url = base_url.split('/anthropic/v1/messages')[0] + '/anthropic'
            elif '/v1/messages' in base_url:
                base_url = base_url.split('/v1/messages')[0]

        # Ensure it ends with /anthropic
        if not base_url.endswith('/anthropic'):
            base_url = f"{base_url}/anthropic"

        # Use Azure Foundry deployment name if provided, otherwise use the passed model
        # Azure uses deployment names like "claude-sonnet-4-5" instead of full model IDs
        if azure_model_name:
            model = azure_model_name
            print(f"Using Azure Foundry endpoint: {base_url}")
            print(f"Using Azure deployment: {model}")
        else:
            # If no deployment name specified, try to infer from the model parameter
            # e.g., "claude-sonnet-4-5-20250929" -> "claude-sonnet-4-5"
            if "claude-sonnet-4" in model.lower():
                model = "claude-sonnet-4-5"
                print(f"Using Azure Foundry endpoint: {base_url}")
                print(f"Using inferred Azure deployment: {model} (set AZURE_FOUNDRY_MODEL_NAME to override)")
            else:
                print(f"Using Azure Foundry endpoint: {base_url}")
                print(f"Using model: {model}")
    elif anthropic_api_key:
        api_key = anthropic_api_key
        base_url = None  # Use default Anthropic endpoint
        print("Using direct Anthropic API")
    else:
        raise ValueError(
            "No API configuration found.\n\n"
            "Option 1 - Direct Anthropic API:\n"
            "  Set ANTHROPIC_API_KEY (get from https://console.anthropic.com/)\n\n"
            "Option 2 - Azure Foundry:\n"
            "  Set AZURE_FOUNDRY_API_KEY, AZURE_FOUNDRY_BASE_URL\n"
            "  Optionally: AZURE_FOUNDRY_MODEL_NAME (deployment name, e.g., 'claude-sonnet-4-5')\n\n"
            "Add these to a .env file or export as environment variables."
        )

    # Create comprehensive security settings
    # Note: Using relative paths ("./**") restricts access to project directory
    # since cwd is set to project_dir
    security_settings = {
        "sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True},
        "permissions": {
            "defaultMode": "acceptEdits",  # Auto-approve edits within allowed directories
            "allow": [
                # Allow all file operations within the project directory
                "Read(./**)",
                "Write(./**)",
                "Edit(./**)",
                "Glob(./**)",
                "Grep(./**)",
                # Bash permission granted here, but actual commands are validated
                # by the bash_security_hook (see security.py for allowed commands)
                "Bash(*)",
            ],
        },
    }

    # Ensure project directory exists before creating settings file
    project_dir.mkdir(parents=True, exist_ok=True)

    # Write settings to a file in the project directory
    settings_file = project_dir / ".claude_settings.json"
    with open(settings_file, "w", encoding='utf-8') as f:
        json.dump(security_settings, f, indent=2)

    print(f"Created security settings at {settings_file}")
    print("   - Sandbox enabled (OS-level bash isolation)")
    print(f"   - Filesystem restricted to: {project_dir.resolve()}")
    print("   - Bash commands restricted to allowlist (see security.py)")
    print()

    # Build client options
    client_options = ClaudeCodeOptions(
        model=model,
        system_prompt="You are an expert backend API developer building production-quality FastAPI applications with comprehensive test coverage.",
        allowed_tools=BUILTIN_TOOLS,
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Bash", hooks=[bash_security_hook]),
            ],
        },
        max_turns=1000,
        cwd=str(project_dir.resolve()),
        settings=str(settings_file.resolve()),  # Use absolute path
    )
    
    # Add base_url if using Azure Foundry
    if base_url:
        client_options.base_url = base_url
    
    return ClaudeSDKClient(options=client_options)
