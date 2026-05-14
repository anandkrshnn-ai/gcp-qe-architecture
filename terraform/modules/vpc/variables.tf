variable "network_name" {
  type        = string
  description = "Name of the network"
}

variable "subnet_name" {
  type        = string
  description = "Name of the subnet"
}

variable "subnet_cidr" {
  type        = string
  description = "CIDR range for the subnet"
}

variable "pod_cidr" {
  type        = string
  description = "CIDR range for GKE pods"
}

variable "service_cidr" {
  type        = string
  description = "CIDR range for GKE services"
}

variable "region" {
  type        = string
  description = "GCP region"
}
