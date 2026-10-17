# Use-case playbooks (match intent → AgentCore architecture)

> Status labels are volatile — confirm GA/Preview and other volatile facts at the linked sources.

## When this applies

Start here when you know *what the customer wants* but not yet *which services to wire together*.
Find the intent that best matches, use the recommended stack and best practices, then open the
linked reference files for cited depth. (Router entry: "Match my intent to a playbook.")

Two rules apply to every playbook below:
- Layer **Guardrails** on any user-facing agent, and enable **Observability** before production.
  ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html), [Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html))
- Scope IAM to least privilege and never make a **Preview** feature a production default (see
  `security-iam-cost.md`).

## Quick intent map

| Customer intent (what they say) | Agent type | Recommended stack | Playbook |
| --- | --- | --- | --- |
| "Answer questions, no actions" | Simple chatbot | Converse + Guardrails | A |
| "Answer from our documents" | Knowledge assistant (RAG) | Knowledge Bases + Memory + Guardrails | B |
| "Do things / call our systems" | Tool-using / action agent | Strands `@tool`/MCP + Gateway + Identity | C |
| "Help our customers end-to-end" | Customer-support agent | RAG + Memory + tools + Guardrails on Runtime | D |
| "Coordinate specialists / complex flow" | Multi-agent system | Strands Graph/Swarm/Workflow (+ A2A) on Runtime | E |
| "Run code / analyze data" | Code/data agent | AgentCore Code Interpreter | F |
| "Use the web / fill forms" | Browser agent | AgentCore Browser | G |
| "Run long / async jobs" | Autonomous/async agent | Runtime (async) + Memory | H |
| "Enterprise-secure it" | Governed agent | Gateway + Identity + Policy/Cedar + VPC/KMS | I |

---

## Playbook A — Simple chatbot (no tools)

- **Signals:** FAQ bot, no external actions, no private data.
- **Stack:** Bedrock **Converse API** (model-agnostic), **Guardrails** attached at inference.
- **Best practices:** use Converse (not `InvokeModel`) for portability; attach a *versioned*
  guardrail; resolve the model ID from config; pick a service tier for cost/latency.
  ([Converse](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html), [Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html), [Service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html))
- **Read:** `model-selection-and-converse.md`, `guardrails.md`.

## Playbook B — Knowledge assistant (RAG over private docs)

- **Signals:** "answer from our PDFs/wiki," citations required.
- **Stack:** **Bedrock Knowledge Bases** (managed by default) + **Guardrails** contextual grounding
  + optional **Memory** for follow-ups.
- **Best practices:** prefer Managed KB for lower ops; keep source citations in responses; enable
  contextual grounding checks to catch ungrounded answers; evaluate retrieval quality before
  rollout. ([Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html), [Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html), [RAG evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html))
- **Read:** `rag-knowledge-bases.md`, `guardrails.md`, `testing-and-rollout.md`.

## Playbook C — Tool-using / action-taking agent

- **Signals:** "call our API," "create a ticket," "look up an order."
- **Stack:** **Strands** agent with `@tool` (in-process) and/or **MCP** (out-of-process); front
  shared tools with **AgentCore Gateway**; authenticate with **AgentCore Identity**.
