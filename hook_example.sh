#!/bin/bash
# Example of how to call the AI pre-commit script from a bash script

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_MODEL="gpt-4o"

# Function to check staged files with AI
check_with_ai() {
  # Get the location of this script
  SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
  
  # Run the AI pre-commit check
  python "$SCRIPT_DIR/ai_pre_commit.py"
  return $?
}

# Example of how to use in a pre-commit hook
run_checks() {
  echo "Running other checks..."
  # Add your other checks here
  # ...
  
  echo "Running AI code quality check..."
  check_with_ai
  AI_RESULT=$?
  
  if [ $AI_RESULT -ne 0 ]; then
    echo "AI check failed, aborting commit"
    return 1
  fi
  
  echo "All checks passed!"
  return 0
}

# Run all checks
run_checks
exit $?
