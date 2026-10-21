#!/usr/bin/env bash
# ==============================================================================
# IBM Cloud Code Engine Deployment Automation Script
# Project: Cars Dealership Full-Stack Capstone
# ==============================================================================
set -e

APP_NAME="dealership-capstone-app"
PROJECT_NAME="dealership-capstone"
RESOURCE_GROUP="Default"
REGION="us-south"
PORT="8000"

echo "=== IBM Cloud Code Engine Deployment Script ==="

# Check CLI prerequisites
if ! command -v ibmcloud &> /dev/null; then
    echo "ERROR: 'ibmcloud' CLI is not installed."
    echo "Install it via: curl -fsSL https://clis.cloud.ibm.com/install/linux | sh"
    exit 1
fi

echo "1. Checking IBM Cloud login status..."
ibmcloud target || {
    echo "Please log in: ibmcloud login -u <YOUR_EMAIL> --sso"
    exit 1
}

echo "2. Targeting resource group '${RESOURCE_GROUP}' and region '${REGION}'..."
ibmcloud target -g "${RESOURCE_GROUP}" -r "${REGION}"

echo "3. Ensuring Code Engine plugin is installed..."
ibmcloud plugin install code-engine -f

echo "4. Creating or targeting Code Engine project '${PROJECT_NAME}'..."
if ! ibmcloud ce project get --name "${PROJECT_NAME}" &> /dev/null; then
    echo "Creating project ${PROJECT_NAME}..."
    ibmcloud ce project create --name "${PROJECT_NAME}"
fi
ibmcloud ce project select --name "${PROJECT_NAME}"

echo "5. Building and deploying container application '${APP_NAME}'..."
if ibmcloud ce application get --name "${APP_NAME}" &> /dev/null; then
    echo "Updating existing application..."
    ibmcloud ce application update --name "${APP_NAME}" \
        --build-source . \
        --port "${PORT}" \
        --env DEBUG=False \
        --env SECRET_KEY="django-insecure-capstone-prod-key"
else
    echo "Creating new application..."
    ibmcloud ce application create --name "${APP_NAME}" \
        --build-source . \
        --port "${PORT}" \
        --env DEBUG=False \
        --env SECRET_KEY="django-insecure-capstone-prod-key"
fi

echo "6. Retrieving application public URL..."
DEPLOY_URL=$(ibmcloud ce application get --name "${APP_NAME}" --output url)
echo "======================================================================="
echo "Application successfully deployed to IBM Cloud Code Engine!"
echo "Live Public URL: ${DEPLOY_URL}"
echo "======================================================================="
