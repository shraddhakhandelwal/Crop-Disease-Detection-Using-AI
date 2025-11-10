# Helper script to build and run the TF-base docker-compose service on Windows PowerShell
# Usage: Run this file from the project root in PowerShell (may require Administrator privileges for Docker).

Write-Host "Building and starting TF-base service (web_tfbase)..."
docker-compose up -d --build web_tfbase
Write-Host "Service started. View logs with: docker-compose logs -f web_tfbase"
