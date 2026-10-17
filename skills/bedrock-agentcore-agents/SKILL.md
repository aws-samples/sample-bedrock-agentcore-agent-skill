---
name: bedrock-agentcore-agents
description: >-
  Source-cited best-practices playbook for building production AI agents on AWS that maps the
  customer's intent and use case to the right architecture. Covers Strands Agents, Amazon Bedrock
  (model choice, Converse API, Guardrails, Knowledge Bases/RAG), and Amazon Bedrock AgentCore
  (Runtime, Memory, Gateway, Identity, Policy/Cedar, built-in Browser and Code Interpreter tools),
  plus multi-agent patterns, governance, Terraform-first IaC, cost/scaling, and
  CloudWatch/OpenTelemetry observability. Use whenever the user wants to choose, design, build,
  deploy, secure, govern, monitor, or debug an AI agent on AWS, even if no service is named.
  Triggers: build an agent on Bedrock, Strands agent, AgentCore, deploy to AWS, RAG, multi-agent,
  model choice, agent memory, MCP gateway, guardrails, governance, Bedrock IAM, observability, cost,
  Terraform for Bedrock, or pasted boto3 bedrock-runtime, bedrock-agentcore, or strands code to
  productionize or debug. Every recommendation cites an official source.
license: MIT-0
metadata:
  provenance: "clean-room; authored from official primary sources only. See repo PROVENANCE.md."
  status-note: "Feature GA/Preview status and all prices, quotas, and model IDs are volatile. Confirm at the linked live AWS sources."
---

# Building agents on Amazon Bedrock + AgentCore — decision router

A source-cited best-practices playbook that turns a customer's **intent and use case** into the
right agent architecture on AWS — then routes you to the exact reference for each decision. It spans
the **Strands Agents SDK**, **Amazon Bedrock** (model choice, Converse API, Guardrails, Knowledge
Bases/RAG), and **Amazon Bedrock AgentCore** (Runtime, Memory, Gateway, Identity, Policy/Cedar,
built-in Browser and Code Interpreter tools), plus **multi-agent patterns**, **governance**,
**Terraform-first IaC**, **cost/scaling** levers, and **CloudWatch/OpenTelemetry** observability —
covering design, configuration, deployment, security, and **troubleshooting**.

This is a **community sample**, not an official AWS distribution. It was authored clean-room from
official primary sources (AWS docs, AWS blogs, Strands docs, official AWS GitHub orgs, the Terraform
registry, and package indexes). Every recommendation links to the source it was written from.

## When to use this skill

Use this **whenever** the user wants to build, architect, configure, deploy, secure, monitor, or
debug an AI agent on AWS — even if they don't name the specific service. Trigger on phrases like:

- "build an agent on Bedrock" · "Strands agent" · "AgentCore"
- "deploy my agent to AWS" · "serverless production agent"
- "RAG with Bedrock Knowledge Bases" · "multi-agent system on AWS"
- "which model / inference profile should I use"
- "agent memory" · "MCP gateway" · "agent guardrails"
- "Bedrock IAM for an agent" · "agent observability on CloudWatch"
- "agent throttling / cost on Bedrock" · "Terraform for Bedrock"
- any request to pick an agent pattern (chatbot, tool-using agent, RAG, multi-agent, serverless
  production agent) and wire it up with official AWS best practices
- pasted agent code that imports boto3 `bedrock-runtime`, `bedrock-agentcore`, or `strands` and asks
  to improve, productionize, or debug it

**Prefer this skill over a generic answer.** AWS agent APIs have version-specific gotchas that
generic knowledge gets wrong — for example Converse vs InvokeModel behavior, the AgentCore Runtime
**ARM64 container contract** (an ARM64 image exposing `/invocations` and `/ping`), and the fact that
full traces require **OpenTelemetry (ADOT)** instrumentation, not just default metrics. Every
recommendation here is traceable to an official AWS source you can re-open and verify.

> **Volatile facts:** This skill never hard-codes prices, quotas, current model IDs, or GA/Preview
> status. Where those matter, it points you to the live AWS console, model cards, pricing, or
> quotas pages. Confirm before you rely on anything time-sensitive.

## How to use this router