- **Best practices:** clear tool signatures/docstrings; treat tool output as untrusted; centralize
  shared/enterprise tools behind Gateway instead of re-implementing per agent; use structured output
  for typed results. ([Tools overview](https://strandsagents.com/docs/user-guide/concepts/tools/), [Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), [Structured output](https://strandsagents.com/docs/examples/structured_output/))
- **Read:** `tools-strands-and-mcp.md`, `agentcore-gateway-identity.md`.

## Playbook D — Customer-support agent (the "full stack")

- **Signals:** "help our customers," answers from docs, remembers the customer, takes actions.
- **Stack:** Knowledge Bases (RAG) + **AgentCore Memory** (short + long-term) + tools via
  Gateway/Identity + **Guardrails**, hosted on **AgentCore Runtime**.
- **Best practices:** use long-term Memory only for what improves future turns (keep PII out unless
  protected); put auth/access-control in Gateway not app code; deploy on Runtime for session
  isolation; instrument with ADOT/OpenTelemetry. ([Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-getting-started.html), [Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), [Gateway via infra](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-connector.html), [Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html))
- **Read:** `rag-knowledge-bases.md`, `agentcore-memory.md`, `agentcore-gateway-identity.md`, `agentcore-runtime.md`, `guardrails.md`, `observability.md`.

## Playbook E — Multi-agent system

- **Signals:** "researcher + writer + reviewer," conditional routing, parallel specialists.
- **Stack:** pick a **Strands** primitive by control flow — **Graph** (known order/dependencies),
  **Swarm** (dynamic hand-offs), **Workflow** (fixed sequence), **Agents-as-Tools** (central
  orchestrator); **A2A** for cross-process agents; host on Runtime.
- **Best practices:** add agents only when responsibilities/context diverge; pass synthesized
  hand-offs, not whole histories; watch latency/cost as the agent count grows. ([Agents as tools](https://strandsagents.com/docs/learning/multi-agent-patterns-agents-as-tools/), [Graph](https://strandsagents.com/docs/learning/multi-agent-patterns-graph-workflows/), [Swarm](https://strandsagents.com/docs/learning/multi-agent-patterns-agent-swarms/), [A2A](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html))
- **Read:** `multi-agent-patterns.md`, `frameworks-on-agentcore.md`, `agentcore-runtime.md`.

## Playbook F — Code / data-analysis agent

- **Signals:** "run calculations," "analyze this dataset," "generate and execute code."
- **Stack:** **AgentCore Code Interpreter** (sandboxed code execution) driven by the agent.
- **Best practices:** rely on the built-in sandbox/session isolation instead of hand-rolled
  execution; treat generated code and outputs as untrusted; scope IAM to what the agent needs.
  ([Built-in tools](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-tools.html), [Code Interpreter](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-tool.html))
- **Read:** `tools-strands-and-mcp.md` (built-in tools), `security-iam-cost.md`.

## Playbook G — Browser / web-automation agent

- **Signals:** "navigate a site," "fill a form," "scrape and act."
- **Stack:** **AgentCore Browser** (isolated cloud browser; Playwright for programmatic control).
- **Best practices:** use the managed isolated browser over self-hosted headless setups; treat page
  content as untrusted input; keep credentials out of prompts. ([Built-in tools how it works](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-tools-how-it-works.html), [Browser + Playwright](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-quickstart-playwright.html))
- **Read:** `tools-strands-and-mcp.md` (built-in tools), `security-iam-cost.md`.

## Playbook H — Autonomous / long-running / async agent

- **Signals:** "kick off a job and come back," background processing, extended runs.
- **Stack:** **AgentCore Runtime** (extended/async support, session isolation) + **Memory** for
  durable state.
- **Best practices:** design for async explicitly; persist only necessary state to Memory; alert on
  latency/token/error metrics. ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), [Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-getting-started.html), [Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html))
- **Read:** `agentcore-runtime.md`, `agentcore-memory.md`, `observability.md`.

## Playbook I — Enterprise-governed agent

- **Signals:** "must be secure/compliant," private networking, fine-grained authz.
- **Stack:** **AgentCore Gateway + Identity** for auth, **Policy/Cedar** for fine-grained tool
  authorization, **VPC PrivateLink** for private connectivity, **KMS** for encryption, **Guardrails**
  for content controls.
- **Best practices:** enforce authz with Cedar policies on gateway tools; reach Bedrock/AgentCore
  over interface VPC endpoints; use customer-managed KMS keys where you need control/audit; scope
  every role. ([Policy/Cedar](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html), [VPC endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html), [KB encryption/KMS](https://docs.aws.amazon.com/bedrock/latest/userguide/encryption-kb.html), [Least privilege](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html))
- **Read:** `agentcore-gateway-identity.md`, `security-iam-cost.md`, `guardrails.md`.

---

## Deciding factors that cut across playbooks

- **Do you even need code?** Consider managed Bedrock Agents / Flows / Responses API first
  (`managed-alternatives.md`).
- **Cost/scale sensitive?** Apply service tiers, prompt caching, batch, routing, Provisioned
  Throughput (`bedrock-inference-scaling.md`).
- **Provisioning?** Terraform-first (`terraform-iac.md`, `deployment-targets.md`).

## Verify at the live source

- AgentCore capabilities: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html

## Sources

- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html
- https://strandsagents.com/docs/user-guide/concepts/tools/
- https://strandsagents.com/docs/examples/structured_output/
- https://strandsagents.com/docs/learning/multi-agent-patterns-agents-as-tools/
- https://strandsagents.com/docs/learning/multi-agent-patterns-graph-workflows/
- https://strandsagents.com/docs/learning/multi-agent-patterns-agent-swarms/
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-getting-started.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-connector.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-tools.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-tools-how-it-works.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-tool.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-quickstart-playwright.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/encryption-kb.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html
