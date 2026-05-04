resource "google_compute_network" "vpc" {
  name                    = "${var.environment}-vpc"
  auto_create_subnetworks = false
  delete_default_routes_on_create = true
}

resource "google_compute_subnetwork" "private" {
  name                     = "${var.environment}-private-subnet"
  ip_cidr_range            = var.subnet_cidr
  region                   = var.region
  network                  = google_compute_network.vpc.id
  private_ip_google_access = true
}

variable "environment" { type = string }
variable "region" { type = string }
variable "subnet_cidr" { default = "10.0.0.0/20" }

output "vpc_id" { value = google_compute_network.vpc.id }
output "subnet_id" { value = google_compute_subnetwork.private.id }
output "vpc_name" { value = google_compute_network.vpc.name }
