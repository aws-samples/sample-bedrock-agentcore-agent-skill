# When a managed alternative beats code-first

> Status labels are volatile — confirm at the linked live sources.

## When this applies

Before writing a custom agent loop, decide whether a managed option gets you there with less code
and less to operate. (Router: "Do you even need to write agent code?")

## The options

- **AgentCore Harness** — a managed agent loop you invoke with a single API call; you specify model,
  system prompt, and tools inline, and it handles orchestration, tool execution, memory, and
  response generation. Good when you want a managed loop but not a full framework.
  ([AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html))
- **Bedrock Agents** — managed autonomous agents that orchestrate FMs, data sources, applications,
  and user conversations to complete actions. Good for a managed agent over your data/actions
  without building orchestration. ([Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html), [How Agents work](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-how.html))
- **Bedrock Flows** — a visual builder to link prompts, FMs, knowledge bases, and AWS services
  (like Lambda) into deployable, immutable workflows. Good for structured, largely deterministic
  pipelines. ([Flows](https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html))
- **Responses API / Chat Completions (OpenAI-compatible)** — bring an existing OpenAI SDK codebase
  to Bedrock by changing base URL and API key; the Responses API supports stateful, agentic
  interactions with built-in tool use and history management, plus Bedrock features like Guardrails
  and cross-Region inference. ([APIs](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html), [API compatibility](https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html), [Endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html))

## Decision criteria

| Choose | When |
| --- | --- |
| **Bedrock Flows** | Workflow is mostly deterministic; you want a visual builder and immutable deploys ([Flows](https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html)) |
| **Bedrock Agents** | You want a managed autonomous agent over your data/actions, minimal orchestration code ([Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)) |
| **AgentCore Harness** | You want a managed agent loop with inline model/prompt/tools, not a full framework ([Overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)) |
| **Responses API / Chat Completions** | You already have OpenAI SDK code and want minimal migration ([API compatibility](https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html)) |
| **Code-first (Strands + Converse) on AgentCore Runtime** | You need a custom control loop, custom tools, or a specific framework ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)) |

## Recommended approach

1. Start at the highest altitude that meets the requirement; drop to code-first only when you hit a
   real limit (custom loop, custom tool logic, specific framework).
   ([APIs](https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html))
2. You can mix: use managed building blocks (Knowledge Bases, Guardrails) from a code-first agent,
   or start managed and migrate specific parts to code as needs grow.

## GA vs Preview

- Bedrock Agents, Flows, and the OpenAI-compatible Responses/Chat Completions APIs are documented
  capabilities of Amazon Bedrock; AgentCore Harness is a documented AgentCore service (status as of
  2026-09; confirm at the sources). Endpoint recommendations can change — for new applications the
  docs currently recommend the `bedrock-runtime` endpoint.
  ([Getting started](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html))

## Pitfalls / anti-patterns

- Writing a custom agent loop when Flows/Agents/Harness would meet the requirement with less to own.
- Choosing code-first for OpenAI-SDK migrations where the Responses API is a smaller change.
  ([API compatibility](https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html))

## Verify at the live source

- APIs overview: https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html

## Sources

- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/agents-how.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/apis.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
