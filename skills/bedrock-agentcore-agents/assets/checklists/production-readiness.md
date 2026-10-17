# Production-readiness checklist

Illustrative pre-launch checklist for a Bedrock/AgentCore agent. Each item links to the reference
file (and underlying source) that explains it. Confirm all volatile facts at their live sources.

## Model & API
- [ ] Model chosen for capability, Region availability, and cost; model ID resolved from config,
      not hard-coded. → `references/model-selection-and-converse.md`
- [ ] Using the Converse API (or a deliberate managed alternative). → `references/managed-alternatives.md`

## Tools
- [ ] Tools have clear signatures/docstrings; external tool/MCP output treated as untrusted.
      → `references/tools-strands-and-mcp.md`

## Knowledge / RAG
- [ ] Managed vs customer-managed KB decision recorded; retrieval quality evaluated.
      → `references/rag-knowledge-bases.md`

## Safety
- [ ] Guardrail created, tested, and a pinned **version** attached (not the draft).
      → `references/guardrails.md`
- [ ] Contextual grounding + PII filters enabled where relevant.

## Runtime & memory
- [ ] Deployed on AgentCore Runtime with session isolation. → `references/agentcore-runtime.md`
- [ ] Memory scope (short/long-term) deliberate; no unnecessary PII persisted.
      → `references/agentcore-memory.md`

## Access & auth
- [ ] Shared tools fronted by AgentCore Gateway; inbound/outbound auth chosen.
      → `references/agentcore-gateway-identity.md`
- [ ] Execution role least-privilege; no `Resource: "*"`; model ARNs scoped.
      → `references/security-iam-cost.md`

## Observability
- [ ] Observability enabled; code instrumented for spans/traces; alerts on latency, token usage,
      error rate. → `references/observability.md`

## Testing & rollout
- [ ] Evaluation baseline exists; rollout gated on thresholds; pinned versions promoted.
      → `references/testing-and-rollout.md`
- [ ] AgentCore **built-in evaluators** enabled (start with `FAITHFULNESS` + `CORRECTNESS` for
      hallucination; add `TOOL_SELECTION_ACCURACY` / `TOOL_PARAMETER_ACCURACY` for tool agents).
      → `references/evaluation-and-hallucination.md`
- [ ] **Online evaluation** on in production, with a deliberate **sampling percentage** (0.01–100%)
      and filters for high-risk flows; raise the rate after releases.
- [ ] **Batch evaluation** wired for pre/post comparison and regression runs (ground truth via
      session metadata: expected responses, assertions, expected tool trajectories).
- [ ] Guardrails contextual grounding on RAG paths; Automated Reasoning findings explicitly handled
      (detect-only — it does not block).

## IaC & cost
- [ ] Resources provisioned via Terraform with pinned provider/module versions; volatile values are
      variables. → `references/terraform-iac.md`
- [ ] `maxTokens` bounded; current pricing/quotas confirmed at the live pages.
      → `references/security-iam-cost.md`

## Status hygiene
- [ ] No Preview feature is a production default; GA/Preview status re-verified at source.
