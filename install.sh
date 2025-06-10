#!/bin/bash
# Install AI Pre-Commit Hook Bash Script

set -e

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed. Please install Git and try again."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if current directory is a git repository
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    echo "Error: Not a git repository. Please run this script from a git repository."
    exit 1
fi

# Get git repository root
GIT_ROOT=$(git rev-parse --show-toplevel)
HOOKS_DIR="${GIT_ROOT}/.git/hooks"

# Create hooks directory if it doesn't exist
mkdir -p "${HOOKS_DIR}"

# Get the source file
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_FILE="${SCRIPT_DIR}/ai_pre_commit.py"
DEST_FILE="${HOOKS_DIR}/pre-commit"

# Install dependencies
echo "Installing dependencies..."
pip3 install -r "${SCRIPT_DIR}/requirements.txt"

# Copy the file
echo "Copying ${SOURCE_FILE} to ${DEST_FILE}"
cp "${SOURCE_FILE}" "${DEST_FILE}"

# Make the file executable
chmod +x "${DEST_FILE}"

# Ask for OpenAI API Key
read -p "Enter your OpenAI API Key (leave blank to skip): " API_KEY

if [ -n "${API_KEY}" ]; then
    # Export environment variable for current session
    export OPENAI_API_KEY="${API_KEY}"
    
    # Ask if user wants to set it permanently
    read -p "Do you want to set the API key permanently in your .bashrc/.zshrc? (y/N): " SET_PERMANENTLY
    
    if [ "${SET_PERMANENTLY}" = "y" ]; then
        if [ -f "${HOME}/.zshrc" ]; then
            echo "export OPENAI_API_KEY=\"${API_KEY}\"" >> "${HOME}/.zshrc"
            echo "API key set in .zshrc. Restart your terminal or run 'source ~/.zshrc'."
        elif [ -f "${HOME}/.bashrc" ]; then
            echo "export OPENAI_API_KEY=\"${API_KEY}\"" >> "${HOME}/.bashrc"
            echo "API key set in .bashrc. Restart your terminal or run 'source ~/.bashrc'."
        else
            echo "Could not find .zshrc or .bashrc. You will need to set the API key manually."
        fi
    fi
fi

echo "Installation successful!"
echo "You can now use the AI pre-commit hook."
if [ -z "${API_KEY}" ]; then
    echo "Make sure to set your OpenAI API key using:"
    echo "  export OPENAI_API_KEY=\"your-api-key\""
    echo "or pass it as an argument when running the script."
fi
