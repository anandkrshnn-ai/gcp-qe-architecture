output "agent_sa_email" {
  value       = google_service_account.agent_sa.email
  description = "The email of the agent service account."
}
