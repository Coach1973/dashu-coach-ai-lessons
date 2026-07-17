# Full junction/reparse-point chain checker.
# Built 2026-07-17 after case 51 (Zoom E-drive junction misjudged as "not linked").
#
# The bug this fixes: checking only a folder's CHILDREN for ReparsePoint status
# tells you nothing, because a junction set at the PARENT level is transparent --
# everything underneath looks like a normal file/folder. You must check the
# folder itself (and every ancestor, if unsure) before concluding "not linked".
#
# Usage:
#   powershell -File check_full_junction_chain.ps1 -Path "C:\Users\bymyw\AppData\Roaming\Zoom"
#
# Prints, for the given path and every folder below it, whether it is itself
# a reparse point (Junction/SymbolicLink) and its target. Use this before any
# "this data isn't linked elsewhere, safe to delete" conclusion.

param(
    [Parameter(Mandatory=$true)]
    [string]$Path
)

function Test-ReparsePoint($item) {
    return (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
}

if (-not (Test-Path -LiteralPath $Path)) {
    Write-Output "Path does not exist: $Path"
    exit 1
}

$root = Get-Item -LiteralPath $Path -Force
$rootIsLink = Test-ReparsePoint $root
Write-Output "SELF  | $Path | IsReparsePoint=$rootIsLink$(if ($rootIsLink) { ' | LinkType=' + $root.LinkType + ' | Target=' + $root.Target })"

if ($rootIsLink) {
    Write-Output "STOP: the path itself is a link. Everything below is transparently redirected -- do not judge 'linked or not' from children alone."
    exit 0
}

Get-ChildItem -LiteralPath $Path -Recurse -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
    $isLink = Test-ReparsePoint $_
    if ($isLink) {
        Write-Output "CHILD | $($_.FullName) | IsReparsePoint=True | LinkType=$($_.LinkType) | Target=$($_.Target)"
    }
}

Write-Output "Done. If nothing but SELF printed above, no junctions found at any level under $Path."
