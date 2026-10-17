# Deployment targets & IaC choice

> Status labels are volatile — confirm at the linked live sources.

## When this applies

You are deciding *where* the agent runs and *how* it is provisioned, beyond the default AgentCore
Runtime path. (Router: "Where do I host it / which IaC?")

## Key decisions

- **AgentCore Runtime vs self-managed compute.** Prefer AgentCore Runtime for serverless hosting
  with session isolation, built-in identity, and observability plumbing — the infrastructure is
  managed and the agent logic is your code. Choose self-managed compute (Lambda, Fargate/ECS, EKS)
  only when you have a specific reason (existing platform, custom networking, non-agent workloads
  alongside). ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), [Harness vs Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-vs-runtime.html))
- **IaC: Terraform-first, CDK secondary.** This skill authors Terraform (see `terraform-iac.md`).
  The AgentCore starter toolkit can also emit IaC-ready code in Terraform or CDK when it scaffolds a
  project, and an AWS CDK AgentCore construct library exists. ([AgentCore get started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html), [CDK AgentCore construct](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrock_agentcore_alpha/README.html))

## Recommended approach

1. Default to AgentCore Runtime; drop to self-managed compute only for a concrete constraint.
   ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html))
2. Whatever the host, if you build a container it must meet the Runtime contract (ARM64,
   `/invocations` + `/ping`) — see `agentcore-runtime.md`. ([Runtime contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html))
3. Provision with Terraform (pinned providers/modules; see `terraform-iac.md`). Use CDK only if your
   org already standardizes on it, and pin the (alpha) AgentCore construct version.
   ([CDK AgentCore construct](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrock_agentcore_alpha/README.html))
4. Keep IAM least-privilege and networking private where needed (see `security-iam-cost.md`).

## GA vs Preview

- AgentCore Runtime is a documented capability (status as of 2026-09; confirm at the source). The
  CDK AgentCore construct is an `alpha` module — do not make an alpha construct a production default;
  pin versions and validate. ([CDK AgentCore construct](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrock_agentcore_alpha/README.html))

## Pitfalls / anti-patterns

- Reaching for Lambda/EKS by habit when AgentCore Runtime removes the ops burden.
- Building an x86_64 container or missing the required endpoints (contract violation).
  ([Runtime contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html))
- Depending on an alpha CDK construct without pinning/validating.

## Verify at the live source

- AgentCore dev guide: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- CDK construct hub / API reference (confirm module stability level)

## Sources

- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-vs-runtime.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html
- https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrock_agentcore_alpha/README.html
