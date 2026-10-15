
# ------------------------------------------
# TERRAFORM OUTPUTS
# ------------------------------------------

# Display the name of our Azure Resource Group.
output "resource_group_name" {
  description = "Name of the DWTS resource group"
  value       = azurerm_resource_group.dwts_rg.name
}

# Display the name of our Azure web application.
output "web_app_name" {
  description = "Name of the DWTS Streamlit web app"
  value       = azurerm_linux_web_app.dwts_app.name
}

# Display the public URL of our website.
output "web_app_url" {
  description = "URL for our deployed DWTS dashboard"
  value       = "https://${azurerm_linux_web_app.dwts_app.default_hostname}"
}
