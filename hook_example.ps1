# Example of how to call the AI pre-commit script from PowerShell
# This script demonstrates how to use the AI pre-commit hook in your own PowerShell scripts

# Set your OpenAI API key
$env:OPENAI_API_KEY = "your-api-key-here"
$env:OPENAI_MODEL = "gpt-4o"

# Function to check staged files with AI
function Check-WithAI {
    # Get the location of this script
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    
    # Run the AI pre-commit check
    python "$scriptDir\ai_pre_commit.py"
    return $LASTEXITCODE
}

# Example of how to use in a pre-commit hook
function Run-Checks {
    Write-Host "Running other checks..." -ForegroundColor Cyan
    # Add your other checks here
    # ...
    
    Write-Host "Running AI code quality check..." -ForegroundColor Cyan
    Check-WithAI
    $aiResult = $LASTEXITCODE
    
    if ($aiResult -ne 0) {
        Write-Host "AI check failed, aborting commit" -ForegroundColor Red
        return 1
    }
    
    Write-Host "All checks passed!" -ForegroundColor Green
    return 0
}

# Run all checks
$result = Run-Checks
exit $result
