#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI Pre-Commit Hook

A pre-commit hook that uses OpenAI to check for obvious errors in your code.
"""

import argparse
import os
import subprocess
import sys
from typing import List, Optional, Dict, Any

try:
    from openai import OpenAI
    from colorama import Fore, Style, init
except ImportError:
    print("Error: Required packages are missing. Please run 'pip install -r requirements.txt'")
    sys.exit(1)

# Initialize colorama
init()

DEFAULT_MODEL = "gpt-4o"
DEFAULT_PROMPT = """
You are a code reviewer. Analyze the following code changes and identify any obvious errors, bugs, 
or security issues. Only report serious issues that would prevent the code from working correctly.
If no serious issues are found, respond with "PASS".

Below are the code changes:
{code_changes}
"""


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="AI Pre-Commit Hook")
    parser.add_argument("--api-key", type=str, help="OpenAI API key")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="OpenAI model to use")
    parser.add_argument("--prompt", type=str, help="Custom prompt to use for checking errors")
    
    return parser.parse_args()


def get_staged_files() -> List[str]:
    """Get list of staged files for commit."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [file for file in result.stdout.splitlines() if os.path.exists(file)]


def get_file_diff(file_path: str) -> str:
    """Get the diff for a specific file."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--", file_path],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def check_code_with_openai(
    api_key: str, model: str, code_changes: str, prompt_template: str
) -> Dict[str, Any]:
    """Check code changes using OpenAI API."""
    client = OpenAI(api_key=api_key)
    
    prompt = prompt_template.format(code_changes=code_changes)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a code reviewer that identifies obvious errors."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )
    
    return {
        "message": response.choices[0].message.content,
        "pass": "PASS" in response.choices[0].message.content,
    }


def main():
    """Main function for the pre-commit hook."""
    args = parse_args()
    
    # Get API key from args or environment variable
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(f"{Fore.RED}Error: OpenAI API key is required{Style.RESET_ALL}")
        print("Set it using --api-key or OPENAI_API_KEY environment variable")
        sys.exit(1)
    
    # Get model from args or environment variable
    model = args.model or os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
    
    # Get prompt from args or environment variable or use default
    prompt_template = args.prompt or os.environ.get("OPENAI_PROMPT", DEFAULT_PROMPT)
    
    # Get staged files
    staged_files = get_staged_files()
    if not staged_files:
        print(f"{Fore.GREEN}No staged files to check{Style.RESET_ALL}")
        sys.exit(0)
    
    print(f"{Fore.CYAN}Checking {len(staged_files)} staged files with OpenAI{Style.RESET_ALL}")
    
    # Get diffs for all staged files
    all_diffs = ""
    for file_path in staged_files:
        diff = get_file_diff(file_path)
        if diff:
            all_diffs += f"File: {file_path}\n{diff}\n\n"
    
    if not all_diffs:
        print(f"{Fore.GREEN}No changes to check{Style.RESET_ALL}")
        sys.exit(0)
    
    try:
        # Check code with OpenAI
        result = check_code_with_openai(api_key, model, all_diffs, prompt_template)
        
        if result["pass"]:
            print(f"{Fore.GREEN}OpenAI check passed{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}OpenAI found potential issues:{Style.RESET_ALL}")
            print(result["message"])
              # Ask user if they want to proceed with the commit
            response = input(f"{Fore.YELLOW}Do you want to proceed with the commit anyway? (y/N): {Style.RESET_ALL}")
            if response.lower() == "y":
                print(f"{Fore.YELLOW}Proceeding with commit despite issues{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Commit aborted{Style.RESET_ALL}")
                sys.exit(1)
    
    except Exception as e:
        print(f"{Fore.RED}Error checking code with OpenAI: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Proceeding with commit without OpenAI check{Style.RESET_ALL}")
        sys.exit(0)


if __name__ == "__main__":
    main()

# Export main functions to make this file usable as a module
__all__ = [
    "check_code_with_openai", 
    "get_staged_files", 
    "get_file_diff", 
    "parse_args", 
    "main"
]
