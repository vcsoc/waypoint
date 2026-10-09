# Parallel Waypoint Health Check Runner (PowerShell version)
#
# This script runs multiple health check containers in parallel.
#
# Usage:
#   $env:WAYPOINT_BASE_URL="https://litellm.example.com"
#   $env:WAYPOINT_API_KEY="<your-virtual-key>"
#   .\run_parallel_health_checks.ps1 [num_parallel_jobs] [image_name]
#
# Defaults:
#   - num_parallel_jobs: 16
#   - image_name: waypoint/waypoint-health-check:latest

param(
    [int]$NumParallelJobs = 16,
    [string]$ImageName = "waypoint/waypoint-health-check:latest",
    [string]$ContainerRuntime = "docker"
)

# Require credentials for the target proxy
if (-not $env:WAYPOINT_BASE_URL) {
    $env:WAYPOINT_BASE_URL = "https://litellm-perf-cache-and-router.onrender.com"
    Write-Warning "WAYPOINT_BASE_URL not set, using default: $env:WAYPOINT_BASE_URL"
}

if (-not $env:WAYPOINT_API_KEY) {
    throw "WAYPOINT_API_KEY must be set"
}

# Check if container runtime is available
$runtimeExists = Get-Command $ContainerRuntime -ErrorAction SilentlyContinue
if (-not $runtimeExists) {
    Write-Error "Error: $ContainerRuntime is not installed"
    exit 1
}

Write-Host "Running $NumParallelJobs parallel health check containers..." -ForegroundColor Yellow
Write-Host "Using image: $ImageName" -ForegroundColor Yellow
Write-Host "Container runtime: $ContainerRuntime" -ForegroundColor Yellow
Write-Host "Waypoint Base URL: $env:WAYPOINT_BASE_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTE: This will run continuously. Press Ctrl+C to stop." -ForegroundColor Red
Write-Host ""
Write-Host "Troubleshooting:" -ForegroundColor Yellow
Write-Host "  - If you see 'All connection attempts failed', check:" -ForegroundColor Yellow
Write-Host "    1. Is the Waypoint proxy running on the expected port?" -ForegroundColor Yellow
Write-Host "    2. Set WAYPOINT_BASE_URL to the correct URL (e.g., http://host.docker.internal:PORT)" -ForegroundColor Yellow
Write-Host "    3. On Linux, you may need to use the host IP instead of host.docker.internal" -ForegroundColor Yellow
Write-Host ""

# Capture environment variables in parent scope for use in parallel block
$baseUrl = $env:WAYPOINT_BASE_URL
$apiKey = $env:WAYPOINT_API_KEY
$customAuthHeader = $env:WAYPOINT_CUSTOM_AUTH_HEADER

# Run parallel health checks
# This creates an infinite loop that keeps spawning containers
# Each container tests all models, then exits, and a new one starts
while ($true) {
    # Start up to NumParallelJobs containers in parallel
    1..$NumParallelJobs | ForEach-Object -Parallel {
        $runtime = $using:ContainerRuntime
        $imageName = $using:ImageName
        $baseUrl = $using:baseUrl
        $apiKey = $using:apiKey
        $customAuthHeader = $using:customAuthHeader
        
        $envVars = @(
            "-e", "WAYPOINT_BASE_URL=$baseUrl",
            "-e", "WAYPOINT_API_KEY=$apiKey",
            "-e", "WAYPOINT_JSON_OUTPUT=true"
        )
        
        if ($customAuthHeader) {
            $envVars += "-e", "WAYPOINT_CUSTOM_AUTH_HEADER=$customAuthHeader"
        }
        
        & $runtime run --rm $envVars $imageName
    } -ThrottleLimit $NumParallelJobs
}
