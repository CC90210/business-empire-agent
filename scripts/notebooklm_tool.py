import sys
import json
import subprocess
import os

def run_command(args):
    """Run a notebooklm CLI command and return the output."""
    cmd = [sys.executable.replace("python.exe", "notebooklm.exe")] + args
    
    # If notebooklm.exe isn't found in the same dir as python.exe, try calling it via python -m notebooklm.cli
    # (Though notebooklm-py installs a console script)
    if not os.path.exists(cmd[0]):
         cmd = [sys.executable, "-m", "notebooklm.cli"] + args

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"status": "success", "stdout": result.stdout, "stderr": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "stdout": e.stdout, "stderr": e.stderr, "exit_code": e.returncode}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No command provided."}))
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    # Handle JSON input if the first arg is '--json-input'
    if command == "--json-input" and len(args) > 0:
        try:
            input_data = json.loads(args[0])
            command = input_data.get("command")
            args = input_data.get("args", [])
        except json.JSONDecodeError:
            print(json.dumps({"status": "error", "message": "Invalid JSON input."}))
            return

    if not command:
        print(json.dumps({"status": "error", "message": "No command specified in JSON."}))
        return

    # Map commands to notebooklm CLI
    # Example: command="create", args=["My Notebook"] -> notebooklm create "My Notebook"
    # We'll just pass them through to the CLI
    full_args = [command] + args
    output = run_command(full_args)
    print(json.dumps(output))

if __name__ == "__main__":
    main()
