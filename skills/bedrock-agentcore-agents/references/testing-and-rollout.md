# Testing & rollout

> Status labels are volatile — confirm at the linked live sources.

## When this applies

You want to measure quality before shipping and roll out changes safely.
(Router: "Validate before/at rollout?")

## Key decisions

- **How to evaluate.** Amazon Bedrock evaluations can measure model and RAG-source performance,
  including LLM-as-a-judge scoring where one model scores another's responses and explains the
  score. ([Evaluate resources](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html), [LLM as a judge](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html))
- **Evaluate retrieval, not just generation.** RAG evaluations let you compare Knowledge Bases and
  other RAG sources to pick the best one. ([RAG evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html))
- **Pin versions for rollout.** Version guardrails and other configs so you promote known-good
  artifacts (see `guardrails.md`). ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))

## Recommended approach

1. Build an evaluation set representative of real tasks; run model and/or RAG evaluations and read
   scores and explanations in the console Evaluations page.
   ([Evaluate resources](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html), [LLM as a judge](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html))
2. For a judge-based job, ensure generator and evaluator models are available in the same Region.
   ([Create judge job](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-judge-create.html))
3. Gate rollout on evaluation thresholds; promote pinned versions of models/guardrails/prompts.
4. After deploy, watch Observability metrics (latency, token usage, error rate) and compare against
   the pre-rollout baseline (see `observability.md`).
   ([Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html))

## GA vs Preview

- Amazon Bedrock evaluations (including RAG and LLM-as-a-judge) are documented capabilities (status
  as of 2026-09; confirm supported models/Regions at the source). Judge criteria and defaults can
  change over time. ([Define evaluation methods](https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompt-optimization-evaluation.html))

## Pitfalls / anti-patterns

- Shipping without an evaluation baseline, so regressions are invisible.
- Evaluating generation while ignoring retrieval quality in RAG systems.
  ([RAG evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html))
- Promoting a "latest/draft" config instead of a pinned version.

## Verify at the live source

- Evaluation docs: https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html

## Sources

- https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-judge-create.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompt-optimization-evaluation.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html
