# Terraform-first IaC

> Provider/module versions and resource schemas are volatile — confirm at the linked live sources.

## When this applies

You want repeatable, reviewable provisioning of Bedrock/AgentCore resources.
(Router: "Provision as code?")

## Key decisions

- **Module vs raw resources.** For Bedrock, the AWS-maintained `aws-ia/terraform-aws-bedrock`
  module can deploy an agent by default and, via input flags, guardrails, knowledge bases, and more.
  Use it to move fast; drop to raw provider resources when you need fine control.
  ([terraform-aws-bedrock](https://github.com/aws-ia/terraform-aws-bedrock))
- **Which provider.** Use the official `hashicorp/aws` provider (and `hashicorp/awscc` for
  resources exposed via Cloud Control) from the Terraform Registry. `hashicorp/aws` is the official
  AWS provider published by HashiCorp. ([Provider registry](https://docs.hashicorp.com/terraform/internals/provider-registry-protocol), [aws guardrail resource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/bedrockagent_guardrail))

## Recommended approach

1. Pin provider and module versions in `required_providers`/module blocks; do not float `latest`.
   ([Configure providers](https://developer.hashicorp.com/terraform/tutorials/configuration-language/configure-providers))
2. Start from the `aws-ia/terraform-aws-bedrock` module for agents/guardrails/knowledge bases; set
   the relevant `create_*` flags for the features you need.
   ([terraform-aws-bedrock](https://github.com/aws-ia/terraform-aws-bedrock))
3. For a single resource, use the provider resource directly (for example a Bedrock guardrail).
   ([aws guardrail resource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/bedrockagent_guardrail))
4. Parameterize everything volatile (model IDs, Region, account) as variables — never hard-code.
5. Keep IAM scoped in the same code (see `security-iam-cost.md`), and see `assets/terraform/` for
   starter skeletons.

> Note: the AgentCore starter toolkit can also emit IaC-ready code in Terraform or CDK when it
> scaffolds a project. ([AgentCore get started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html))

## GA vs Preview

- The `hashicorp/aws` and `hashicorp/awscc` providers and the `aws-ia/terraform-aws-bedrock` module
  are actively published; individual resources track service features and may lag new/Preview APIs.
  Confirm resource availability in the registry before relying on it.
  ([aws provider docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/bedrockagent_guardrail))

## Pitfalls / anti-patterns

- Floating `latest` provider/module versions — pin them for reproducibility.
  ([Configure providers](https://developer.hashicorp.com/terraform/tutorials/configuration-language/configure-providers))
- Hard-coding model IDs/account IDs/Regions in `.tf` instead of variables.
- Expecting a Terraform resource to exist for a brand-new/Preview API before the provider adds it.

## Verify at the live source

- AWS provider registry: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- AWSCC provider registry: https://registry.terraform.io/providers/hashicorp/awscc/latest/docs
- Module: https://github.com/aws-ia/terraform-aws-bedrock

## Sources

- https://github.com/aws-ia/terraform-aws-bedrock
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/bedrockagent_guardrail
- https://docs.hashicorp.com/terraform/internals/provider-registry-protocol
- https://developer.hashicorp.com/terraform/tutorials/configuration-language/configure-providers
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html
