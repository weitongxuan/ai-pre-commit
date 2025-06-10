#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the AI Pre-Commit Hook.
This script creates a test git repository and performs a commit with intentional errors
to test if the AI pre-commit hook correctly identifies them.
"""

import os
import shutil
import subprocess
import sys
import tempfile

def setup_test_repo():
    """Set up a temporary git repository for testing."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Initialize git repository
    subprocess.run(["git", "init"], cwd=temp_dir, check=True)
    
    # Configure git user
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_dir, check=True)
    
    return temp_dir

def install_hook(repo_dir, hook_script):
    """Install the pre-commit hook to the test repository."""
    hooks_dir = os.path.join(repo_dir, ".git", "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    
    # Copy the hook script
    shutil.copy2(hook_script, os.path.join(hooks_dir, "pre-commit"))
    
    # Make it executable
    os.chmod(
        os.path.join(hooks_dir, "pre-commit"),
        os.stat(os.path.join(hooks_dir, "pre-commit")).st_mode | 0o111
    )

def create_test_file_with_errors(repo_dir):
    """Create a test file with intentional errors."""
    test_file = os.path.join(repo_dir, "test_file.py")
    
    with open(test_file, "w") as f:
        f.write("""
def add_numbers(a, b):
    # This function has an intentional error - it tries to add strings without conversion
    return a + b

def main():
    # This will cause a TypeError if called with strings
    result = add_numbers("10", "20")
    print("The result is:", result)
    
    # Undefined variable
    print(undefined_variable)
    
    # Syntax error - missing closing parenthesis
    print("Hello world"
    
    # Security issue - using eval with user input
    user_input = input("Enter something: ")
    eval(user_input)

if __name__ == "__main__":
    main()
""")
    
    return test_file

def test_commit(repo_dir, test_file):
    """Try to commit the test file and see if the hook catches the errors."""
    # Stage the file
    subprocess.run(["git", "add", test_file], cwd=repo_dir, check=True)
    
    # Try to commit
    try:
        result = subprocess.run(
            ["git", "commit", "-m", "Test commit with errors"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr

def main():
    """Main function for the test script."""
    # Check if OpenAI API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)
    
    # Get the path to the hook script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    hook_script = os.path.join(script_dir, "ai_pre_commit.py")
    
    # Set up test repository
    print("Setting up test repository...")
    repo_dir = setup_test_repo()
    
    try:
        # Install hook
        print("Installing pre-commit hook...")
        install_hook(repo_dir, hook_script)
        
        # Create test file with errors
        print("Creating test file with errors...")
        test_file = create_test_file_with_errors(repo_dir)
        
        # Try to commit
        print("Attempting to commit...")
        returncode, stdout, stderr = test_commit(repo_dir, test_file)
        
        # Check results
        if returncode != 0:
            print("Test PASSED: Pre-commit hook correctly blocked the commit.")
            print("Hook output:")
            print(stdout)
            print(stderr)
        else:
            print("Test FAILED: Pre-commit hook did not block the commit with errors.")
            print("Hook output:")
            print(stdout)
            print(stderr)
    
    finally:
        # Clean up
        print("Cleaning up...")
        shutil.rmtree(repo_dir)

if __name__ == "__main__":
    main()
