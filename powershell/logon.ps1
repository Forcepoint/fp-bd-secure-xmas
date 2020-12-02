# Set file directory for User Logs
$filedir = "\\WIN-D4LB6HM1EEM\Logs\"

# Get current session details, including username, machine name and session ID.
$username = $env:USERNAME
$computer = $env:COMPUTERNAME
$session = ((quser | Where-Object { $_ -match $username.ToLower() }) -split ' +')[2]

# Check if file with users name exists on shared directory, create if not.
$file = "${filedir}${username}.txt"
if ([System.IO.File]::Exists($file)) { 
    
    $linenumber = (Select-String -Path $file -Pattern $computer).LineNumber
    if ($linenumber) {

        # If computer already logged on replace line
        $content = Get-Content $file

        if ($content.GetType().Name -eq "Object[]") {
            $content[[int]$linenumber] = "${computer} - ${session}"
        } elseif ($content.GetType().Name -eq "String") {
            $content = "${computer} - ${session}"
        } else {
            Write-Output "The contents of this file are unrecognised."
        }

        $content | Set-Content $file

    } else {

        # Else entry does not exist, write entry
        Add-Content $file "${computer} - ${session}"

    }
    
} else {

    New-Item -Path $filedir -Name "${username}.txt" -ItemType "file" -Value "${computer} - ${session}"

}