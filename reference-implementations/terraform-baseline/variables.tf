variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Default region"
  type        = string
  default     = "asia-south1"
}

variable "environment" {
  description = "Environment name (dev/staging/prod)"
  type        = string
}
