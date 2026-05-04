resource "google_sql_database_instance" "main" {
  name             = "${var.environment}-cloudsql"
  database_version = "POSTGRES_16"
  region           = var.region

  settings {
    tier              = var.db_tier
    availability_type = "REGIONAL"

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
    }

    ip_configuration {
      ipv4_enabled = true
    }
  }

  deletion_protection = false
}

variable "environment" { type = string }
variable "region" { type = string }
variable "db_tier" { default = "db-custom-2-8192" }

output "instance_name" { value = google_sql_database_instance.main.name }
output "connection_name" { value = google_sql_database_instance.main.connection_name }
