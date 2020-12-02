# Set file directory for User Logs
$filedir = "\\WIN-D4LB6HM1EEM\Logs\"

# Get current session details, including username, machine name and session ID.
$username = $env:USERNAME
$computer = $env:COMPUTERNAME
$session = ((quser | Where-Object { $_ -match $username.ToLower() }) -split ' +')[2]

# Check if file with users name exists on shared directory, create if not.
$file = "${filedir}${username}.txt"
if ([System.IO.File]::Exists($file)) {

    $linenumber = (Select-String -Path $file -Pattern "${computer} - ${session}").LineNumber
    if ($linenumber) {

        $content = Get-Content -Path $file
        if ($content.GetType().Name -eq "Object[]") {
            $line = $content[$linenumber]
            $content | Where-Object { $_ -ne $line } | Out-File $file    
        } elseif ($content.GetType().Name -eq "String") {
            $content = ""
            $content | Set-Content $file
        } else {
            Write-Output "The contents of this file are unrecognised."
        }

    } 

}