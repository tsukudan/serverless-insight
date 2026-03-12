# GitHub Copilot Instructions

This file provides workspace-level instructions for GitHub Copilot in the `serverless-insight` project.

## Project Overview

`serverless-insight` is a lightweight observability platform for AWS serverless applications.
It provides an AWS Observability Dashboard built with a frontend, backend, and infrastructure-as-code.

## Architecture

```
aws-observability-dashboard/
├── README.md
├── app/
│   ├── frontend/   # UI for the observability dashboard
│   └── backend/    # API / serverless functions
└── infra/          # Infrastructure as Code (AWS CDK / SAM / Terraform)
```

## Coding Guidelines

- Use TypeScript for both frontend and backend code where possible.
- Follow AWS best practices for serverless architecture (Lambda, API Gateway, DynamoDB, etc.).
- Write infrastructure code using AWS CDK or SAM templates.
- Prefer immutable infrastructure patterns.
- All Lambda functions should include structured logging (JSON format) and proper error handling.
- Use environment variables for configuration; never hard-code secrets or credentials.

## Testing

- Write unit tests for all Lambda functions and utility modules.
- Use integration tests to validate infrastructure deployments in a non-production environment.

## Security

- Follow the principle of least privilege for all IAM roles and policies.
- Enable AWS CloudTrail, AWS Config, and AWS Security Hub integrations where applicable.
- Scan dependencies for known vulnerabilities before deployment.
