# Deploying to Production (GCP)

This repository provides an **Architectural Simulation**. To move from simulation to a live production deployment on Google Cloud Platform, follow these steps.

## 1. Prerequisites
- A Google Cloud Project with Billing enabled.
- Google Cloud SDK (`gcloud`) installed and authenticated.
- Terraform (v1.10+) installed.
- Python 3.9+ installed.

## 2. Infrastructure Setup (IaC)
Deploy the baseline infrastructure to host the analyzer and your applications:

```bash
cd terraform-baseline
terraform init
terraform plan
terraform apply
```
*Note: This will deploy the networking, GKE clusters, and Cloud Run services defined in the modules.*

## 3. Configure Authentication
For the analyzer to connect to real GCP logs, you must provide a Service Account with `Logging Viewer` permissions.

1. Create a Service Account in GCP Console.
2. Grant the role `roles/logging.viewer`.
3. Download the JSON key file.
4. Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
   ```

## 4. Enable Production Mode in Code
Modify the entry point in `frameworks/sovereign_core/client.py` or your execution script:

```python
# Change mode from "simulation" to "production"
client = SovereignClient(mode="production", project_id="your-gcp-project-id")
```

## 5. Install Production Dependencies
The simulation mode requires zero dependencies, but production mode requires the Google Cloud SDKs:

```bash
pip install google-cloud-logging google-cloud-monitoring
```

## 6. Verification
Run the demo with real credentials and project ID:
```bash
python run_demo.py oomkill
```
The system will now fetch real logs from your GKE clusters instead of loading local JSON files.
