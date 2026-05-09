# Global Variables
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

# VPC Variables
variable "network_name" { type = string }
variable "subnet_name" { type = string }
variable "subnet_cidr" { type = string }
variable "pod_cidr" { type = string }
variable "service_cidr" { type = string }

# GKE Variables
variable "cluster_name" { type = string }
variable "node_count" { type = number }
variable "network_link" { type = string }
variable "subnet_link" { type = string }
variable "service_account_email" { type = string }

# IAM Variables
variable "sa_name" { type = string }
variable "k8s_namespace" { type = string }
variable "k8s_sa_name" { type = string }
