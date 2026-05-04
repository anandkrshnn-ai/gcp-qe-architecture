module "vpc" {
  source      = "../../modules/vpc"
  environment = var.environment
  region      = var.region
}

module "gke" {
  source      = "../../modules/gke"
  project_id  = var.project_id
  environment = var.environment
  region      = var.region
  vpc_id      = module.vpc.vpc_id
  subnet_id   = module.vpc.subnet_id
}

module "cloud_run" {
  source      = "../../modules/cloud-run"
  environment = var.environment
  region      = var.region
}

module "cloud_sql" {
  source      = "../../modules/cloud-sql"
  environment = var.environment
  region      = var.region
}

module "slo_monitoring" {
  source               = "../../../slo-monitoring"
  notification_channel = "projects/${var.project_id}/notificationChannels/${var.environment}-alerts"
}

output "cloud_run_url" {
  value = module.cloud_run.service_url
}

variable "project_id" { type = string }
variable "environment" { default = "staging" }
variable "region" { default = "asia-south1" }
