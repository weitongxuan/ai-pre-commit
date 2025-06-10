# Install AI Pre-Commit Hook PowerShell Script

# Check if git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed. Please install Git and try again."
    exit 1
}

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed. Please install Python and try again."
    exit 1
}

# Check if current directory is a git repository
$isGitRepo = git rev-parse --is-inside-work-tree 2>$null
if (-not $isGitRepo) {
    Write-Error "Not a git repository. Please run this script from a git repository."
    exit 1
}

# Get git repository root
$gitRoot = git rev-parse --show-toplevel
$hooksDir = Join-Path $gitRoot ".git\hooks"

# Create hooks directory if it doesn't exist
if (-not (Test-Path $hooksDir)) {
    New-Item -ItemType Directory -Path $hooksDir -Force | Out-Null
}

# Get the source file
$scriptDir = $PSScriptRoot
$sourceFile = Join-Path $scriptDir "ai_pre_commit.py"
$destFile = Join-Path $hooksDir "pre-commit"

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r (Join-Path $scriptDir "requirements.txt")

# Copy the file
Write-Host "Copying $sourceFile to $destFile"
Copy-Item -Path $sourceFile -Destination $destFile -Force

# Ask for OpenAI API Key
$apiKey = Read-Host "Enter your OpenAI API Key (leave blank to skip)"

if ($apiKey) {
    # Set environment variable for current session
    $env:OPENAI_API_KEY = $apiKey
    
    # Ask if user wants to set it permanently
    $setPermanently = Read-Host "Do you want to set the API key permanently for your user? (y/N)"
    
    if ($setPermanently -eq "y") {
        [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $apiKey, "User")
        Write-Host "API key set permanently for your user."
    }
}

Write-Host "Installation successful!"
Write-Host "You can now use the AI pre-commit hook."
if (-not $apiKey) {
    Write-Host "Make sure to set your OpenAI API key using:"
    Write-Host "  $env:OPENAI_API_KEY = 'your-api-key'"
    Write-Host "or pass it as an argument when running the script."
}
