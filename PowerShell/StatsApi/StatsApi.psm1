function Invoke-StatsApiFunction {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$FunctionName,
        [Hashtable]$Parameters = @{},
        [string]$PythonPath = "python"
    )

    $json = $Parameters | ConvertTo-Json -Compress
    $script = Join-Path $PSScriptRoot 'pswrapper.py'
    $output = & $PythonPath $script $FunctionName --params $json 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "statsapi call failed: $output"
    }
    if ($output) {
        return $output | ConvertFrom-Json
    }
}

function Get-MLBSchedule {
    [CmdletBinding()]
    param(
        [string]$Date,
        [string]$StartDate,
        [string]$EndDate,
        [string]$Team,
        [string]$Opponent,
        [int]$SportId = 1,
        [int]$GameId,
        [string]$LeagueId,
        [string]$Season,
        [switch]$IncludeSeriesStatus
    )
    $params = @{}
    if ($PSBoundParameters.ContainsKey('Date')) { $params['date'] = $Date }
    if ($PSBoundParameters.ContainsKey('StartDate')) { $params['start_date'] = $StartDate }
    if ($PSBoundParameters.ContainsKey('EndDate')) { $params['end_date'] = $EndDate }
    if ($PSBoundParameters.ContainsKey('Team')) { $params['team'] = $Team }
    if ($PSBoundParameters.ContainsKey('Opponent')) { $params['opponent'] = $Opponent }
    if ($PSBoundParameters.ContainsKey('SportId')) { $params['sportId'] = $SportId }
    if ($PSBoundParameters.ContainsKey('GameId')) { $params['game_id'] = $GameId }
    if ($PSBoundParameters.ContainsKey('LeagueId')) { $params['leagueId'] = $LeagueId }
    if ($PSBoundParameters.ContainsKey('Season')) { $params['season'] = $Season }
    if ($IncludeSeriesStatus) { $params['include_series_status'] = $true }
    Invoke-StatsApiFunction -FunctionName 'schedule' -Parameters $params
}

function Get-MLBBoxscore {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [int]$GamePk,
        [string]$Timecode
    )
    $params = @{ 'gamePk' = $GamePk }
    if ($PSBoundParameters.ContainsKey('Timecode')) { $params['timecode'] = $Timecode }
    Invoke-StatsApiFunction -FunctionName 'boxscore' -Parameters $params
}

Export-ModuleMember -Function Invoke-StatsApiFunction, Get-MLBSchedule, Get-MLBBoxscore
