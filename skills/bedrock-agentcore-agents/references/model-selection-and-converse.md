# Model selection & the Bedrock Converse API

> Status labels, model IDs, Regions, and prices are volatile — confirm at the linked live sources.

## When this applies

You are picking a foundation model and calling it from code, and you want one interface that works
across models. (Router: "Pick / call a model?")

## Key decisions

- **Which model?** Match capability (reasoning, tool use, multimodal, context length), Region
  availability, and cost to your task. Browse candidates and their IDs in the model catalog rather
  than memorizing them. ([Models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html), [Supported foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html))
- **Which API?** Prefer the **Converse API** for a consistent, model-agnostic message interface so
  you write code once and swap models. ([Using the Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html))
- **Region-agnostic model ID vs cross-Region inference profile?** The model ID is Region-agnostic;
  cross-Region inference profiles route across Regions in a geography. Choose based on availability
  and resilience needs. ([Supported foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html))

## Recommended approach

1. Find a model ID from the console model catalog or `ListFoundationModels`; do not hard-code a
   specific ID in long-lived guidance. ([Find the model ID](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-api.html))
2. Call `Converse` for single responses or `ConverseStream` for streaming. `Converse` needs
   `bedrock:InvokeModel`; `ConverseStream` needs `bedrock:InvokeModelWithResponseStream`.
   ([Using the Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html))

```python
# source: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html
import boto3

client = boto3.client("bedrock-runtime")  # region from env/config

# MODEL_ID is illustrative — look up the current ID for your Region in the console model catalog.
MODEL_ID = "<your-model-id>"

response = client.converse(
    modelId=MODEL_ID,
    system=[{"text": "You are a concise assistant."}],
    messages=[{"role": "user", "content": [{"text": "Summarize the Converse API in one line."}]}],
    inferenceConfig={"maxTokens": 512, "temperature": 0.2},
)
print(response["output"]["message"]["content"][0]["text"])
```

- **Tool use** is part of Converse: pass tool definitions in `toolConfig`; the model may return a
  request to run a tool, and you return the result back in the next turn.
  ([Call a tool with the Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html))

> Node/TypeScript note: the AWS SDK for JavaScript v3 exposes the same `Converse`/`ConverseStream`
> operations on the Bedrock Runtime client; the message shape is the same.
> ([Using the Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html))

### Service tier (request-time cost/latency lever)

Bedrock offers four inference service tiers — Reserved, Priority, Standard, and Flex — selected per
request to trade off availability, latency, and cost. Pick the tier deliberately per workload rather
than accepting a default. ([Service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html), [Converse API reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html))
For routing, batching, and reserved capacity, see `bedrock-inference-scaling.md`.

### Prompt caching (repeated context)

If your prompt has a long, stable prefix (e.g., a large system prompt or an uploaded document)
reused across queries, prompt caching lets the model skip recomputation of that prefix at reduced
input-token rates and lower latency. Support is model-specific — confirm before relying on it.
([Prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html))

## GA vs Preview

- The Converse API and the model catalog are documented as generally available capabilities of
  Amazon Bedrock (status as of 2026-09; confirm at the source). Individual models can have their
  own availability and access requirements — some require submitting use-case details.
  ([Using models with Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/foundation-models-reference.html))

## Pitfalls / anti-patterns

- Hard-coding a model ID in durable code or docs — IDs and availability change; resolve them at
  runtime or configuration. ([Supported foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html))
- Assuming every model supports Converse — most do, but confirm compatibility.
  ([Model compatibility](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-marketplace-model-reference.html))

## Verify at the live source

- Model IDs / Regions: model catalog + [Supported foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- Pricing: [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)

## Sources

- https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/inference-api.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/foundation-models-reference.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-marketplace-model-reference.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
