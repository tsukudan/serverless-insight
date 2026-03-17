# AWS Observability Dashboard

A serverless observability dashboard for AWS applications, built as part of the [serverless-insight](../README.md) project.

## Directory Structure

```
aws-observability-dashboard/
├── README.md          # This file
├── app/
│   ├── frontend/      # Dashboard UI (Next.js / TypeScript)
│   └── backend/       # Serverless API (AWS Lambda / Python)
└── infra/             # Infrastructure as Code (Terraform)
```

## Getting Started

### Prerequisites

- Node.js >= 18
- Python >= 3.12
- AWS CLI configured with appropriate credentials
- Terraform CLI

### Setup

1. **Frontend**

   ```bash
   cd app/frontend
   npm install
   npm run dev
   ```

2. **Backend**

   ```bash
   cd app/backend
   pip install -r requirements.txt
   pytest
   ```

3. **Infrastructure**

   ```bash
   cd infra
   terraform init
   terraform plan
   terraform apply
   ```

## Architecture Overview

| Layer        | Technology                                  |
|--------------|---------------------------------------------|
| Frontend     | Next.js (Static Export), TypeScript, Tailwind CSS |
| Backend      | AWS Lambda (Python), API Gateway            |
| Data Source   | CloudWatch Metrics, CloudWatch Logs         |
| Database     | DynamoDB (Demo App)                         |
| Hosting      | CloudFront + S3                             |
| IaC          | Terraform                                   |
| CI/CD        | GitHub Actions                              |
| Region       | ap-northeast-1 (Tokyo)                      |

## Contributing

Please read the root [README](../README.md) and the [Copilot instructions](../.github/copilot-instructions.md)
before submitting a pull request.
