# Model-selection guide

Illustrative decision aid for choosing and configuring a Bedrock model. It intentionally contains
**no hard-coded model IDs, prices, or quotas** — resolve those at the live sources below.

## Steps

1. **Shortlist by capability.** Match the task (reasoning, tool use, multimodal, context length,
   language) to candidates in the model catalog. ([Models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html), [Supported foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html))
2. **Check availability.** Confirm the model (and any cross-Region inference profile) is available
   in your Region. ([Supported foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html))
3. **Confirm API compatibility.** Prefer models that support the Converse API for portability; some
   support Converse, all support InvokeModel. ([Model compatibility](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-marketplace-model-reference.html))
4. **Resolve the model ID at runtime/config**, never hard-code it. ([Find the model ID](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-api.html))
5. **Tune cost/latency:** pick a service tier, and enable prompt caching if you have a large stable
   prefix; consider intelligent prompt routing to shift easy requests to cheaper same-family models.
   ([Service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html), [Prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html), [Intelligent prompt routing](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html))
6. **Check maturity.** Confirm GA vs Preview for the model/feature before making it a production
   default.

## Verify at the live source (volatile)

- Model IDs / Regions / modalities: model catalog + Supported foundation models
- Pricing: https://aws.amazon.com/bedrock/pricing/
- Quotas: Service Quotas console

See `references/model-selection-and-converse.md` and `references/bedrock-inference-scaling.md` for
the cited detail behind each step.
