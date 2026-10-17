# Bedrock inference scaling & cost levers

> Prices, quotas, tiers, and supported models are volatile — confirm at the linked live sources.

## When this applies

You need to control latency, throughput, availability, or cost of Bedrock inference beyond a single
on-demand call — routing, batching, reserved capacity, or caching. (Router: "Batch / cost-routing /
capacity?")

## Key decisions

- **Service tier.** Bedrock offers four inference service tiers — Reserved, Priority, Standard, and
  Flex — to trade off availability, latency, and cost; tier selection is a request-time choice.
  ([Service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html), [Capacity & performance](https://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html))
- **Route across models automatically.** Intelligent prompt routing gives a single serverless
  endpoint that predicts per-request response quality and routes within a model family, to balance
  quality and cost. ([Intelligent prompt routing](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html))
- **Batch vs real-time.** For large, latency-tolerant workloads, batch inference processes many
  requests from S3 in one job. ([Batch inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html))
- **Dedicated capacity.** Provisioned Throughput reserves capacity for custom/imported models (and
  is required for some custom-model inference paths). ([Provisioned Throughput API](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-thru-api.html))
- **Prompt caching.** For long, repeated prompt prefixes (e.g., a large stable system prompt),
  prompt caching reuses cached context at reduced input-token rates and lower latency. ([Prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html))

## Recommended approach

1. Start on an on-demand tier (Standard/Flex/Priority share a per-model quota); pick the tier per
   workload's latency/cost needs. ([Service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html))
2. For agents with large stable system prompts, enable prompt caching — it is a high-impact cost
   lever for agentic workloads. ([Prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html), [Agentic AI Lens: caching](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentcost02-bp03.html), [GenAI Lens: caching](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gencost03-bp03.html))
3. Move offline/bulk work (evals, backfills, enrichment) to batch inference instead of real-time.
   ([Batch inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html))
4. Use intelligent prompt routing to keep quality while shifting easy requests to cheaper models in
   the same family. ([Intelligent prompt routing](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html))
5. Reserve Provisioned Throughput only when you have predictable, sustained demand or need it for a
   custom model. ([Provisioned Throughput](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-thru-api.html))

## GA vs Preview

- Service tiers, intelligent prompt routing, batch inference, Provisioned Throughput, and prompt
  caching are documented Bedrock capabilities (status as of 2026-09; confirm supported models,
  Regions, and tiers at the sources). Prompt caching and routing support specific model sets — check
  before relying on them for a given model. ([Prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html), [Intelligent prompt routing](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html))

## Pitfalls / anti-patterns

- Paying real-time rates for work that could be batched.
  ([Batch inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html))
- Reserving Provisioned Throughput for spiky/low-volume workloads.
- Assuming caching or routing works for every model — support is model-specific.
- Treating tier as a global setting — it is a per-request parameter.
  ([Service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html))

## Verify at the live source

- Pricing: https://aws.amazon.com/bedrock/pricing/
- Quotas: Service Quotas console + Bedrock quotas docs
- Supported models for caching/routing: the pages linked above

## Sources

- https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/prov-thru-api.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
- https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gencost03-bp03.html
- https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentcost02-bp03.html