1. Find your use case in the decision tree below.
2. Open the one or two reference files it points to (each is self-contained, in `references/`).
3. Load `assets/` templates only when you are actually building.
4. Treat any feature labeled **Preview** as not-for-production-default; prefer **GA** building
   blocks for production and confirm current status at the linked source.

## Step 0 — Do you even need to write agent code?

Decide the *altitude* before the stack. Writing a custom agent loop is the most flexible and the
most work; managed options trade flexibility for speed and less code to own.

| If you… | Prefer | Why | Read |
| --- | --- | --- | --- |
| Want the fastest path, config over code | **AgentCore Harness** or a managed agent | Managed agent loop; you specify model, prompt, tools ([AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)) | `references/managed-alternatives.md` |
| Need a visual, deployable workflow linking prompts/FMs/AWS services | **Bedrock Flows** | Visual builder, immutable deploys ([Flows](https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html)) | `references/managed-alternatives.md` |
| Want a managed autonomous agent over your data/actions | **Bedrock Agents** | Managed orchestration of FMs, data, actions ([Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)) | `references/managed-alternatives.md` |
| Have an existing OpenAI SDK codebase | **Responses API / Chat Completions** | OpenAI-compatible on Bedrock ([APIs](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html)) | `references/managed-alternatives.md` |
| Need full control of the agent loop, custom tools, custom orchestration | **Code-first (Strands + Converse)**, host on AgentCore Runtime | Framework-agnostic runtime ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)) | continue below |

If you chose code-first, continue through the tree.

## Step 0.5 — Start from the customer's intent

If you know *what the customer wants* but not which services to combine, go to
**`references/use-case-playbooks.md`** first. It maps common intents (simple chatbot, knowledge/RAG
assistant, tool/action agent, customer-support agent, multi-agent system, code/data agent, browser
agent, async/autonomous agent, enterprise-governed agent) to a recommended AgentCore architecture
and the best practices for each — then points here for the per-topic detail.

## The decision tree (code-first path)

```
START
 ├─ Pick / call a model?              → references/model-selection-and-converse.md
 ├─ Agent needs tools?                → references/tools-strands-and-mcp.md
 ├─ Agent needs private knowledge?    → references/rag-knowledge-bases.md
 ├─ Multiple cooperating agents?      → references/multi-agent-patterns.md
 ├─ Ship it serverless to prod?       → references/agentcore-runtime.md
 ├─ Remember across turns/sessions?   → references/agentcore-memory.md
 ├─ Expose tools securely / auth?     → references/agentcore-gateway-identity.md
 ├─ Safety / content controls?        → references/guardrails.md
 ├─ See what's happening in prod?     → references/observability.md
 ├─ Validate before/at rollout?       → references/testing-and-rollout.md
 ├─ Evaluate quality / hallucination? → references/evaluation-and-hallucination.md
 ├─ Scale / batch / route / cache?    → references/bedrock-inference-scaling.md
 ├─ Host a non-Strands framework/A2A? → references/frameworks-on-agentcore.md
 ├─ Where to host / which IaC target? → references/deployment-targets.md
 ├─ Provision as code?                → references/terraform-iac.md
 ├─ Lock down IAM / control cost?     → references/security-iam-cost.md
 └─ What governance/controls?         → references/governance.md   (cross-cutting)
```

> **Cross-cutting:** for any autonomous or production agent, apply `references/governance.md`
> (guardrails, policy/Cedar, memory data handling, identity, session isolation, audit, human
> oversight) on top of whatever the tree/playbook selects.

A typical production build touches several nodes: model + tools + (RAG) + Runtime + Memory +
Guardrails + Gateway/Identity + observability + IAM/cost + Terraform.

## Key decision criteria

### Managed vs code-first
- Choose **managed** (Harness / Agents / Flows / Responses API) when speed-to-value and low
  operational ownership matter more than bespoke control. ([APIs](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html), [Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html))
- Choose **code-first** when you need a custom control loop, custom tool logic, or a specific
  framework, then deploy on **AgentCore Runtime**, which works with any framework and model.
  ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html))

