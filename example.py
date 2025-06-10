#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example usage of the AI Pre-Commit Hook.
"""

import os
import subprocess
import sys

def main():
    """Example of how to use the AI Pre-Commit Hook programmatically."""
    # Define the parameters
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)
    
    model = os.environ.get("OPENAI_MODEL", "gpt-4o")
    
    # Custom prompt (optional)
    custom_prompt = """
    You are a code reviewer with expertise in Python. 
    Analyze the following code changes and identify any obvious errors, bugs, 
    or security issues. Only report serious issues that would prevent the code from working correctly.
    If no serious issues are found, respond with "PASS".

    Below are the code changes:
    {code_changes}
    """
    
    # Run the pre-commit hook
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai_pre_commit.py")
    
    cmd = [
        sys.executable, 
        script_path,
        "--api-key", api_key,
        "--model", model,
    ]
    
    # Add custom prompt if specified
    if custom_prompt:
        cmd.extend(["--prompt", custom_prompt])
    
    # Run the command
    result = subprocess.run(cmd)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
