# Terraform GCP Baseline with Quality Gates
# This module sets up a secure project with monitoring enabled by default.

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Enable Critical Services for QE
resource "google_project_service" "services" {
  for_each = toset([
    "monitoring.googleapis.com",
    "cloudtrace.googleapis.com",
    "cloudprofiler.googleapis.com",
    "cloudbuild.googleapis.com"
  ])
  service = each.key
  disable_on_destroy = false
}

# 2. Monitoring Notification Channel (for SLO Breaches)
resource "google_monitoring_notification_channel" "email" {
  display_name = "QE Alert Channel"
  type         = "email"
  labels = {
    email_address = var.admin_email
  }
}

# 3. Uptime Check (Baseline Availability)
resource "google_monitoring_uptime_check_config" "https" {
  display_name = "Global Availability Check"
  timeout      = "10s"
  period       = "60s"

  http_check {
    path = "/"
    port = "443"
    use_ssl = true
  }

  monitored_resource {
    type = "uptime_url"
    labels = {
      project_id = var.project_id
      host       = var.target_host
    }
  }
}
