
# ------------------------------------------
# RESOURCE GROUP
# ------------------------------------------

# A resource group is a container that organizes
# all the Azure resources belonging to our project.
resource "azurerm_resource_group" "dwts_rg" {

  # Give the resource group a descriptive name.
  name = "rg-${var.project_name}-${var.environment}"

  # Choose which Azure region will host our resources.
  location = var.location

  # Add labels to help identify our resources.
  tags = {
    project     = var.project_name
    environment = var.environment
  }
}

# ------------------------------------------
# APP SERVICE PLAN
# ------------------------------------------

# An App Service Plan defines the computing resources
# available to our website, including its pricing tier.
resource "azurerm_service_plan" "dwts_plan" {

  # Name of the hosting plan.
  name = "plan-${var.project_name}-${var.environment}"

  # Place the plan inside our resource group.
  resource_group_name = azurerm_resource_group.dwts_rg.name

  # Use the same Azure region as the resource group.
  location = azurerm_resource_group.dwts_rg.location

  # Our Streamlit app will run on Linux.
  os_type = "Linux"

  # Use the Basic B1 pricing tier for our initial configuration.
  sku_name = "B1"

  tags = {
    project     = var.project_name
    environment = var.environment
  }
}


# ------------------------------------------
# LINUX WEB APP
# ------------------------------------------

# Create the Azure web application that will
# eventually run our Python Streamlit dashboard.
resource "azurerm_linux_web_app" "dwts_app" {

  # Azure web app names must be globally unique.
  name = "app-${var.project_name}-${var.environment}"

  # Put the website inside our existing resource group.
  resource_group_name = azurerm_resource_group.dwts_rg.name

  # Use the same Azure region.
  location = azurerm_resource_group.dwts_rg.location

  # Connect the website to our App Service Plan.
  service_plan_id = azurerm_service_plan.dwts_plan.id

  # Require secure HTTPS connections.
  https_only = true

  # Configure how our Python website will run.
  site_config {

    # Streamlit listens on port 8501 by default.
    app_command_line = "python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8000"

    # Use Python as the application runtime.
    application_stack {
      python_version = var.python_version
    }
  }

  # Environment variables used by Azure.
  app_settings = {

    # Tell Azure to install dependencies during deployment.
    SCM_DO_BUILD_DURING_DEPLOYMENT = "true"

    # Allow Azure's Python build system to run.
    ENABLE_ORYX_BUILD = "true"
  }

  # Add identifying tags.
  tags = {
    project     = var.project_name
    environment = var.environment
  }
}
