# Basic test resources
resource "google_project_service" "test" {
  service = "monitoring.googleapis.com"
}
