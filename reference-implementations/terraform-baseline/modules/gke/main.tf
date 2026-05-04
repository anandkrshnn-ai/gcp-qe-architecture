resource "google_container_cluster" "primary" {
  name     = "${var.environment}-gke-cluster"
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = var.vpc_id
  subnetwork = var.subnet_id

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS"]
  }

  release_channel {
    channel = "REGULAR"
  }

  deletion_protection = false
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.environment}-primary-nodes"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = var.min_node_count

  node_config {
    machine_type = var.machine_type
    disk_size_gb = 100

    workload_metadata_config {
      mode = "GKE_METADATA"
    }
  }
}

variable "project_id" { type = string }
variable "environment" { type = string }
variable "region" { type = string }
variable "vpc_id" { type = string }
variable "subnet_id" { type = string }
variable "min_node_count" { default = 2 }
variable "machine_type" { default = "e2-medium" }

output "cluster_name" { value = google_container_cluster.primary.name }
output "cluster_endpoint" { value = google_container_cluster.primary.endpoint }
