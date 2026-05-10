# NemoClaw: Advanced Secure GKE Sandbox Baseline

# --- GKE Sandbox (gVisor) Config ---
resource "google_container_node_pool" "nemoclaw_sandbox" {
  name       = "nemoclaw-secure-runtime"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {
    machine_type = "n2-standard-4"
    
    # Enable gVisor Sandbox
    sandbox_config {
      sandbox_type = "gvisor"
    }

    # Enable Confidential Computing
    confidential_nodes {
      enabled = true
    }

    # Shielded Nodes
    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    # Workload Identity
    workload_metadata_config {
      mode = "GKE_METADATA"
    }
  }
}

# --- KMS Key for Agent Workspace ---
resource "google_kms_crypto_key" "agent_vault" {
  name     = "nemoclaw-agent-vault"
  key_ring = google_kms_key_ring.ring.id
  purpose  = "ENCRYPT_DECRYPT"
}
