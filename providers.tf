
# ------------------------------------------
# TERRAFORM CONFIGURATION
# ------------------------------------------

# Tell Terraform which providers our project requires.
terraform {
  required_providers {

    # Azure Resource Manager lets Terraform manage Azure resources.
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }

  # Require Terraform version 1.5 or newer.
  required_version = ">= 1.5.0"
}

# ------------------------------------------
# AZURE PROVIDER
# ------------------------------------------

# Configure the Azure provider.
# Resource-specific settings will come later.
provider "azurerm" {
  features {}

  # AzureRM 4.x requires a subscription ID.
  # We'll configure this when we connect our Azure account.
  subscription_id = var.subscription_id
}
