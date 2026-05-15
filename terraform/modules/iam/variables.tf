variable "project_id" {
  type        = string
  description = "The GCP project ID"
}

variable "sa_name" {
  type        = string
  description = "Name of the service account"
}

variable "k8s_namespace" {
  type        = string
  description = "Kubernetes namespace"
}

variable "k8s_sa_name" {
  type        = string
  description = "Kubernetes service account name"
}
