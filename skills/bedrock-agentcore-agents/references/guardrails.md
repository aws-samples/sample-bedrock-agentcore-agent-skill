# Amazon Bedrock Guardrails

> Status labels are volatile — confirm at the linked live sources.

## When this applies

You need configurable safety, privacy, or grounding controls on inputs and model responses.
(Router: "Safety / content controls?")

> For hallucination detection and quality scoring end to end (contextual grounding tuning,
> Automated Reasoning findings handling, Bedrock evaluations, and AgentCore Evaluations including
> online production evaluation), see `evaluation-and-hallucination.md`.

## Key decisions

- **Which safeguards to enable.** Bedrock Guardrails provides configurable filters: content filters
  (Hate, Insults, Sexual, Violence, Misconduct, Prompt Attack), denied topics, word filters,
  sensitive-information filters (PII block/mask, custom regex), contextual grounding checks, and
  Automated Reasoning checks. ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))
- **How to apply.** Attach a guardrail (ID + version) during inference, or call the standalone
  `ApplyGuardrail` API to evaluate content without invoking a model.
  ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))
- **Selective evaluation for RAG.** You can evaluate only part of an input (for example just user
  input, not retrieved context or history) using input tagging — available via the SDK, not the
  console. ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))

## Recommended approach

1. Create a guardrail, iterate on a working draft in the built-in test window, then cut a version to
   use in production. ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))
2. For RAG/conversational apps, enable contextual grounding checks to flag responses not grounded in
   the source (see `rag-knowledge-bases.md`). ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))
3. Use sensitive-information filters to block or mask PII in inputs and responses.
   ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))
4. Version guardrails and roll them out like any other production config (see
   `testing-and-rollout.md`).

## GA vs Preview

- Bedrock Guardrails is a documented, generally available capability with Classic and Standard
  safeguard tiers (status as of 2026-09; confirm supported Regions/models and tier features at the
  source). ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))

## Pitfalls / anti-patterns

- Testing only in the console — selective input evaluation for RAG is SDK-only.
  ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))
- Treating guardrails as a substitute for least-privilege IAM and prompt hygiene — they are one
  layer, not the whole defense.
- Shipping the working draft instead of a pinned version.
  ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))

## Verify at the live source

- Supported Regions/models and tiers: https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html

## Sources

- https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
