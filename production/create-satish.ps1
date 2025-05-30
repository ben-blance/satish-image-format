# PowerShell script to create SATISH project structure
Write-Host "Creating SATISH Image Format Project Structure..." -ForegroundColor Cyan

# Create main project directory
New-Item -ItemType Directory -Name "satish-format" -Force
Set-Location "satish-format"

# Create root files
New-Item -ItemType File -Name "README.md" -Force
New-Item -ItemType File -Name "setup.py" -Force
New-Item -ItemType File -Name "requirements.txt" -Force

# Create main satish package
New-Item -ItemType Directory -Name "satish" -Force
Set-Location "satish"

New-Item -ItemType File -Name "__init__.py" -Force

# Create core module
New-Item -ItemType Directory -Name "core" -Force
Set-Location "core"

@("__init__.py", "format.py", "encoder.py", "decoder.py", "validator.py") | ForEach-Object {
    New-Item -ItemType File -Name $_ -Force
}

Set-Location ".."

# Create utils module
New-Item -ItemType Directory -Name "utils" -Force
Set-Location "utils"

@("__init__.py", "colors.py", "file_utils.py", "exceptions.py") | ForEach-Object {
    New-Item -ItemType File -Name $_ -Force
}

Set-Location ".."

# Create CLI module
New-Item -ItemType Directory -Name "cli" -Force
Set-Location "cli"

@("__init__.py", "commands.py", "main.py") | ForEach-Object {
    New-Item -ItemType File -Name $_ -Force
}

Set-Location ".."

# Go back to project root
Set-Location ".."

# Create tests directory
New-Item -ItemType Directory -Name "tests" -Force
Set-Location "tests"

New-Item -ItemType File -Name "__init__.py" -Force

# Create test_core subdirectory
New-Item -ItemType Directory -Name "test_core" -Force
Set-Location "test_core"

@("test_encoder.py", "test_decoder.py", "test_format.py") | ForEach-Object {
    New-Item -ItemType File -Name $_ -Force
}

Set-Location ".."

# Create test_utils subdirectory
New-Item -ItemType Directory -Name "test_utils" -Force
Set-Location "test_utils"

@("test_colors.py", "test_file_utils.py") | ForEach-Object {
    New-Item -ItemType File -Name $_ -Force
}

Set-Location ".."
Set-Location ".."

# Create examples directory
New-Item -ItemType Directory -Name "examples" -Force
Set-Location "examples"

@("basic_usage.py", "batch_convert.py", "custom_metadata.py") | ForEach-Object {
    New-Item -ItemType File -Name $_ -Force
}

Set-Location ".."

# Create docs directory
New-Item -ItemType Directory -Name "docs" -Force
Set-Location "docs"

@("format_spec.md", "api_reference.md", "examples.md") | ForEach-Object {
    New-Item -ItemType File -Name $_ -Force
}

Set-Location ".."

Write-Host ""
Write-Host "SATISH project structure created successfully!" -ForegroundColor Green
Write-Host ""

Write-Host "PROJECT STRUCTURE:" -ForegroundColor Yellow
tree /F

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. cd satish-format"
Write-Host "2. pip install Pillow"
Write-Host "3. Start implementing the modules"
Write-Host ""

# Optional: Show directory structure without tree command
function Show-DirectoryTree {
    param([string]$Path = ".", [int]$Indent = 0)

    $items = Get-ChildItem $Path | Sort-Object Name
    foreach ($item in $items) {
        $prefix = "  " * $Indent + "|-- "
        Write-Host "$prefix$($item.Name)"
        if ($item.PSIsContainer) {
            Show-DirectoryTree -Path $item.FullName -Indent ($Indent + 1)
        }
    }
}

Read-Host "Press Enter to continue..."
