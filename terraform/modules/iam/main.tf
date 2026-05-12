# IAM Module for Safety SRE Agent

# 1. Create the GCP Service Account
resource "google_service_account" "agent_sa" {
  account_id   = var.sa_name
  display_name = "Secure Agentic Runtime Safety SRE Agent"
}

# 2. Grant Vertex AI User permissions
resource "google_project_iam_member" "vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

# 3. Allow K8s Service Account to impersonate the GCP Service Account
resource "google_service_account_iam_member" "workload_identity_user" {
  service_account_id = google_service_account.agent_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.k8s_namespace}/${var.k8s_sa_name}]"
}

# 4. Grant read-only access to Logs/Metrics (for diagnostics)
resource "google_project_iam_member" "logging_viewer" {
  project = var.project_id
  role    = "roles/logging.viewer"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

resource "google_project_iam_member" "monitoring_viewer" {
  project = var.project_id
  role    = "roles/monitoring.viewer"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}
