variable "project_id" {
  type        = string
  description = "The GCP project ID"
}

variable "cluster_name" {
  type        = string
  description = "The name of the GKE cluster"
}

variable "region" {
  type        = string
  description = "The GCP region"
}

variable "network_link" {
  type        = string
  description = "The VPC network link"
}

variable "subnet_link" {
  type        = string
  description = "The subnet link"
}

variable "node_count" {
  type        = number
  description = "Number of nodes"
  default     = 1
}

variable "service_account_email" {
  type        = string
  description = "The service account email for the nodes"
}
