# Requires Git for Windows. Create an empty repository ONN9IX/project-analyst-portfolio first.
$ErrorActionPreference = "Stop"
$repo = "https://github.com/ONN9IX/project-analyst-portfolio.git"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
if (-not (Test-Path "README.md") -or -not (Test-Path "data/github_issues_snapshot.csv")) {
  throw "Запускай скрипт только из распакованной папки project-analyst-portfolio"
}
if (Test-Path ".git") {
  throw "Здесь уже есть Git-репозиторий. Проверь origin вручную, скрипт повторно не запускай."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Установи Git for Windows" }
git init
git branch -M main
git add .
git commit -m "Initial Project Analyst portfolio with verified GitHub snapshot"
git remote add origin $repo
git push -u origin main
Write-Host "Готово: https://github.com/ONN9IX/project-analyst-portfolio"
