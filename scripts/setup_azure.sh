#!/bin/bash

# Variables
RESOURCE_GROUP="crop-disease-rg"
LOCATION="eastus"
APP_NAME="crop-disease-detection"
SERVICE_PLAN="crop-disease-plan"

# Create resource group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create app service plan
echo "Creating app service plan..."
az appservice plan create --name $SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# Create web app
echo "Creating web app..."
az webapp create --resource-group $RESOURCE_GROUP --plan $SERVICE_PLAN --name $APP_NAME --runtime "PYTHON|3.11"

# Configure web app settings
echo "Configuring web app settings..."
az webapp config set --resource-group $RESOURCE_GROUP --name $APP_NAME --startup-file "python app.py"

# Create service principal for GitHub Actions
echo "Creating service principal..."
az ad sp create-for-rbac --name "crop-disease-github-actions" \
    --role contributor \
    --scopes /subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP \
    --json-auth

echo "Done! Copy the JSON output above and add it as a secret named AZURE_CREDENTIALS in your GitHub repository"
echo "Also add AZURE_WEBAPP_NAME=$APP_NAME as another secret"