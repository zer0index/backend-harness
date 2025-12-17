Plan: Add minimal "test" config for fast pipeline validation
Add a new "test" configuration with a separate minimal spec file (app_spec_test.txt) using a simple Notes API domain, keeping all pipeline stages intact for full workflow coverage.

Steps
Create configs/test.json with minimal settings:

Create prompts/app_spec_test.txt — minimal Notes API spec with:

2 resources: User (mock auth), Note (title, content, user_id, timestamps)
5 endpoints: health check, list notes, create note, get note, delete note
Basic validation, pagination, and error handling
Simplified DB schema (2 tables)
Update autonomous_agent_demo.py — add "test" to the --config argument's choices list.

Modify copy_spec_to_project() in prompts.py — accept a config_name parameter and copy app_spec_test.txt when config is "test", otherwise use app_spec.txt.

Update call chain in agent.py — pass config_name from run_agent() through to copy_spec_to_project() so the correct spec file is selected based on the chosen config.