---
applyTo: "aws-observability-dashboard/**"
---

# AWS Observability Dashboard – Copilot Instructions

These instructions apply to all files under `aws-observability-dashboard/`.

## Frontend (`app/frontend/`)

- Use a modern JavaScript framework (e.g., React or Vue) with TypeScript.
- Consume data from the backend REST API or GraphQL endpoint.
- Use AWS Amplify or direct API calls for authentication and data fetching.
- Implement responsive design with accessibility (a11y) in mind.

## Backend (`app/backend/`)

- Implement AWS Lambda functions in TypeScript (Node.js runtime).
- Use AWS API Gateway for HTTP endpoints.
- Store data in Amazon DynamoDB; prefer single-table design.
- Emit structured logs (JSON) to Amazon CloudWatch Logs.
- Propagate AWS X-Ray traces for end-to-end observability.

## Infrastructure (`infra/`)

- Define all AWS resources using AWS CDK (TypeScript) or AWS SAM templates.
- Follow a stack-per-concern pattern (e.g., separate stacks for networking, data, and compute).
- Tag all resources with `Project`, `Environment`, and `Owner` tags.
- Store Terraform / CDK state remotely (e.g., S3 + DynamoDB lock table).

## General

- Do not commit `.env` files or any secrets to source control.
- Validate all user inputs on both frontend and backend.
- Handle errors gracefully and return meaningful HTTP status codes.
