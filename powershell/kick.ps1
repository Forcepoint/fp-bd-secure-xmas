# Get username from command line
$username = $args[0]

# Set file directory for User Logs
$filedir = "\\WIN-D4LB6HM1EEM\Logs\"
$file = "${filedir}${username}.txt"

if ([System.IO.File]::Exists($file)) {

    $contents = Get-Content -Path $file
    
    foreach ($line in $contents) {

        $splitline = $line -split " - "
        $machine = $splitline[0]
        $session = $splitline[1]

        if ($machine -and $session) {

            logoff $session /server:$machine

        }

    }

    $contents = ""
    $contents | Set-Content $file

} else {

    Write-Output "There was no file for the specified user."

}

