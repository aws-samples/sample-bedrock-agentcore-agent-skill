# AgentCore Gateway + Identity

> Status labels are volatile — confirm at the linked live sources.

## When this applies

You need to expose tools to agents securely, connect to existing MCP servers, or authenticate
callers and downstream calls. (Router: "Expose tools securely / auth?")

## Key decisions

- **Gateway as the single entry point.** AgentCore Gateway is a fully managed AI gateway that gives
  a single, secure entry point for agentic traffic, connecting agents to tools, other agents, and
  models. It can convert APIs, Lambda functions, and existing services into MCP tools, and connect
  to pre-existing MCP servers. ([Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), [AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html))
- **Inbound vs outbound auth.** When you create a gateway you choose an inbound authorizer type
  that determines how callers authenticate and what identity is available to access-control
  policies; outbound auth governs how the gateway calls downstream targets.
  ([Gateway with Memory target](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-setup.html))
- **Push enforcement into infrastructure.** Putting a gateway in front of a resource (for example
  Memory) moves authentication and access-control out of application code into the gateway.
  ([Memory via gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-connector.html))

## Recommended approach

1. Front shared tools/resources with a Gateway so every call is authenticated and policy-checked at
   one place. ([Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html))
2. Create the gateway and pick the inbound authorizer type deliberately (for example a Cognito-based
   authorizer). ([Gateway setup](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-setup.html), [Authenticated agent tutorial](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-getting-started-cognito.html))
3. Use AgentCore Identity to build authenticated agents end to end.
   ([Identity getting started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-getting-started-cognito.html))
4. For fine-grained authorization on gateway tools, use **Policy in AgentCore**, which uses
   **Cedar** — an open-source, human-readable, schema-validated policy language from AWS — to
   provide precise, verifiable access control (you can also author policies in natural language).
   ([Policy core concepts](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html), [Understanding Cedar](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-understanding-cedar.html), [Getting started with Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-getting-started.html))
5. Scope IAM for gateway targets to least privilege (see `security-iam-cost.md`).

## GA vs Preview

- AgentCore Gateway and Identity are documented AgentCore capabilities (status as of 2026-09;
  confirm at the sources). The Gateway quick start notes prerequisites such as Node.js 18+ and
  Python 3.10+ for tooling — confirm current requirements. ([Gateway quick start](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-quick-start.html))

## Pitfalls / anti-patterns

- Embedding tool authentication in each agent instead of centralizing at the gateway.
  ([Memory via gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-connector.html))
- Choosing an inbound authorizer without mapping who should be allowed to call which tools.
  ([Gateway setup](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-setup.html))
- Over-permissioning outbound targets (Lambda/APIs) reachable through the gateway.

## Verify at the live source

- Gateway docs: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html
- Identity docs: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-getting-started-cognito.html

## Sources

- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-quick-start.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-setup.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-gateway-connector.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-getting-started-cognito.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-understanding-cedar.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-getting-started.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
