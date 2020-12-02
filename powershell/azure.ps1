# Take in user parameter from the command line
param (
    [string]$user = ""
)

Import-Module AzureAD

# Get configuration
$config = Get-Content -Raw -Path 'config.json' | ConvertFrom-Json

# User account details for account with global administrator privileges.
$user_email = $config.azure_email
$password = $config.azure_password
$password_secure = $password | ConvertTo-SecureString -AsPlainText -Force
$credentials = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $user_email, $password_secure

# Tenant ID
$tenant_id = $config.tenant_id

# Set session to utilise Tls 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Connect to Azure Active Directory
Connect-AzureAD -Credential $credentials -TenantId $tenant_id

# Handle user
if (!($user -eq "")) {

    $user_object = Get-AzureADUser -SearchString $user 
    Set-AzureADUser -ObjectId $user_object.objectId -AccountEnabled 0
    $user_object | Revoke-AzureADUserAllRefreshToken

    $telephone_number = $user_object.telephoneNumber
    $mobile = $user_object.mobile

    Write-Host $mobile ',' $telephone_number

}

Disconnect-AzureAD