# Hosting any framework on AgentCore (+ A2A)

> Status labels are volatile — confirm at the linked live sources.

## When this applies

You built (or want to build) an agent in a framework other than Strands, and want to run it on
AgentCore — or you need agent-to-agent (A2A) interoperability. (Router: "Host any framework on
AgentCore?")

## Key decisions

- **Framework-agnostic runtime.** AgentCore works with any framework — including CrewAI, LangGraph,
  LlamaIndex, Google ADK, and Strands Agents — and any foundation model in or outside Bedrock, so
  the runtime choice does not lock your framework. ([AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html), [Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html))
- **Contract, not framework, is what matters.** Whatever the framework, a custom container must meet
  the Runtime contract — ARM64 image exposing `/invocations` and `/ping` (see
  `agentcore-runtime.md`). ([Get started without the CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html))
- **A2A for agent-to-agent.** AgentCore supports the A2A protocol by acting as a proxy layer; A2A
  servers run as stateless, streamable HTTP servers per the A2A protocol contract. ([Deploy A2A servers](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html), [A2A protocol contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a-protocol-contract.html))

## Recommended approach

1. Keep the agent's entrypoint framework-neutral; let the AgentCore SDK/toolkit wrap it, or build a
   custom container to the contract. ([Interfaces](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/develop-agents.html))
2. Choose the protocol for your workload: HTTP for request/response and streaming, A2A for
   agent-to-agent, MCP for tool servers (see `tools-strands-and-mcp.md`). ([HTTP contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-http-protocol-contract.html), [A2A contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a-protocol-contract.html))
3. Reuse the same AgentCore building blocks (Memory, Gateway, Identity, Observability) regardless of
   framework. ([AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html))

> IaC note: the AWS CDK provides an AgentCore construct library that also documents this
> framework-agnostic support. ([CDK AgentCore construct](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrock_agentcore_alpha/README.html))

## GA vs Preview

- Framework-agnostic Runtime and A2A support are documented AgentCore capabilities (status as of
  2026-09; confirm at the sources). CDK AgentCore constructs are published as an `alpha` module —
  treat alpha modules as not-for-production-default and pin versions. ([CDK AgentCore construct](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrock_agentcore_alpha/README.html))

## Pitfalls / anti-patterns

- Assuming a framework is "unsupported" — Runtime is framework-agnostic; the container contract is
  the real requirement. ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html))
- Running an A2A server on the wrong port/path or as stateful — follow the A2A contract.
  ([A2A contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a-protocol-contract.html))

## Verify at the live source

- AgentCore dev guide: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html

## Sources

- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/develop-agents.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-http-protocol-contract.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a-protocol-contract.html
- https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrock_agentcore_alpha/README.html
