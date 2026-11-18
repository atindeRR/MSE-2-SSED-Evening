# Reproducible networking, health, and PostgreSQL-volume persistence verification.
# Run from the repository root after copying .env.example to .env and setting real values.
$ErrorActionPreference = 'Stop'

function Invoke-Compose {
  & docker compose @args
  if ($LASTEXITCODE -ne 0) { throw "docker compose $($args -join ' ') failed" }
}

$settings = @{}
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#=\s]+)\s*=\s*(.*)\s*$') { $settings[$matches[1]] = $matches[2] }
}
$postgresUser = $settings['POSTGRES_USER']
if (-not $postgresUser) { $postgresUser = 'taskflow_user' }
$postgresDatabase = $settings['POSTGRES_DB']
if (-not $postgresDatabase) { $postgresDatabase = 'taskflow' }

Invoke-Compose up -d
Invoke-Compose ps

Write-Host 'Checking frontend-to-backend reverse proxy:'
Invoke-RestMethod http://localhost:8080/health | ConvertTo-Json -Compress
Write-Host 'Checking backend health and its PostgreSQL/Redis connectivity:'
Invoke-RestMethod http://localhost:3000/health | ConvertTo-Json -Compress

Write-Host 'Inspecting the custom bridge network:'
docker network inspect taskflow_taskflow-network
if ($LASTEXITCODE -ne 0) { throw 'Unable to inspect taskflow_taskflow-network' }

Write-Host 'Checking PostgreSQL and Redis directly:'
Invoke-Compose exec -T postgres pg_isready -U $postgresUser -d $postgresDatabase
Invoke-Compose exec -T redis redis-cli ping

$marker = "persistence-$([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())"
Write-Host "Inserting persistence marker: $marker"
Invoke-Compose exec -T postgres psql -v ON_ERROR_STOP=1 -U $postgresUser -d $postgresDatabase -c 'CREATE TABLE IF NOT EXISTS persistence_checks (marker TEXT PRIMARY KEY);'
Invoke-Compose exec -T postgres psql -v ON_ERROR_STOP=1 -U $postgresUser -d $postgresDatabase -c "INSERT INTO persistence_checks (marker) VALUES ('$marker');"
Invoke-Compose exec -T postgres psql -U $postgresUser -d $postgresDatabase -c "SELECT marker FROM persistence_checks WHERE marker = '$marker';"

Write-Host 'Recreating only the PostgreSQL container; the named volume is retained.'
Invoke-Compose rm -sf postgres
Invoke-Compose up -d postgres
for ($attempt = 1; $attempt -le 30; $attempt++) {
  $containerId = (& docker compose ps -q postgres).Trim()
  $health = if ($containerId) { (& docker inspect -f '{{.State.Health.Status}}' $containerId).Trim() } else { '' }
  if ($health -eq 'healthy') { break }
  Start-Sleep -Seconds 2
  if ($attempt -eq 30) { throw 'PostgreSQL did not become healthy after recreation' }
}
Invoke-Compose exec -T postgres psql -U $postgresUser -d $postgresDatabase -c "SELECT marker FROM persistence_checks WHERE marker = '$marker';"

Write-Host 'Restarting Redis and confirming it returns PONG:'
Invoke-Compose restart redis
Invoke-Compose exec -T redis redis-cli ping
Write-Host 'Verification complete. No docker compose down -v command was used.'
