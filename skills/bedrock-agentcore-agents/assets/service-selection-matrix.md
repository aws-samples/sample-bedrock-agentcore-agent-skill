# Service-selection matrix

Illustrative quick-reference mapping a need to the AWS service and the reference file with cited
detail. Confirm GA/Preview and volatile facts at the linked sources.

| Need | Use | Reference |
| --- | --- | --- |
| Call a model with one interface | Bedrock Converse API | `references/model-selection-and-converse.md` |
| Fastest path / managed loop | AgentCore Harness / Bedrock Agents / Flows | `references/managed-alternatives.md` |
| Custom agent loop, code-first | Strands Agents | `references/tools-strands-and-mcp.md` |
| In-process tool | Strands `@tool` | `references/tools-strands-and-mcp.md` |
| Out-of-process / shared tool | MCP (+ AgentCore Gateway) | `references/tools-strands-and-mcp.md`, `references/agentcore-gateway-identity.md` |
| Run code / drive a browser | AgentCore Code Interpreter / Browser | `references/tools-strands-and-mcp.md` |
| Answer from private data | Bedrock Knowledge Bases | `references/rag-knowledge-bases.md` |
| Coordinate multiple agents | Strands Graph/Swarm/Workflow/Agents-as-Tools; A2A | `references/multi-agent-patterns.md` |
| Serverless production hosting | AgentCore Runtime (ARM64 contract) | `references/agentcore-runtime.md` |
| Host a non-Strands framework | AgentCore Runtime (framework-agnostic) | `references/frameworks-on-agentcore.md` |
| Persist state across turns/sessions | AgentCore Memory | `references/agentcore-memory.md` |
| Secure tool access / user auth | AgentCore Gateway + Identity (+ Policy/Cedar) | `references/agentcore-gateway-identity.md` |
| Content safety / PII / grounding | Bedrock Guardrails | `references/guardrails.md` |
| Traces, metrics, dashboards | AgentCore Observability + CloudWatch + ADOT/OTel | `references/observability.md` |
| Evaluate + roll out safely | Bedrock evaluations, versioned endpoints | `references/testing-and-rollout.md` |
| Control cost/latency/throughput | Service tiers, prompt routing, batch, Provisioned Throughput, prompt caching | `references/bedrock-inference-scaling.md` |
| Provision as code | Terraform (`hashicorp/aws`/`awscc`); CDK secondary | `references/terraform-iac.md`, `references/deployment-targets.md` |
| Least-privilege IAM / network / encryption | IAM, VPC PrivateLink, KMS | `references/security-iam-cost.md` |

Sources: each row's linked reference file carries the official-source citations; this matrix is a
restatement of `SKILL.md` routing.
