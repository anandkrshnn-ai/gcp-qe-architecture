# Root Terraform Configuration for Agent Safety Patterns on GCP

provider "google" {
  project = var.project_id
  region  = var.region
}

# 0. Enable Required APIs
resource "google_project_service" "aiplatform" {
  project = var.project_id
  service = "aiplatform.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "logging" {
  project = var.project_id
  service = "logging.googleapis.com"
  disable_on_destroy = false
}

# 1. Network
module "vpc" {
  source       = "./modules/vpc"
  network_name = "agent-safety-net"
  subnet_name  = "agent-safety-subnet"
  subnet_cidr  = "10.10.0.0/24"
  pod_cidr     = "10.100.0.0/16"
  service_cidr = "10.101.0.0/24"
  region       = var.region
}

# 2. IAM for Agents
module "iam" {
  source        = "./modules/iam"
  project_id    = var.project_id
  sa_name       = "safety-sre-agent"
  k8s_namespace = "agent-safety-system"
  k8s_sa_name   = "safety-sre"
}

# 3. Hardened GKE Cluster
module "gke" {
  source                = "./modules/gke"
  project_id            = var.project_id
  cluster_name          = "agent-safety-cluster"
  region                = var.region
  network_link          = module.vpc.network_link
  subnet_link           = module.vpc.subnet_link
  node_count            = 2
  service_account_email = module.iam.agent_sa_email
  depends_on            = [google_project_service.aiplatform]
}

# 4. Observability Dashboards
module "monitoring" {
  source     = "./modules/monitoring"
  project_id = var.project_id
}
