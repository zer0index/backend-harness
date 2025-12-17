"""
Prompt Loading Utilities
========================

Functions for loading prompt templates from the prompts directory.
"""

import json
import shutil
from pathlib import Path


PROMPTS_DIR = Path(__file__).parent / "prompts"
CONFIGS_DIR = Path(__file__).parent / "configs"


def load_config(config_name: str = 'medium') -> dict:
    """Load configuration file for app size/complexity.

    Args:
        config_name: Name of config file (small, medium, large)

    Returns:
        Dictionary containing configuration values
    """
    config_path = CONFIGS_DIR / f'{config_name}.json'

    if not config_path.exists():
        print(f"⚠️  Warning: Config '{config_name}' not found, using 'medium'")
        config_path = CONFIGS_DIR / 'medium.json'

    with open(config_path, encoding='utf-8') as f:
        config = json.load(f)

    print(f"📋 Using '{config['app_size']}' configuration: {config['description']}")
    print(f"   Tests: {config['test_spec']['min_tests']}-{config['test_spec']['max_tests']}")
    print(f"   Endpoints: {config['test_spec']['min_endpoints']}-{config['test_spec']['max_endpoints']}")
    print(f"   Expected duration: {config['session_expectations']['total_sessions']}")

    return config


def apply_config_to_prompt(prompt_text: str, config: dict) -> str:
    """Replace placeholders in prompt with config values.

    Args:
        prompt_text: Prompt template with {{PLACEHOLDER}} markers
        config: Configuration dictionary

    Returns:
        Prompt with placeholders replaced by actual values
    """
    replacements = {
        '{{MIN_TESTS}}': str(config['test_spec']['min_tests']),
        '{{MAX_TESTS}}': str(config['test_spec']['max_tests']),
        '{{MIN_ENDPOINTS}}': str(config['test_spec']['min_endpoints']),
        '{{MAX_ENDPOINTS}}': str(config['test_spec']['max_endpoints']),
        '{{TESTS_PER_ENDPOINT}}': config['test_spec']['tests_per_endpoint'],
        '{{MOCK_USERS}}': str(config['mock_data']['users']),
        '{{MOCK_MAIN_ENTITY}}': str(config['mock_data']['main_entity']),
        '{{MOCK_SECONDARY}}': str(config['mock_data']['secondary_entities']),
        '{{INIT_DURATION}}': config['session_expectations']['initializer_duration'],
        '{{TOTAL_SESSIONS}}': config['session_expectations']['total_sessions']
    }

    for placeholder, value in replacements.items():
        prompt_text = prompt_text.replace(placeholder, value)

    return prompt_text


def load_prompt(name: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = PROMPTS_DIR / f"{name}.md"
    return prompt_path.read_text(encoding='utf-8')


def get_initializer_prompt(config_name: str = 'medium') -> str:
    """Load and configure the initializer prompt.

    Args:
        config_name: Configuration size (small, medium, large)

    Returns:
        Configured prompt with values substituted
    """
    config = load_config(config_name)
    prompt = load_prompt("initializer_prompt")
    return apply_config_to_prompt(prompt, config)


def get_coding_prompt(config_name: str = 'medium') -> str:
    """Load and configure the coding agent prompt.

    Args:
        config_name: Configuration size (small, medium, large)

    Returns:
        Configured prompt with values substituted
    """
    config = load_config(config_name)
    prompt = load_prompt("coding_prompt")
    return apply_config_to_prompt(prompt, config)


def copy_spec_to_project(project_dir: Path, config_name: str = 'medium') -> None:
    """Copy the app spec file into the project directory for the agent to read.
    
    Args:
        project_dir: Target project directory
        config_name: Configuration name - uses app_spec_test.txt for 'test' config
    """
    # Use minimal spec for test config, full spec otherwise
    if config_name == 'test':
        spec_source = PROMPTS_DIR / "app_spec_test.txt"
    else:
        spec_source = PROMPTS_DIR / "app_spec.txt"
    
    spec_dest = project_dir / "app_spec.txt"
    if not spec_dest.exists():
        shutil.copy(spec_source, spec_dest)
        print(f"Copied {spec_source.name} to project directory as app_spec.txt")


def copy_templates_to_project(project_dir: Path) -> None:
    """Copy template files into the project directory for the agent to use."""
    templates_source = PROMPTS_DIR / "templates"
    templates_dest = project_dir / "prompts" / "templates"

    if templates_source.exists() and not templates_dest.exists():
        # Create the prompts directory structure in the project
        templates_dest.parent.mkdir(parents=True, exist_ok=True)

        # Copy the entire templates directory
        shutil.copytree(templates_source, templates_dest)
        print("Copied template files to project directory")
