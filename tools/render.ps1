# Exporta a PNG las plantillas y aplicaciones SVG usando Edge o Chrome en modo headless.
# Uso:  powershell -ExecutionPolicy Bypass -File tools\render.ps1 [-Only nombre]
param([string]$Only = "")

$root = Split-Path -Parent $PSScriptRoot
$browser = @(
  "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
  "C:\Program Files\Microsoft\Edge\Application\msedge.exe",
  "C:\Program Files\Google\Chrome\Application\chrome.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $browser) { throw "No se encontró Edge ni Chrome." }

$profile = Join-Path $env:TEMP "tpd-render-profile"
foreach ($dir in @("plantillas", "aplicaciones")) {
  $out = Join-Path $root "$dir\png"
  New-Item -ItemType Directory -Force $out | Out-Null
  Get-ChildItem (Join-Path $root $dir) -Filter *.svg | Where-Object { -not $Only -or $_.BaseName -eq $Only } | ForEach-Object {
    $head = Get-Content $_.FullName -TotalCount 1
    if ($head -notmatch 'width="(\d+)" height="(\d+)"') { Write-Warning "Sin tamaño: $($_.Name)"; return }
    $size = "$($Matches[1]),$($Matches[2])"
    $png = Join-Path $out ($_.BaseName + ".png")
    $url = "file:///" + ($_.FullName -replace '\\', '/')
    Start-Process -Wait $browser -ArgumentList '--headless=new', '--disable-gpu', '--hide-scrollbars',
      "--user-data-dir=$profile", "--window-size=$size", "--screenshot=$png", $url
    Write-Output "  $dir/png/$($_.BaseName).png ($size)"
  }
}
