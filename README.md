# MLB-StatsAPI

Python wrapper for MLB Stats API

Created by Todd Roberts

https://pypi.org/project/MLB-StatsAPI/

Issues: https://github.com/toddrob99/MLB-StatsAPI/issues

Wiki/Documentation: https://github.com/toddrob99/MLB-StatsAPI/wiki

## Copyright Notice

This package and its author are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.

## PowerShell Module

A simple PowerShell module is provided in `PowerShell/StatsApi` to expose
common functions from this library. It requires Python and this package to be
available on the system. Import the module and then call the functions:

```powershell
Import-Module ./PowerShell/StatsApi/StatsApi.psd1
$schedule = Get-MLBSchedule -Date "2024-05-01"
```

`Invoke-StatsApiFunction` can be used to access any other function by name.
