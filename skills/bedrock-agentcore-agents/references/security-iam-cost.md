# Security, IAM & cost

> Prices, quotas, and policy details are volatile — confirm at the linked live sources.

## When this applies

You are hardening access and controlling spend for a Bedrock/AgentCore workload.
(Router: "Lock down IAM / control cost?")

## Key decisions

- **Least privilege by default.** Grant only the permissions required for a task, scoped to
  specific resources and conditions — this is the baseline for IAM policies on Bedrock and
  AgentCore. ([Bedrock IAM examples](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html), [Bedrock IAM](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html), [AgentCore IAM](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security-iam.html))
- **Scope model access.** Restrict which identities can invoke which foundation model endpoints;
  the Well-Architected Generative AI Lens calls for least-privilege access to FM endpoints.
  ([GENSEC01-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec01-bp01.html))
- **Prefer scoped actions over broad managed policies.** Broad policies (for example full-access)
  are convenient but over-grant; scope to the specific actions/resources used.
  ([Bedrock Agents IAM examples](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples-agent.html))
- **Network isolation.** Use interface VPC endpoints (AWS PrivateLink) to reach Bedrock (and
  AgentCore) privately, without an internet gateway/NAT. ([Bedrock VPC endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html), [Protect data with VPC/PrivateLink](https://docs.aws.amazon.com/bedrock/latest/userguide/usingVPC.html), [AgentCore VPC endpoints](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/vpc-interface-endpoints.html))
- **Encryption / KMS.** Data is encrypted at rest with an AWS managed key by default; use a
  customer-managed KMS key where you need control/audit (for example a knowledge base uses a single
  KMS key you specify). Customer-managed keys incur KMS charges. ([KB encryption](https://docs.aws.amazon.com/bedrock/latest/userguide/encryption-kb.html))
- **Cost levers.** Service tiers, prompt caching, batch inference, intelligent prompt routing, and
  Provisioned Throughput are the main cost/throughput levers — see `bedrock-inference-scaling.md`.
  ([Service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html))

## Recommended approach

1. Write identity-based policies that name specific actions (for example `bedrock:InvokeModel` /
   `bedrock:InvokeModelWithResponseStream`) and scope `Resource` to specific model ARNs where
   possible. ([Bedrock IAM examples](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html))
2. Give the AgentCore Runtime execution role only what the agent needs (model invoke, specific
   tools, Memory, gateway targets). ([AgentCore IAM](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security-iam.html))
3. Apply least-privilege access to foundation model endpoints as an identity-based security layer,
   per the Well-Architected Generative AI Lens.
   ([GENSEC01-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec01-bp01.html))
4. Control cost with model choice, token limits (`inferenceConfig.maxTokens`), and observability on
   token usage (see `observability.md`); confirm current prices/quotas at the live pages below.
5. See `assets/iam/` for least-privilege policy templates with scoping placeholders.

## GA vs Preview

- IAM identity-based policies and the Well-Architected Generative AI Lens guidance are documented
  and stable (status as of 2026-09; confirm at the sources). Specific action names track service
  features. ([Bedrock IAM](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html))

## Pitfalls / anti-patterns

- Attaching full-access managed policies to agent roles in production.
  ([Bedrock Agents IAM examples](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples-agent.html))
- Unbounded `maxTokens` or no usage monitoring, so cost drifts silently.
- Wildcard `Resource: "*"` where a model/tool ARN could be named.
  ([Bedrock IAM examples](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html))

## Verify at the live source

- Bedrock pricing: https://aws.amazon.com/bedrock/pricing/
- Bedrock quotas (Service Quotas console) and the Bedrock quotas docs page
- IAM policy references above

## Sources

- https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples-agent.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security-iam.html
- https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec01-bp01.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/usingVPC.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/vpc-interface-endpoints.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/encryption-kb.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html
