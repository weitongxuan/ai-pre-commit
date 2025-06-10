#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example of using AI Pre-Commit Hook as a module.
This shows how to use the AI pre-commit hook in your own Python code.
"""

import os
import sys
from ai_pre_commit import check_code_with_openai

def check_code_quality(code_snippet, api_key=None, model=None):
    """Check code quality using OpenAI."""
    # Get API key from args or environment variable
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is required")
    
    # Get model from args or environment variable
    model = model or os.environ.get("OPENAI_MODEL", "gpt-4o")
    
    # Define custom prompt
    prompt_template = """
    You are a code reviewer with expertise in software development.
    Analyze the following code and identify any obvious errors, bugs, 
    security issues, or performance problems.
    
    Only report serious issues that would prevent the code from working correctly
    or could cause problems in production.
    
    If no serious issues are found, respond with "PASS".
    
    Code to review:
    {code_changes}
    """
    
    # Check code with OpenAI
    result = check_code_with_openai(
        api_key=api_key,
        model=model,
        code_changes=code_snippet,
        prompt_template=prompt_template
    )
    
    return result

if __name__ == "__main__":
    # Example usage
    code_to_check = """
    def divide_numbers(a, b):
        return a / b  # Potential division by zero error
        
    def main():
        result = divide_numbers(10, 0)
        print(f"Result: {result}")
        
    if __name__ == "__main__":
        main()
    """
    
    try:
        result = check_code_quality(code_to_check)
        
        if result["pass"]:
            print("‚ú?Code check passed!")
            sys.exit(0)
        else:
            print("‚ù?Issues found:")
            print(result["message"])
            sys.exit(1)
            
    except Exception as e:
        print(f"Error checking code: {e}")
        sys.exit(1)
