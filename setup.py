#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for AI Pre-Commit Hook.
This script installs the pre-commit hook to your git repository.
"""

import os
import shutil
import stat
import sys
import subprocess

def is_git_repository():
    """Check if current directory is a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False

def get_git_root():
    """Get the root directory of the git repository."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()

def main():
    """Main function for setup script."""
    # Check if current directory is a git repository
    if not is_git_repository():
        print("Error: Not a git repository. Please run this script from a git repository.")
        sys.exit(1)
    
    # Get git repository root
    git_root = get_git_root()
    
    # Create hooks directory if it doesn't exist
    hooks_dir = os.path.join(git_root, ".git", "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    
    # Get the source file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(script_dir, "ai_pre_commit.py")
    
    # Destination file
    dest_file = os.path.join(hooks_dir, "pre-commit")
    
    # Copy the file
    print(f"Copying {source_file} to {dest_file}")
    shutil.copy2(source_file, dest_file)
    
    # Make the file executable
    os.chmod(dest_file, os.stat(dest_file).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    
    print("Installation successful!")
    print("You can now use the AI pre-commit hook.")
    print("Make sure to set your OpenAI API key using:")
    print("  export OPENAI_API_KEY=\"your-api-key\"")
    print("or pass it as an argument:")
    print("  git commit --no-verify && OPENAI_API_KEY=\"your-api-key\" .git/hooks/pre-commit")

if __name__ == "__main__":
    main()
