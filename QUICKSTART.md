# 🚀 Quickstart: GCP QE Architecture

Follow these steps to deploy the architecture or run the Sovereign AI RCA prototype locally.

## 1. Local Sovereign AI RCA (No GCP Required)
Test the **Sovereign-Native Quality Engineering** flow on your machine.

### Prerequisites
- Python 3.12+
- [Ollama](https://ollama.com/) (Local LLM Server)

### Steps
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/anandkrshnn-ai/gcp-qe-architecture.git
   cd gcp-qe-architecture
   ```
2. **Setup Environment**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Pull Sovereign Model**:
   ```bash
   ollama pull llama3
   ```
4. **Execute RCA Agent**:
   ```bash
   python frameworks/sovereign-ai-qe/tools/sovereign-rca-agent.py --logs frameworks/gemini-agent-qe/tools/sample_logs.json
   ```

---

## 2. Infrastructure Deployment (GCP)
Provision the hardened QE baseline in your GCP project.

### Prerequisites
- [Terraform v1.10+](https://www.terraform.io/downloads)
- Active GCP Project and Service Account credentials.

### Steps
1. **Navigate to Environment**:
   ```bash
   cd reference-implementations/terraform-baseline/environments/dev
   ```
2. **Configure Variables**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your project_id
   ```
3. **Deploy**:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

---

## 3. Performance Testing (k6)
Validate the deployment or run against the local mock server.

### Steps
1. **Start Mock Server**:
   ```bash
   node tools/mock-server/server.js
   ```
2. **Execute k6 Suite**:
   ```bash
   # Basic Load Test
   k6 run reference-implementations/k6-performance/cloud-run-load-test.js
   
   # Cold Start Test
   k6 run reference-implementations/k6-performance/cold-start-test.js
   ```
