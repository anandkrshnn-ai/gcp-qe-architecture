resource "google_cloud_run_service" "service" {
  name     = "${var.environment}-cloud-run"
  location = var.region

  template {
    spec {
      containers {
        image = var.container_image
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.service.name
  location = google_cloud_run_service.service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

variable "environment" { type = string }
variable "region" { type = string }
variable "container_image" { default = "us-docker.pkg.dev/cloudrun/container/hello" }

output "service_url" { value = google_cloud_run_service.service.status[0].url }
