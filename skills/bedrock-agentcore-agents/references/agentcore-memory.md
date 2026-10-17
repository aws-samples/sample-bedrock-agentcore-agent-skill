# AgentCore Memory

> Status labels are volatile — confirm at the linked live sources.

## When this applies

Your agent needs to remember context within a conversation and/or across sessions.
(Router: "Remember across turns/sessions?")

## Key decisions

- **Short-term vs long-term memory.** AgentCore Memory supports short-term memory for multi-turn
  conversations and long-term memory that persists across sessions, with control over what the
  agent remembers and learns. ([AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html), [Memory getting started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-getting-started.html))
- **Shared vs per-agent memory.** Memory stores can be shared across agents, so multiple agents can
  learn from the same experiences. ([AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html))
- **Framework integration.** Memory integrates with frameworks including Strands, LangGraph,
  LangChain, and LlamaIndex. ([AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html))

## Recommended approach

1. Create and manage a Memory resource, then implement short-term (in-conversation) and, where
   useful, long-term (cross-session) memory. ([Memory getting started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-getting-started.html), [Get started with Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-get-started.html))
2. Be deliberate about what you persist — store only what improves future responses; keep sensitive
   data out unless required and protected (see `security-iam-cost.md`).
3. For secure, policy-controlled access to Memory, you can place an AgentCore Gateway in front of
   Memory so authentication and access-control move out of app code into infrastructure.
   ([Memory via gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-connector.html))
4. Trace memory reads/writes via Observability spans (see `observability.md`).
   ([Memory observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-memory-metrics.html))

## GA vs Preview

- AgentCore Memory is a documented AgentCore capability (status as of 2026-09; confirm at the
  source). ([Memory getting started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-getting-started.html))

## Pitfalls / anti-patterns

- Persisting everything by default — bloats storage/cost and increases privacy risk.
- Storing PII in long-term memory without access controls or a retention policy.
- Sharing a memory store across agents that should not see each other's context.
  ([AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html))

## Verify at the live source

- Memory docs: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-getting-started.html

## Sources

- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-getting-started.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-get-started.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-connector.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-memory-metrics.html
