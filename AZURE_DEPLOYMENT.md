# Azure Static Web Apps Deployment Guide

## Steps to Deploy to Azure Static Web Apps:

### 1. Create Azure Static Web Apps Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Static Web Apps"
4. Click "Create"

### 2. Configure Deployment

**Basic Settings:**
- **Subscription**: Your Azure subscription
- **Resource Group**: Create new or use existing
- **Name**: `atos-chatbot-webapp` (or your preferred name)
- **Plan Type**: Free (for development/testing)
- **Region**: Choose closest to your users

**Deployment Details:**
- **Source**: GitHub
- **Organization**: `IN-PUN-COAONE-AUTOMATNSA`
- **Repository**: `copilot-websearch`
- **Branch**: `main`

**Build Details:**
- **Build Presets**: React
- **App location**: `/` (root)
- **Api location**: `` (leave empty)
- **Output location**: `build`

### 3. GitHub Integration

Azure will automatically:
- Create a GitHub secret `AZURE_STATIC_WEB_APPS_API_TOKEN`
- Update your repository with deployment workflow
- Trigger the first deployment

### 4. Domain Configuration (Optional)

After deployment, you can:
- Use the auto-generated domain (e.g., `https://gentle-hill-123abc.azurestaticapps.net`)
- Configure a custom domain if needed

### 5. Verification

1. Check the Actions tab in your GitHub repository
2. Verify the deployment workflow runs successfully
3. Visit your deployed URL to test the Copilot integration

## Troubleshooting

If deployment fails:
1. Check GitHub Actions logs
2. Verify the `AZURE_STATIC_WEB_APPS_API_TOKEN` secret exists
3. Ensure the workflow file matches the Azure configuration

## Security Notes

The `staticwebapp.config.json` file includes:
- Content Security Policy allowing Copilot Studio iframe
- Navigation fallback for single-page app routing
- Security headers for protection
