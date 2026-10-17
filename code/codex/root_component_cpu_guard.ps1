param(
    [Parameter(Mandatory=$true)][string]$Log,
    [int]$MaximumCores = 4
)
# All campaign workers share one affinity mask. Only our research Python
# process trees are changed; other applications are left to their owner.
$ErrorActionPreference = 'Stop'
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class C1CpuThreads {
  [DllImport("kernel32.dll", SetLastError=true)] public static extern IntPtr OpenThread(uint rights, bool inherit, uint id);
  [DllImport("kernel32.dll", SetLastError=true)] public static extern uint SuspendThread(IntPtr thread);
  [DllImport("kernel32.dll", SetLastError=true)] public static extern uint ResumeThread(IntPtr thread);
  [DllImport("kernel32.dll")] public static extern bool CloseHandle(IntPtr handle);
}
'@
$taskSuspended = @{}
function Resume-ResearchThreads($handles) {
    foreach ($handle in $handles.Values) {
        [void][C1CpuThreads]::ResumeThread($handle)
        [void][C1CpuThreads]::CloseHandle($handle)
    }
    $handles.Clear()
}
$taskPaused = $false
$taskPausedAt = [datetime]::MinValue
$taskStopFile = [System.IO.Path]::ChangeExtension($Log, '.stop')
$taskBudgetFile = [System.IO.Path]::ChangeExtension($Log, '.budget.json')
$taskBudget = 1
$taskLastIncrease = Get-Date
$taskLastSeen = Get-Date
$taskLastLog = [datetime]::MinValue
try { while ($true) {
    $taskNow = Get-Date
    $taskCpu = Get-CimInstance Win32_PerfFormattedData_Counters_ProcessorInformation |
        Where-Object { $_.Name -eq '_Total' } | Select-Object -First 1
    $taskUtility = if ($null -ne $taskCpu) { [double]$taskCpu.PercentProcessorUtility } else { 100.0 }
    $taskPrevious = $taskBudget
    if ($taskUtility -ge 65) {
        $taskBudget = 1; $taskLastIncrease = $taskNow
        if (-not $taskPaused) { $taskPausedAt = $taskNow; $taskPaused = $true }
    }
    elseif ($taskUtility -ge 60) { $taskBudget = [Math]::Max(1, $taskBudget - 1); $taskLastIncrease = $taskNow }
    elseif ($taskUtility -lt 45 -and ($taskNow - $taskLastIncrease).TotalSeconds -ge 30) {
        $taskBudget = [Math]::Min($MaximumCores, $taskBudget + 1)
        $taskLastIncrease = $taskNow
    }
    if ($taskPaused -and $taskUtility -lt 50 -and ($taskNow - $taskPausedAt).TotalSeconds -ge 15) {
        Resume-ResearchThreads $taskSuspended
        $taskPaused = $false
        $taskLastIncrease = $taskNow
    }
    $taskProcesses = @(Get-CimInstance Win32_Process -Filter "name='python.exe'")
    $taskIds = [System.Collections.Generic.HashSet[int]]::new()
    foreach ($taskProcess in $taskProcesses) {
        if ($taskProcess.CommandLine -match 'code[/\\]codex[/\\]root_component_') {
            [void]$taskIds.Add([int]$taskProcess.ProcessId)
        }
    }
    $taskExpanded = $true
    while ($taskExpanded) {
        $taskExpanded = $false
        foreach ($taskProcess in $taskProcesses) {
            if ($taskIds.Contains([int]$taskProcess.ParentProcessId) -and $taskIds.Add([int]$taskProcess.ProcessId)) {
                $taskExpanded = $true
            }
        }
    }
    $taskMask = ([int64]1 -shl $taskBudget) - 1
    foreach ($taskId in $taskIds) {
        try {
            $taskRunning = Get-Process -Id $taskId
            $taskRunning.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal
            $taskRunning.ProcessorAffinity = [IntPtr]$taskMask
            if ($taskPaused) {
                foreach ($taskThread in $taskRunning.Threads) {
                    $taskKey = "$taskId/$($taskThread.Id)"
                    if ($taskSuspended.ContainsKey($taskKey)) { continue }
                    $taskHandle = [C1CpuThreads]::OpenThread(2, $false, [uint32]$taskThread.Id)
                    if ($taskHandle -eq [IntPtr]::Zero) { continue }
                    $taskPriorCount = [C1CpuThreads]::SuspendThread($taskHandle)
                    if ($taskPriorCount -eq [uint32]::MaxValue) { [void][C1CpuThreads]::CloseHandle($taskHandle) }
                    else { $taskSuspended[$taskKey] = $taskHandle }
                }
            }
        } catch {
            # The worker can finish between the inventory and this update.
            if (Get-Process -Id $taskId -ErrorAction SilentlyContinue) {
                Add-Content -LiteralPath $Log -Value "resource_update_failed pid=$taskId error=$($_.Exception.Message)"
            }
        }
    }
    if ($taskIds.Count -gt 0) { $taskLastSeen = $taskNow }
    [pscustomobject]@{logical_cores=$taskBudget; paused=$taskPaused; time=$taskNow.ToString('o')} |
        ConvertTo-Json -Compress | Set-Content -LiteralPath $taskBudgetFile -Encoding UTF8
    if ($taskBudget -ne $taskPrevious -or ($taskNow - $taskLastLog).TotalSeconds -ge 15) {
        [pscustomobject]@{time=$taskNow.ToString('o'); cpu_utility=$taskUtility;
            shared_logical_cores=$taskBudget; owned_processes=$taskIds.Count; paused=$taskPaused} |
            ConvertTo-Json -Compress | Add-Content -LiteralPath $Log
        $taskLastLog = $taskNow
    }
    if (($taskNow - $taskLastSeen).TotalSeconds -gt 300 -or (Test-Path -LiteralPath $taskStopFile)) { break }
    Start-Sleep -Seconds 1
} } finally {
    Resume-ResearchThreads $taskSuspended
    [pscustomobject]@{logical_cores=$MaximumCores; paused=$false; stopped=$true; time=(Get-Date).ToString('o')} |
        ConvertTo-Json -Compress | Set-Content -LiteralPath $taskBudgetFile -Encoding UTF8
}
