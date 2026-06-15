targetScope = 'resourceGroup'

# Infrastructure template for the hybrid-channel
# It creates the App Service Plan, the Web App, and Application Insights inside
# the existing resource group

param location string = resourceGroup().location
param namePrefix string
param appServicePlanSkuName string = 'B1'
param linuxFxVersion string = 'PYTHON|3.11'

var appInsightsName = '${namePrefix}-appi'
var appServicePlanName = '${namePrefix}-plan'
var webAppName = '${namePrefix}-app'

# Application Insights resource used for logs, events, and metrics
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    RetentionInDays: 30
  }
}

# Compute layer that hosts the Linux App Service container
resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: appServicePlanSkuName
    tier: 'Basic'
    capacity: 1
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

# Main web application that runs FastAPI + uvicorn on port 8000
resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: linuxFxVersion
      # Explicit startup command so App Service imports the correct module path
      appCommandLine: 'python -m uvicorn server.app:app --host 0.0.0.0 --port 8000 --app-dir /home/site/wwwroot'
      alwaysOn: true
      appSettings: [
        {
          # App Service and uvicorn must agree on the exposed port
          name: 'WEBSITES_PORT'
          value: '8000'
        }
        {
          name: 'PORT'
          value: '8000'
        }
        {
          # Let Azure build the Python app during ZIP deployment
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          # Connection string for Application Insights telemetry from the server
          name: 'APPINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
        {
          # Instrumentation key kept for compatibility with older SDK usage
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
      ]
    }
  }
  dependsOn: [
    appInsights
    appServicePlan
  ]
}

output webAppDefaultHostname string = webApp.properties.defaultHostName
output applicationInsightsName string = appInsights.name
output applicationInsightsConnectionString string = appInsights.properties.ConnectionString
