variable "project_id" {
  type        = string
  description = "The GCP project ID"
}

variable "dashboard_name" {
  type        = string
  description = "The display name of the dashboard"
  default     = "Agent Safety & Governance Dashboard"
}
