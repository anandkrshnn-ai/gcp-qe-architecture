# Policy as Code (OPA / Gatekeeper)

These Rego policies can be used with:
- **Terraform validation**: Use `opa` to validate `terraform show -json tfplan`
- **GKE Policy Automation**: Automate policy checks in CI
- **Gatekeeper**: Apply policies directly on GKE clusters to prevent non-compliant resource creation.

## Usage Example
```bash
opa exec --decision main/deny --bundle policies/ tfplan.json
```
