import subprocess
import sys
import re

def run_cmd(*args):
    print(f"Running: {' '.join(args)}")
    import os
    exe_path = os.path.join(os.path.dirname(sys.executable), "notebooklm.exe")
    cmd = [exe_path] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error ({result.returncode}): {result.stderr}")
    return result.stdout

def create_notebook_and_add_sources(title, files):
    out = run_cmd("create", title)
    print(out)
    
    # Extract ID. Usually "Created notebook: <uuid>" or similar.
    # The CLI outputs standard text.
    match = re.search(r'([a-f0-9\-]{36})', out)
    if not match:
        # If the output format is different, we can try listing notebooks and getting the latest.
        out = run_cmd("list")
        lines = out.strip().split("\n")
        # Try to find the title in the table
        for line in lines:
            if title in line:
                match = re.search(r'([a-f0-9\-]{36})', line)
                if match:
                    break

    if match:
        notebook_id = match.group(1)
        print(f"Using notebook ID: {notebook_id}")
        run_cmd("use", notebook_id)
        for f in files:
            run_cmd("source", "add", f)
            print(f"Added {f}")
    else:
        print(f"Could not find ID for notebook: {title}")

def main():
    notebooks = {
        "Bravo Core Knowledge": [
            "CLAUDE.md",
            "GEMINI.md",
            "ANTIGRAVITY.md",
            "BLACKBOX.md",
            "brain/SOUL.md",
            "brain/STATE.md",
            "brain/CAPABILITIES.md",
            "brain/AGENTS.md"
        ],
        "OASIS AI": [
            "APPS_CONTEXT/OASIS_AI_CLAUDE.md",
            "APPS_CONTEXT/OASIS_WORKFLOWS.md"
        ],
        "PropFlow": [
            "APPS_CONTEXT/PROPFLOW_CLAUDE.md"
        ],
        "Nostalgic Requests": [
            "APPS_CONTEXT/NOSTALGIC_REQUESTS_CLAUDE.md"
        ],
        "Content & Media": [
            "APPS_CONTEXT/CONTENT_BRAND_CLAUDE.md",
            "APPS_CONTEXT/AI_TRAINING_CLAUDE.md"
        ]
    }
    
    for title, files in notebooks.items():
        print(f"\n--- Populating {title} ---")
        create_notebook_and_add_sources(title, files)

if __name__ == "__main__":
    main()
