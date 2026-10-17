# Observability

> Status labels are volatile — confirm at the linked live sources.

## When this applies

You need to trace, debug, and monitor agent behavior and performance in production.
(Router: "See what's happening in prod?")

## Key decisions

- **What you get by default vs what needs instrumentation.** AgentCore Observability gives
  real-time visibility through CloudWatch-powered dashboards and telemetry for metrics such as
  session count, latency, duration, token usage, and error rates. For agents in AgentCore Runtime,
  a set of session metrics is generated automatically; richer span/trace data requires
  instrumenting your agent code. ([Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html), [Service-provided data](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-service-provided.html), [Configure](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html))
- **Coverage across resources.** Built-in metrics span runtime, memory, gateway, built-in tools,
  and identity resource types, viewable on the CloudWatch generative AI observability page.
  ([Telemetry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html), [Configure](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html))
- **OpenTelemetry-based.** AgentCore Observability is OpenTelemetry-compatible; to get the full
  range of telemetry across all AgentCore services you instrument your code with the **AWS Distro
  for OpenTelemetry (ADOT)** SDK, and traces cover the full invocation path (request → LLM inference
  → tool calls → memory access → response). ([CloudWatch: AgentCore getting started](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AgentCore-GettingStarted.html), [Agentic AI Lens: tracing](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentrel08-bp02.html))

## Recommended approach

1. Enable Observability early and view metrics on the CloudWatch GenAI Observability page.
   ([Get started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-get-started.html), [View data](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-view.html))
2. Instrument your agent code with the ADOT (OpenTelemetry) SDK to emit spans/traces so you get
   relationship-level detail (for example memory event-to-memory spans), beyond default metrics.
   ([CloudWatch: AgentCore getting started](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AgentCore-GettingStarted.html), [Configure](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html), [Memory metrics](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-memory-metrics.html))
3. Watch latency, token usage, and error rate as first-class SLOs; alert on regressions.
   ([Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html))

## GA vs Preview

- AgentCore Observability is a documented capability powered by CloudWatch (status as of 2026-09;
  confirm at the source). ([Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html))

## Pitfalls / anti-patterns

- Relying only on default metrics — without ADOT/OpenTelemetry code instrumentation you miss
  span/trace detail. ([CloudWatch: AgentCore getting started](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AgentCore-GettingStarted.html), [Configure](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html))
- No alerting on token usage or error rate, so cost/quality regressions go unnoticed.

## Verify at the live source

- Observability docs: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html

## Sources

- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-service-provided.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-telemetry.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-get-started.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-view.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-memory-metrics.html
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AgentCore-GettingStarted.html
- https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentrel08-bp02.html
