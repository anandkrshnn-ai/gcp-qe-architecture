terraform {
  backend "gcs" {
    bucket = "tf-state-your-project-id" # Placeholder, actual usage needs dynamic project ID or variable
    prefix = "gcp-qe-architecture/state"
  }
}
