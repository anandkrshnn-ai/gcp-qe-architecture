# Hardened Cloud Run Module

resource "google_cloud_run_v2_service" "default" {
  name     = var.service_name
  location = var.region

  template {
    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    containers {
      image = var.container_image
      
      resources {
        limits = {
          cpu    = var.cpu_limit
          memory = var.memory_limit
        }
      }

      # Hardened Concurrency
      max_instance_request_concurrency = var.concurrency

      startup_probe {
        initial_delay_seconds = 5
        timeout_seconds       = 1
        period_seconds        = 3
        failure_threshold     = 3
        tcp_socket {
          port = 8080
        }
      }

      liveness_probe {
        http_get {
          path = "/health"
        }
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

variable "service_name" { type = string }
variable "region" { default = "asia-south1" }
variable "min_instances" { default = 0 }
variable "max_instances" { default = 10 }
variable "cpu_limit" { default = "1000m" }
variable "memory_limit" { default = "512Mi" }
variable "concurrency" { default = 80 }
variable "container_image" { type = string }
