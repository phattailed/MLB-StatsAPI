$ErrorActionPreference = 'Stop'
$projRoot = Split-Path $PSScriptRoot -Parent
pip install -r "$projRoot/requirements.txt"
pip install -r "$projRoot/requirements-dev.txt"
