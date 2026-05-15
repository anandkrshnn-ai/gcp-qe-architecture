output "network_link" {
  value       = google_compute_network.vpc.self_link
  description = "The self-link of the VPC network."
}

output "subnet_link" {
  value       = google_compute_subnetwork.subnet.self_link
  description = "The self-link of the subnet."
}
