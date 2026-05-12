terraform {
  backend "gcs" {
    # This should be populated via backend-config or updated manually for the project
    # bucket  = "YOUR_TF_STATE_BUCKET"
    # prefix  = "terraform/state"
  }
}
