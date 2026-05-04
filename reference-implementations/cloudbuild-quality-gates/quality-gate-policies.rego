package cloudbuild.quality

# Default deny
default allow = false

# Gate: Container images must not run as root
deny[msg] {
    input.kind == "Deployment"
    container := input.spec.template.spec.containers[_]
    not container.securityContext.runAsNonRoot
    msg := sprintf("Container '%v' must set securityContext.runAsNonRoot to true", [container.name])
}

# Gate: All workloads must have resource limits defined
deny[msg] {
    input.kind == "Deployment"
    container := input.spec.template.spec.containers[_]
    not container.resources.limits.cpu
    msg := sprintf("Container '%v' must have CPU limits defined to prevent resource exhaustion", [container.name])
}

# Gate: Readiness probes are mandatory for zero-downtime deployments
deny[msg] {
    input.kind == "Deployment"
    container := input.spec.template.spec.containers[_]
    not container.readinessProbe
    msg := sprintf("Container '%v' is missing a readinessProbe", [container.name])
}
