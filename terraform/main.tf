# Root Terraform Configuration for NemoClaw on GCP

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Network
module "vpc" {
  source       = "./modules/vpc"
  network_name = "nemoclaw-net"
  subnet_name  = "nemoclaw-subnet"
  subnet_cidr  = "10.10.0.0/24"
  pod_cidr     = "10.100.0.0/16"
  service_cidr = "10.101.0.0/24"
  region       = var.region
}

# 2. IAM for Agents
module "iam" {
  source        = "./modules/iam"
  project_id    = var.project_id
  sa_name       = "sovereign-sre-agent"
  k8s_namespace = "nemoclaw"
  k8s_sa_name   = "sovereign-sre"
}

# 3. Hardened GKE Cluster
module "gke" {
  source                = "./modules/gke"
  project_id            = var.project_id
  cluster_name          = "nemoclaw-cluster"
  region                = var.region
  network_link          = module.vpc.network_link
  subnet_link           = module.vpc.subnet_link
  node_count            = 2
  service_account_email = module.iam.agent_sa_email
}
