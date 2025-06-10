# AI Pre-Commit Hook

A pre-commit hook that uses OpenAI to check for obvious errors in your code.

## Installation Options

### Option 1: Standalone Pre-commit Hook

1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Copy the script to your `.git/hooks` directory and rename it to `pre-commit`:
```bash
cp ai_pre_commit.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Option 2: Install as a Python Package

You can install this tool as a Python package, which makes it available system-wide:

```bash
# Install from local directory
pip install -e .

# Or install directly from GitHub
pip install git+https://github.com/yourusername/ai-pre-commit.git
```

Then use it in your pre-commit hook:

```bash
#!/bin/bash
ai-pre-commit --api-key "your-api-key" --model "gpt-4o"
```

### Option 3: Integrate with Existing Pre-commit Hook

If you already have a pre-commit hook, you can call this script from your existing hook:

1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Copy the script to your repository:
```bash
cp ai_pre_commit.py /path/to/your/repo/scripts/ai_pre_commit.py
```

3. Add this to your existing `.git/hooks/pre-commit` file:
```bash
#!/bin/bash

# Run your existing pre-commit checks
# ...

# Run AI code check
python /path/to/your/repo/scripts/ai_pre_commit.py --api-key "your-api-key" --model "gpt-4o"

# If AI check fails, exit with its exit code
AI_EXIT_CODE=$?
if [ $AI_EXIT_CODE -ne 0 ]; then
    exit $AI_EXIT_CODE
fi

# Continue with your existing pre-commit hook
# ...
```

### Option 3: Using pre-commit Framework

If you're using the [pre-commit framework](https://pre-commit.com/), add this to your `.pre-commit-config.yaml`:

```yaml
# Local repo option (if installed as a package)
- repo: local
  hooks:
    - id: ai-code-check
      name: AI Code Check
      entry: ai-pre-commit
      language: system
      pass_filenames: false
      always_run: true
      # Optionally specify args
      args: [--api-key, "your-api-key", --model, "gpt-4o"]
      # Or use environment vars instead of args
      # env:
      #   OPENAI_API_KEY: "your-api-key"
      #   OPENAI_MODEL: "gpt-4o"

# OR - Direct from Git repository
- repo: https://github.com/yourusername/ai-pre-commit
  rev: v0.1.0  # Use specific tag/revision
  hooks:
    - id: ai-pre-commit
      # args and env can be specified here as well
```

### Option 4: Using Husky (for JavaScript/TypeScript projects)

For JavaScript/TypeScript projects using [Husky](https://typicode.github.io/husky/), add this to your `.husky/pre-commit` file:

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run your other checks
npm test

# Run AI code check
ai-pre-commit --api-key "your-api-key" --model "gpt-4o"
```

## Usage

You can configure the hook by setting environment variables or passing command-line arguments:

```bash
# Using environment variables
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL="gpt-4o"

# Or using command-line arguments
pre-commit --api-key "your-api-key" --model "gpt-4o" --prompt "Your custom prompt"
```

## Configuration

- `--api-key`: Your OpenAI API key
- `--model`: The OpenAI model to use (default: gpt-4o)
- `--prompt`: (Optional) Custom prompt to use for checking errors

## Using as a Module in Your Code

You can also import and use the AI code checker in your own Python scripts:

```python
from ai_pre_commit import check_code_with_openai

# Your code to get changes
code_changes = "..."

# Define your custom prompt (optional)
prompt_template = """
Analyze the following code changes and identify any obvious errors.
If no issues are found, respond with "PASS".

{code_changes}
"""

# Check code with OpenAI
result = check_code_with_openai(
    api_key="your-api-key", 
    model="gpt-4o", 
    code_changes=code_changes, 
    prompt_template=prompt_template
)

if result["pass"]:
    print("Code check passed!")
else:
    print("Issues found:", result["message"])
```

## How it works

The hook will:
1. Get the staged files
2. Extract the changes from those files
3. Send the changes to OpenAI API for analysis
4. Block the commit if obvious errors are found
