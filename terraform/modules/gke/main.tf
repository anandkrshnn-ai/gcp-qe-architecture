# GKE Module for Secure Agentic Runtime Secure Runtime

resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.region

  # We use a separately managed node pool
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = var.network_link
  subnetwork = var.subnet_link

  networking_mode = "VPC_NATIVE"
  datapath_provider = "ADVANCED_DATAPATH" # Enable Cilium (Dataplane V2)

  enable_binary_authorization = true # Sovereign-Cloud: Only run signed images

  ip_allocation_policy {
    cluster_secondary_range_name  = "pod-range"
    services_secondary_range_name = "service-range"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false # Keep endpoint public for demo accessibility
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = "0.0.0.0/0" # WARNING: In production, restrict to your jumpbox/VPN
      display_name = "Allow All (Demo Only)"
    }
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }
}

resource "google_project_iam_member" "agent_vertex" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

# 2026 Enhancement: Managed MCP Server Access
resource "google_project_iam_member" "agent_alloydb_viewer" {
  project = var.project_id
  role    = "roles/alloydb.viewer"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

resource "google_container_node_pool" "agent_nodes" {
  name       = "agent-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count

  node_config {
    # 2026 Sovereign SRE Enhancement: GKE Sandbox (gVisor) for Agent Isolation
    sandbox_config {
      sandbox_type = "gvisor"
    }

    # Confidential GKE Nodes (SEV-SNP) for Hardware-Rooted Memory Encryption
    confidential_nodes {
      enabled = true
    }
    
    # Using G4 instances for high-efficiency Agentic compute
    machine_type = "g4-standard-4" 
    
    # Root disk hardening
    boot_disk_kms_key = "projects/${var.project_id}/locations/${var.region}/keyRings/sre-keys/cryptoKeys/boot-key"

    labels = {
      workload = "Secure Agentic Runtime-agent"
    }

    # Taint the nodes to ensure only agent workloads run here
    taint {
      key    = "workload"
      value  = "Secure Agentic Runtime-agent"
      effect = "NO_SCHEDULE"
    }

    service_account = var.service_account_email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    workload_metadata_config {
      mode = "GKE_METADATA"
    }
  }
}
