# Multi-agent patterns

> Status labels are volatile — confirm at the linked live sources.

## When this applies

One agent is doing too much, or distinct responsibilities (research vs writing vs review) benefit
from isolation. (Router: "Multiple cooperating agents?")

## Key decisions

- **Single agent vs multiple agents.** Add agents only when separation of concerns or isolated
  context windows help. Each Strands agent keeps its own isolated context; a specialist can do the
  heavy work and hand back a synthesized result. ([Agents as tools](https://strandsagents.com/docs/learning/multi-agent-patterns-agents-as-tools/))
- **Orchestration shape.** Strands offers several multi-agent primitives — choose by control flow:
  - **Agents-as-tools** — a central orchestrator decides which specialist (exposed as a tool) to
    call. ([Agents as tools](https://strandsagents.com/docs/learning/multi-agent-patterns-agents-as-tools/))
  - **Graph** — each node is a full agent; you connect agents with edges expressing dependencies,
    and the graph resolves what runs in parallel vs waits. Use when the execution order is known
    upfront. ([Graph workflows](https://strandsagents.com/docs/learning/multi-agent-patterns-graph-workflows/))
  - **Swarm** — agents collaborate as a team with shared context and autonomous hand-offs (agents
    decide whether to hand off or finish). Use when routing is dynamic, not fixed.
    ([Agent swarms](https://strandsagents.com/docs/learning/multi-agent-patterns-agent-swarms/), [swarm API](https://strandsagents.com/docs/api/python/strands.multiagent.swarm/))
  - **Workflow** — specialized roles run in a defined sequence (e.g., research → fact-check →
    report). ([Workflow example](https://strandsagents.com/docs/examples/python/agents_workflows/))
  - See also the AWS blog on advanced Strands orchestration for tradeoffs.
    ([Advanced orchestration (AWS blog)](https://aws.amazon.com/blogs/machine-learning/customize-agent-workflows-with-advanced-orchestration-techniques-using-strands-agents))
- **Cross-agent interoperability (A2A).** For agent-to-agent communication across processes/teams,
  use the A2A protocol; AgentCore Runtime can host A2A servers (see `frameworks-on-agentcore.md`).
  ([Deploy A2A servers](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html))
- **Where it runs.** AgentCore Runtime supports multi-agent and multi-modal agentic workloads and
  works with any framework, so multi-agent systems can be deployed without custom infrastructure.
  ([AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html))

## Recommended approach

1. Start with one agent; split only when a role's context or logic clearly diverges.
   ([Agents as tools](https://strandsagents.com/docs/learning/multi-agent-patterns-agents-as-tools/))
2. Model specialists as tools of an orchestrator so the orchestrator controls flow and only
   relevant, synthesized information crosses agent boundaries.
   ([Agents as tools](https://strandsagents.com/docs/learning/multi-agent-patterns-agents-as-tools/))
3. For cross-team or cross-process agents/tools, standardize on MCP and front them with AgentCore
   Gateway (see `agentcore-gateway-identity.md`). ([Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html))
4. Deploy the composed system on AgentCore Runtime for session isolation.
   ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html))

## GA vs Preview

- Multi-agent support on AgentCore Runtime and Strands multi-agent patterns are documented
  capabilities (status as of 2026-09; confirm at the sources). Newer discovery/interoperability
  services may be Preview — for example AWS Agent Registry is documented as Preview.
  ([Agent Registry (Preview)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html))

## Pitfalls / anti-patterns

- Multiplying agents without a reason — more agents means more latency, cost, and failure surface.
- Passing whole conversation histories between agents instead of synthesized hand-offs, defeating
  context isolation. ([Agents as tools](https://strandsagents.com/docs/learning/multi-agent-patterns-agents-as-tools/))

## Verify at the live source

- Strands multi-agent docs: https://strandsagents.com/docs/learning/multi-agent-patterns-agents-as-tools/
- AgentCore capabilities: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html

## Sources

- https://strandsagents.com/docs/learning/multi-agent-patterns-agents-as-tools/
- https://strandsagents.com/docs/learning/multi-agent-patterns-graph-workflows/
- https://strandsagents.com/docs/learning/multi-agent-patterns-agent-swarms/
- https://strandsagents.com/docs/api/python/strands.multiagent.swarm/
- https://strandsagents.com/docs/examples/python/agents_workflows/
- https://aws.amazon.com/blogs/machine-learning/customize-agent-workflows-with-advanced-orchestration-techniques-using-strands-agents
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html