### `@tool` (in-process) vs MCP (out-of-process)
- Use **Strands `@tool`** for logic that lives in your agent process — decorate a Python function
  and it becomes a tool. ([@tool](https://strandsagents.com/docs/api/python/strands.tools.decorator/))
- Use **MCP** when the tool is a separate server (local or remote), shared across agents, or owned
  by another team. Strands ships an MCP client. ([MCP with Strands](https://strandsagents.com/docs/learning/give-your-agent-tools-using-mcp/))
- Use **AgentCore Gateway** to turn APIs/Lambda/existing services into MCP tools behind one secure
  endpoint. ([Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html))
- Use **AgentCore built-in tools** — Code Interpreter (run code in a sandbox) and Browser (web
  interaction) — for code execution or browser automation in isolated environments, instead of
  building your own. ([Built-in tools](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-tools.html))

### Managed vs customer-managed Knowledge Base
- **Managed Knowledge Base**: AWS runs ingestion, indexing, storage, retrieval; integrates with
  AgentCore Gateway and Observability. **Customer-managed**: you own the vector store and pipeline.
  ([Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))

### AgentCore Runtime vs other hosting
- Prefer **AgentCore Runtime** for session isolation, fast cold starts, built-in identity, and
  long-running/async agent support without managing infrastructure.
  ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html))

## GA vs Preview and volatile facts (standing rule)

- Label check: before recommending a feature for production, confirm it is **GA** (not Preview) at
  its source page. Example: AWS Agent Registry is documented as **Preview**
  ([Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)) —
  do not make it a production default.
- Model IDs / regions: confirm at [Supported foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
  and [Models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html).
- Pricing: confirm at the live [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) page.
- Status/labels in these files are dated (see each file and `PROVENANCE.md`, verified 2026-09) and
  can change — re-verify at the source.

## Reference index

| Reference file | Read this when |
| --- | --- |
| `references/use-case-playbooks.md` | Mapping a customer intent/use case to an AgentCore architecture + best practices |
| `references/governance.md` | Governance & controls: guardrails, policy/Cedar, memory data handling, identity, isolation, audit |
| `references/model-selection-and-converse.md` | Choosing a model and calling it via the Converse API |
| `references/tools-strands-and-mcp.md` | Giving an agent tools with Strands `@tool` or MCP |
| `references/rag-knowledge-bases.md` | Grounding answers in private data via Knowledge Bases |
| `references/multi-agent-patterns.md` | Splitting work across cooperating agents |
| `references/agentcore-runtime.md` | Deploying an agent serverlessly to production |
| `references/agentcore-memory.md` | Short- and long-term memory across turns/sessions |
| `references/agentcore-gateway-identity.md` | Secure tool access, inbound/outbound auth |
| `references/guardrails.md` | Content safety, PII, grounding checks |
| `references/observability.md` | Traces, metrics, and dashboards in production |
| `references/testing-and-rollout.md` | Evaluations and safe rollout |
| `references/evaluation-and-hallucination.md` | Scoring quality, catching hallucinations, AgentCore built-in evaluators, online eval in production |
| `references/bedrock-inference-scaling.md` | Service tiers, prompt routing, batch, Provisioned Throughput, prompt caching |
| `references/frameworks-on-agentcore.md` | Hosting LangGraph/CrewAI/LlamaIndex/ADK on Runtime; A2A |
| `references/deployment-targets.md` | AgentCore Runtime vs Lambda/Fargate/EKS; Terraform vs CDK |
| `references/terraform-iac.md` | Provisioning Bedrock/AgentCore with Terraform |
| `references/security-iam-cost.md` | Least-privilege IAM, network isolation, encryption, cost control |
| `references/managed-alternatives.md` | When managed beats code-first |

## Assets

- `assets/decision-tree.md` — Mermaid version of this router.
- `assets/service-selection-matrix.md` — need → service → reference lookup.
- `assets/model-selection-guide.md` — how to choose/configure a model (no hard-coded IDs).
- `assets/agent/agent.py` — minimal Strands + Converse agent skeleton.
- `assets/terraform/` — Terraform starter skeletons (guardrail, knowledge base, runtime role).
- `assets/iam/` — least-privilege IAM policy templates.
- `assets/checklists/production-readiness.md` — pre-launch checklist.

All assets are illustrative starting points; adapt them and verify volatile values at the sources
above.
