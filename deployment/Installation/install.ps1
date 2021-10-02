[CmdletBinding()]
Param(

    [string] 
    [Parameter(Mandatory=$true)]
    $ResourceGroupName,

    [string] 
    $ResourceLocation = "westeurope",

    [string] 
    [Parameter(Mandatory=$true)]
    $TemplateFile,

    [string] 
    [Parameter(Mandatory=$true)]
    $TemplateParameterFile
)

Function CreateResourceGroup() {
   
    param(

        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]$ResourceGroupName,

        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]$ResourceLocation
    )
    
    $ResourceGroup = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue
    if (-not($ResourceGroup)) {
        Write-Verbose "Creating resource group $ResourceGroupName"
        $ResourceGroup = New-AzResourceGroup -Name $ResourceGroupName -Location $ResourceLocation 
    }
    else {
        Write-Verbose "Resource group $ResourceGroupName found"
    }
    return $ResourceGroup
}

CreateResourceGroup -ResourceGroupName $ResourceGroupName -ResourceLocation $ResourceLocation 
$outputs = (New-AzResourceGroupDeployment -ResourceGroupName $ResourceGroupName -TemplateFile $TemplateFile -TemplateParameterFile $TemplateParameterFile).Outputs
$qnaHostEndpoint = $outputs.qnaHostEndpoint.value

"##vso[task.setvariable variable=qnaHostEndpoint;]$qnaHostEndpoint"
