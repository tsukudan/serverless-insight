# Skill: AWS Observability Dashboard

## Overview

This skill teaches GitHub Copilot how to build, extend, and maintain the
`aws-observability-dashboard` within the `serverless-insight` project.

## Skill Metadata

| Field       | Value                              |
|-------------|------------------------------------|
| Name        | aws-observability                  |
| Version     | 0.1.0                              |
| Author      | serverless-insight maintainers     |
| Language    | TypeScript                         |
| Platform    | AWS (Lambda, API Gateway, DynamoDB)|

## Prerequisites

- Node.js >= 18
- AWS CLI configured with appropriate credentials
- AWS CDK CLI (`npm install -g aws-cdk`)

## Examples

### Lambda Handler (TypeScript)

```typescript
import { APIGatewayProxyHandler } from "aws-lambda";

export const handler: APIGatewayProxyHandler = async (event) => {
  console.log(JSON.stringify({ message: "Received event", event }));

  return {
    statusCode: 200,
    body: JSON.stringify({ message: "OK" }),
  };
};
```

### CDK Stack Skeleton

```typescript
import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

export class ObservabilityStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    // Define AWS resources here
  }
}
```

## Patterns

- **Single-table DynamoDB design** – Store all entities in one table using composite keys.
- **Structured logging** – Emit JSON logs so CloudWatch Logs Insights can query them.
- **X-Ray tracing** – Enable active tracing on Lambda functions and API Gateway stages.
- **Least-privilege IAM** – Grant only the permissions required for each function.

## References

- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [AWS CDK v2 Documentation](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- [Amazon DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [AWS X-Ray Documentation](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)
