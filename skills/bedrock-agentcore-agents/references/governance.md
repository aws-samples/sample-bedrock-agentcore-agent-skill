# Governance & responsible-agent best practices

> Status labels and version-specific limits (e.g., retention min/max) are volatile — confirm at the
> linked live sources.

## When this applies

Any agent that acts autonomously, touches user data, or runs in production. Governance is
cross-cutting: apply it alongside whichever use-case playbook you picked
(`use-case-playbooks.md`). (Router: "What governance/controls do I need?")

## The governance model

Autonomous agents invoke tools, modify data, and interact with systems without a human in the loop
at each step — so they need controls, permission boundaries, and human-oversight patterns built for
autonomy. ([Agentic AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html), [Security pillar](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/security.html))

Two design principles anchor the rest:
- **Layer guardrails between intent and action** — pre-execution input filters, runtime alignment
  controls, and post-execution output filters; keep critical actions gated behind human approval.
  ([Security design principles](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/security-design-principles.html))
- **Pair autonomy with proportionate human oversight** — define autonomy levels (observer,
  assistant, autonomous, orchestrator) and escalation paths up front; review depth scales with the
  consequence of the action. ([Design principles](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/design-principles.html))

## Best practices by control area

### Guardrails (content, PII, grounding)
- Attach a **versioned** Bedrock Guardrail (never the draft); enable content filters, denied topics,
  sensitive-information (PII block/mask), and contextual grounding for RAG.
  ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))
- Treat guardrails as one layer of defense between intent and action, not the whole control.
  ([Security design principles](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/security-design-principles.html))
- Detail: `guardrails.md`.

### Policy & authorization (what the agent may do)
- Use **Policy in AgentCore** with **Cedar** for precise, verifiable, schema-validated authorization
  on gateway tools — human-readable and analyzable. Gate high-consequence tools tightly.
  ([Policy core concepts](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html), [Understanding Cedar](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-understanding-cedar.html))
- Detail: `agentcore-gateway-identity.md`.

### Identity & access (who is calling)
- Authenticate callers with **AgentCore Identity**; push auth/access-control into **Gateway** rather
  than app code. Encrypt Identity token vaults — a customer-managed key is available where you need
  control. ([Identity encryption](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-data-encryption.html), [Gateway via infra](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-connector.html))
- Protect account credentials and give each identity only the permissions it needs (least
  privilege). ([Data protection](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/data-protection.html))
- Detail: `agentcore-gateway-identity.md`, `security-iam-cost.md`.

### Memory governance (what the agent remembers)
This is a common failure area — treat memory as governed data, not a scratchpad.
- **Partition by namespace.** Do not share memory across agents/users/sessions without namespace
  partitioning; unpartitioned, unvalidated memory enables cross-session contamination with no tamper
  detection. ([Secure agent memory & state](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec01.html))
- **Encrypt.** AgentCore Memory is encrypted at rest with KMS; use a **customer-managed key**
  (`encryptionKeyArn`) when handling sensitive data. ([Memory best practices](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html), [Encrypt Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/storage-encryption.html), [Create a memory store](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-create-a-memory-store.html))
- **Minimize + set retention.** Persist only what improves future turns; keep PII out of long-term
  memory unless required and protected; configure the retention/expiration window per your
  data-retention policy (confirm the current min/max at the source). ([Create a memory store](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-create-a-memory-store.html))
- Detail: `agentcore-memory.md`.

### Runtime isolation (blast radius)
- Rely on Runtime's per-session **microVM isolation**: sessions cannot access other workloads, and
  the microVM is terminated and memory sanitized after the session. Do not treat session/disk state
  as durable — it persists only for the compute lifecycle (use Memory for durability).
  ([Runtime security best practices](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html), [Isolated sessions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html))
- Detail: `agentcore-runtime.md`.

### Network & encryption (data protection)
- Reach Bedrock/AgentCore privately via **interface VPC endpoints (PrivateLink)**; use customer-
  managed **KMS** keys where control/audit is required. ([VPC endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html), [KB encryption](https://docs.aws.amazon.com/bedrock/latest/userguide/encryption-kb.html))
- Detail: `security-iam-cost.md`.

### Observability & audit (prove what happened)
- Enable **Observability** before production; instrument with **ADOT/OpenTelemetry** for full-path
  traces (request → inference → tools → memory → response); alert on latency, token usage, and error
  rate. ([Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), [Agentic AI Lens: tracing](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentrel08-bp02.html))
- Detail: `observability.md`.

### Lifecycle governance (safe change)
- Define purpose, autonomy level, and success criteria before deployment; promote agents through
  explicit gates (SME validation, CI/CD for non-deterministic systems, staged rollouts); detect
  drift and anomalies. ([Operational excellence principles](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/operational-excellence-design-principles.html))
- Gate rollout on evaluations; promote pinned versions. Detail: `testing-and-rollout.md`.

## Governance checklist (apply per agent)

- [ ] Autonomy level chosen; high-consequence actions gated behind human approval.
- [ ] Versioned Guardrail attached (content + PII + grounding as relevant).
- [ ] Cedar policies scope which tools the agent may call.
- [ ] Identity/auth enforced at the Gateway; least-privilege IAM roles.
- [ ] Memory namespaced, encrypted (CMK for sensitive data), minimized, with a retention window.
- [ ] Runtime session isolation understood; durable state in Memory, not session disk.
- [ ] Private networking (PrivateLink) + KMS where required.
- [ ] Observability on; ADOT traces; alerts on latency/tokens/errors.
- [ ] Evaluation gate + staged rollout + pinned versions.
- [ ] No Preview feature used as a production default; volatile facts verified at source.

## GA vs Preview

- The Well-Architected Agentic AI Lens guidance and the AgentCore security/memory/identity controls
  above are documented (status as of 2026-09; confirm at the sources). Retention limits and CMK
  configuration options can change — verify current values before relying on them.

## Verify at the live source

- Agentic AI Lens (security): https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/security.html
- AgentCore data protection: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/data-protection.html

## Sources

- https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html
- https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/security.html
- https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/security-design-principles.html
- https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/design-principles.html
- https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/operational-excellence-design-principles.html
- https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec01.html
- https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentrel08-bp02.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/storage-encryption.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-create-a-memory-store.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/data-protection.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-data-encryption.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-understanding-cedar.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-connector.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/encryption-kb.html
