# AWS Observability Dashboard

A serverless observability dashboard for AWS applications, built as part of the [serverless-insight](../README.md) project.

## Directory Structure

```
aws-observability-dashboard/
├── README.md          # This file
├── app/
│   ├── frontend/      # Dashboard UI (React / TypeScript)
│   └── backend/       # Serverless API (AWS Lambda / TypeScript)
└── infra/             # Infrastructure as Code (AWS CDK / TypeScript)
```

## Getting Started

### Prerequisites

- Node.js >= 18
- AWS CLI configured with appropriate credentials
- AWS CDK CLI: `npm install -g aws-cdk`

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
   npm install
   npm test
   ```

3. **Infrastructure**

   ```bash
   cd infra
   npm install
   npx cdk bootstrap   # First time only
   npx cdk deploy
   ```

## Architecture Overview

| Layer        | Technology                            |
|--------------|---------------------------------------|
| Frontend     | React, TypeScript, AWS Amplify        |
| Backend      | AWS Lambda, API Gateway, DynamoDB     |
| Observability| CloudWatch, X-Ray, CloudTrail         |
| IaC          | AWS CDK (TypeScript)                  |

## Contributing

Please read the root [README](../README.md) and the [Copilot instructions](../.github/copilot-instructions.md)
before submitting a pull request.
