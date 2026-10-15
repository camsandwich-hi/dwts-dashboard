
# ------------------------------------------
# AZURE SUBSCRIPTION
# ------------------------------------------

# Identifies which Azure subscription Terraform will use.
# We will supply the actual ID later.
variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
  sensitive   = true
}

# ------------------------------------------
# PROJECT SETTINGS
# ------------------------------------------

# A short name used when naming Azure resources.
variable "project_name" {
  description = "Name of our DWTS dashboard project"
  type        = string
  default     = "dwts-dashboard"
}

# The Azure region where our resources will be hosted.
variable "location" {
  description = "Azure region for our resources"
  type        = string
  default     = "centralus"
}

# Identifies whether we are using development or production.
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

# ------------------------------------------
# APPLICATION SETTINGS
# ------------------------------------------

# The Python version our Streamlit application will use.
variable "python_version" {
  description = "Python runtime version for our web app"
  type        = string
  default     = "3.12"
}
