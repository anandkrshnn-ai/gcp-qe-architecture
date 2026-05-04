terraform {
  # Note: Backend blocks do not support interpolation. 
  # Use 'terraform init -backend-config="bucket=..."' for dynamic backends.
  backend "gcs" {
    bucket = "tf-state-YOUR_PROJECT_ID" 
    prefix = "gcp-qe-architecture/terraform"
  }
}
