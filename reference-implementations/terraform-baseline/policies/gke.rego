package main

# Enforce Workload Identity
deny[msg] {
    input.resource.type == "container.googleapis.com/Cluster"
    not input.resource.workload_identity_config
    msg := "GKE clusters must have Workload Identity enabled"
}

# Enforce Private Clusters (optional strict rule)
deny[msg] {
    input.resource.type == "container.googleapis.com/Cluster"
    input.resource.private_cluster_config == null
    msg := "GKE clusters should be private"
}
