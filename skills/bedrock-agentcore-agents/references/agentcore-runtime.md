# Serverless production on AgentCore Runtime

> Status labels and prices are volatile — confirm at the linked live sources.

## When this applies

You have working agent code and want to run it in production without managing servers.
(Router: "Ship it serverless to prod?")

## Key decisions

- **Runtime vs rolling your own hosting.** AgentCore Runtime is a secure, serverless runtime for
  deploying and scaling agents and tools, with fast cold starts, session isolation, built-in
  identity, and support for long-running/async and multi-modal/multi-agent workloads.
  ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), [AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html))
- **Framework choice is open.** Runtime works with any framework (Strands, LangGraph, CrewAI,
  others) and any model, so you are not locked in. ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html))
- **How to package.** The AgentCore Python SDK wraps your agent function as an HTTP service
  compatible with Runtime; the starter toolkit/CLI scaffolds and deploys it.
  ([Runtime starter toolkit](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-getting-started-toolkit.html), [Interfaces](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/develop-agents.html))

## Runtime contract (common gotcha)

If you deploy a custom container instead of using the SDK/toolkit, you must satisfy the Runtime
contract:

- The agent must be packaged as a **Docker container built for ARM64** — AgentCore requires ARM64
  architecture for all deployed agents.
- It must expose an **`/invocations` (POST)** endpoint and a **`/ping` (GET)** endpoint.
  ([Get started without the CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html), [Runtime how it works](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html))
- Each user session runs in a **dedicated microVM** with isolated CPU, memory, and filesystem, which
  prevents cross-session data contamination.
  ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html))
- Runtime provides the infrastructure (isolation, scaling, sessions, auth gating, observability
  plumbing) while the agent logic is your code — this is the split vs AgentCore Harness.
  ([Harness vs Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-vs-runtime.html))

Building for x86_64, or missing either endpoint, is a common deployment failure — build ARM64 and
implement both endpoints. Time-bound platform requirements can change (for example a MicroVM
Metadata Service version requirement); check the troubleshooting page for current contract details.
([Runtime troubleshooting](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-troubleshooting.html))

## Recommended approach

1. Develop locally with your framework (for example Strands); keep the agent entrypoint a plain
   function. ([Interfaces](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/develop-agents.html))
2. Use the AgentCore starter toolkit/CLI to scaffold, test locally, deploy, and invoke.
   ([Get started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-starter-toolkit.html), [Runtime toolkit](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-getting-started-toolkit.html))
3. Rely on Runtime session isolation for per-session state, and add AgentCore Memory for
   persistence (see `agentcore-memory.md`).
4. Enable Observability from day one (see `observability.md`) and scope the execution role tightly
   (see `security-iam-cost.md`).
5. Provision repeatably with Terraform (see `terraform-iac.md`).

> Requirements note: the AgentCore starter toolkit documents a minimum Python version (3.10+ at the
> time of writing). Confirm the current requirement before you build.
> ([Get started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html))

## GA vs Preview

- AgentCore Runtime and the starter toolkit are documented capabilities of Amazon Bedrock AgentCore
  (status as of 2026-09; confirm at the sources). Some adjacent services are Preview (for example
  AWS Agent Registry) — do not make Preview services production defaults.
  ([Agent Registry (Preview)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html))

## Pitfalls / anti-patterns

- Baking long-term state into a single session instead of using Memory.
- Deploying without observability or with an over-broad execution role.
- Assuming synchronous-only behavior — Runtime also supports extended/async execution.
  ([Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html))
- Building an x86_64 image or omitting `/invocations` or `/ping` — violates the Runtime contract.
  ([Runtime contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html))

## Verify at the live source

- AgentCore dev guide: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- Pricing: https://aws.amazon.com/bedrock/agentcore/pricing/ (confirm current AgentCore pricing)

## Sources

- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-getting-started-toolkit.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/develop-agents.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-starter-toolkit.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-vs-runtime.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-troubleshooting.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html
