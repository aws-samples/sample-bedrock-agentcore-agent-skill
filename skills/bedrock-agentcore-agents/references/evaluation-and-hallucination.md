# Evaluation & hallucination detection

> Status labels are volatile — confirm GA/Preview and supported models/Regions at the linked sources.

## When this applies

You need to measure whether the agent is *right*, catch hallucinations, and keep quality from
regressing after launch. (Router: "Evaluate quality / catch hallucinations?")

Two distinct jobs — do both:
- **Prevent/flag at runtime** (per request): Guardrails contextual grounding + Automated Reasoning.
- **Measure over time** (dev + production): Bedrock evaluations and AgentCore Evaluations.

## Key decisions

| Need | Use |
| --- | --- |
| Catch ungrounded answers in RAG at request time | Guardrails **contextual grounding check** |
| Validate answers against formal rules/policies | Guardrails **Automated Reasoning checks** |
| Benchmark model/prompt quality in dev | **Bedrock evaluations** (incl. LLM-as-a-judge) |
| Compare RAG sources / knowledge bases | **Bedrock RAG evaluation** |
| Score the *agent's* behavior (traces, tool calls, trajectory) | **AgentCore Evaluations** — start with **built-in evaluators** |
| Detect hallucination in scoring | Built-in **`FAITHFULNESS`** + **`CORRECTNESS`** evaluators |
| Continuously watch quality in production | AgentCore Evaluations **online** (with sampling) |
| Regression-test a curated session set | AgentCore Evaluations **batch** (ground truth via session metadata) |
| Investigate one interaction / try a new evaluator | AgentCore Evaluations **on-demand** |

## Runtime hallucination controls

### Contextual grounding check
Guardrails supports contextual grounding checks to **detect and filter hallucinations** in model
responses when a reference source and user query are provided; supported use cases include
summarization, paraphrasing, and question answering. This is the primary control for RAG.
([Contextual grounding](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html), [Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))

- Best practice: enable it on any RAG/summarization path, and tune thresholds for grounding
  (is it supported by the source?) and relevance (does it answer the question?).
- Note: contextual grounding needs a **reference source** — it cannot judge open-domain answers.

### Automated Reasoning checks
Automated Reasoning checks use mathematical/formal-logic techniques to validate natural-language
content against policies you define — unlike pattern-matching filters, they give structured feedback
on whether a response is correct. ([Automated Reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html), [Guardrail components](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html))

- **Critical behavior:** they operate in **detect mode only** — they return findings rather than
  blocking. *Your application decides* what to do: serve, rewrite, ask for clarification, or fall
  back. Do not assume a bad answer is automatically suppressed.
  ([Integrate Automated Reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/integrate-automated-reasoning-checks.html))
- Best fit: domains with stateable rules (policy, eligibility, compliance answers).

> Guardrails combine multiple techniques (keyword/regex through automated reasoning) to identify
> undesirable output — implementing these by hand would be difficult and slow.
> ([GENSEC02-BP01](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html))

## Measuring quality

### Bedrock evaluations (model + RAG)
- Score model outputs, including **LLM-as-a-judge**, which scores another model's responses and
  explains each score (visible on the console Evaluations page).
  ([Evaluate resources](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html), [LLM as a judge](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html))
- **Evaluate retrieval, not just generation** — RAG evaluation compares knowledge bases/RAG sources
  so you can pick the best one. ([RAG evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html))
- Generator and evaluator models must be available in the same Region.
  ([Create judge job](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-judge-create.html))

### AgentCore Evaluations (agent behavior)
Model-level scores miss agent-specific failure modes (wrong tool, wrong order, looping). AgentCore
Evaluations provides automated assessment of how well your agent/tools perform tasks, handle edge
cases, and stay consistent. ([Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html))

- **Evaluators** analyze agent **traces** and return quantitative scores against criteria such as
  helpfulness or accuracy (plus custom business metrics), scoring at session, trace, or tool-call
  level. ([Evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluators.html), [BuiltinEvaluator](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_bedrockagentcore.BuiltinEvaluator.html))

### Start with the built-in evaluators (no configuration needed)

**Best practice: use built-in evaluators before building your own.** They are pre-configured
LLM-as-a-judge solutions — prompt templates, evaluator model, and scoring criteria already chosen —
and because they are part of the fully managed offering you can **use them immediately without
additional configuration**, with AWS improving them and adding more over time. Their configurations
**cannot be modified**, which is what keeps scores consistent and comparable across runs.
([Evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluators.html))

Available built-in evaluators and what each one catches
([BuiltinEvaluator](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_bedrockagentcore.BuiltinEvaluator.html)):

| Built-in evaluator | Evaluates |
| --- | --- |
| `FAITHFULNESS` | Whether the response is **supported by the provided context/sources** — the core hallucination signal for RAG |
| `CORRECTNESS` | Whether the information in the response is **factually accurate** |
| `RESPONSE_RELEVANCE` | Whether the response actually addresses the user's query |
| `GOAL_SUCCESS_RATE` | Whether the conversation met the user's goals |
| `INSTRUCTION_FOLLOWING` | How well the agent followed the system instructions |
| `TOOL_SELECTION_ACCURACY` | Whether the agent picked the right tool for the task |
| `TOOL_PARAMETER_ACCURACY` | How accurately it extracted parameters from the user query |
| `COHERENCE` | Whether the response is logically structured |
| `CONCISENESS` | Appropriately brief without dropping key information |
| `REFUSAL` | Agent evading or refusing to answer |
| `HARMFULNESS` | Harmful content in the response |
| `STEREOTYPING` | Generalizations about individuals or groups |

**For hallucination specifically:** pair **`FAITHFULNESS`** (is it grounded in the sources?) with
**`CORRECTNESS`** (is it factually right?). Add `RESPONSE_RELEVANCE` to catch on-topic-but-unhelpful
answers, and `REFUSAL` to catch over-refusal introduced by tightening guardrails.
For tool-using agents, `TOOL_SELECTION_ACCURACY` and `TOOL_PARAMETER_ACCURACY` catch failures that
answer-only scoring misses.

You select built-in evaluators by identifier and can mix them with custom ones in a single online
evaluation configuration, with a CloudWatch Logs data source — illustrative shape:

```text
# Illustrative: online evaluation combining built-in + custom evaluators.
# source: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_bedrockagentcore.BuiltinEvaluator.html
evaluators:
  - builtin: HELPFULNESS
  - builtin: CORRECTNESS
  - builtin: FAITHFULNESS      # hallucination signal
  - custom:  <your-evaluator>
dataSource: CloudWatch Logs (log group + service name for your agent)
```

Confirm the current evaluator list and exact API/CDK shapes at the sources before you build — the
set grows over time.

### Escalation path: built-in → third-party → custom

Work down this list; only move to the next step when the previous one can't express what you need.
You can **mix all of these in one evaluation configuration**.
([Evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluators.html))

1. **Built-in** — no configuration, managed and improved for you. Default choice.
2. **Third-party** — evaluators from the **DeepEval** and **AutoEval** open-source libraries, managed
   the same way as built-ins: select by ID and the service runs it, **no model or configuration
   required**.
3. **Derived from a base evaluator** — the middle ground people often miss: run an existing
   **built-in or third-party evaluator's logic on your own model/inference** instead of the model the
   service picks. Use this when you like the built-in criteria but must control the judge model (for
   example for consistency, region, or cost reasons).
4. **Custom evaluators** — full control, two flavors:
   - **LLM-as-a-judge**: your evaluator model, evaluation instructions, criteria, and scoring schema.
   - **Code-based**: your own **AWS Lambda** function for deterministic checks — regex matching,
     external API calls, custom metrics, or business-specific rules with **no LLM judge**. Best where
     correctness is objectively checkable (schema valid, value in range, ID exists).

Custom evaluators are most valuable for domain-specific agents, unique quality standards, or
industry-specific criteria (for example healthcare or finance) and organization-specific scoring
schemas. ([Evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluators.html), [Create evaluator](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/create-evaluator.html))

> Pattern for hallucination: start with built-in `FAITHFULNESS` + `CORRECTNESS`; if you need the same
> judgement on your own model, derive a custom evaluator from the built-in rather than writing a
> judge from scratch; add a **code-based** evaluator for any claim you can verify deterministically
> (e.g., does the cited document/ID actually exist?).
### Three evaluation types — pick per stage

| Type | What it does | Use it for |
| --- | --- | --- |
| **On-demand** | Evaluates a chosen set of spans/traces that you specify by span or trace ID | Build-time testing, trying a new custom evaluator, investigating a specific customer interaction, validating a fix |
| **Batch** | One asynchronous job across many sessions; the service handles session discovery, span collection, and scoring from a CloudWatch Logs location, returning per-evaluator averages plus per-session detail | Baseline before a change, pre/post comparison after a prompt or model update, regression testing over a curated session set, periodic quality audits |
| **Online** | Continuously samples live production traffic and scores it against multiple criteria | Ongoing production monitoring and drift detection |

([Evaluation types](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations-types.html), [AGENTOPS06-BP02](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp02.html))

Batch evaluation supports **ground truth through session metadata** — expected responses,
assertions, and expected tool trajectories — which makes it the natural home for reference-based
regression testing. ([Evaluation types](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations-types.html))

### Sampling & filtering (control cost and coverage)

Online evaluation has three parts: **session sampling and filtering**, the **evaluators** you choose
(built-in, new custom, or existing custom), and **monitoring/analysis** — aggregated scores in
dashboards, quality trends over time, drill-down into low-scoring sessions, and full
input-to-output interaction flows. ([Evaluation types](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations-types.html))

- **Percentage sampling.** Evaluate a portion of sessions (for example 10%) rather than everything.
  The sampling percentage ranges from **0.01% to 100%**. Online evaluation samples live traffic from
  CloudWatch logs at the rate you set. ([SamplingConfig](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_SamplingConfig.html), [CreateOnlineEvaluationConfig](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateOnlineEvaluationConfig.html))
- **Conditional filters** target evaluation more precisely than a blanket percentage — use them to
  focus on the traffic that matters (configuration also supports filters and a session timeout).
  ([Evaluation types](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations-types.html), [OnlineEvaluationConfigProps](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrockagentcore/OnlineEvaluationConfigProps.html))

**Best practices for sampling**
- Every sampled session runs LLM judges, so **sampling rate drives cost** — start low (a few
  percent), confirm the signal, then raise it.
- Use a **higher rate right after a release** (to catch regressions quickly) and a lower steady-state
  rate afterwards.
- Prefer **filters over a high global percentage** when you only care about specific flows (for
  example a high-risk tool path or a particular customer segment).
- Sample at **100% only** for low-volume, high-consequence traffic — or in a pre-production
  environment.
- Keep the rate stable when comparing score trends; changing it mid-comparison changes your
  denominator.
- **Traces are the input.** The `Evaluate` API accepts traces in **OpenTelemetry** format and returns
  scores with explanations — so **observability is a prerequisite** for evaluation (see
  `observability.md`). ([Evaluate API](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_Evaluate.html), [Telemetry setup](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/supported-frameworks-telemetry.html))
- **Dataset evaluations with ground truth.** Spans are collected from CloudWatch and dataset ground
  truth (`expected_response`, `assertions`, `expected_trajectory`) maps to evaluator inputs — note
  `expected_trajectory` lets you assert the *path*, not just the final answer.
  ([Dataset evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/dataset-evaluations.html))
- Custom criteria: `CreateEvaluator` defines how to assess specific aspects of behavior.
  ([Create evaluator](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/create-evaluator.html))

## Recommended approach

1. **Instrument first.** Enable Observability + ADOT/OpenTelemetry — no traces means no agent
   evaluation. ([Telemetry setup](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/supported-frameworks-telemetry.html))
2. **Add runtime controls.** Contextual grounding on RAG paths; Automated Reasoning where rules are
   stateable — and implement explicit handling of its findings (detect-only).
   ([Integrate Automated Reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/integrate-automated-reasoning-checks.html))
3. **Turn on built-in evaluators first** — no configuration required. Start with `FAITHFULNESS` and
   `CORRECTNESS` (hallucination), `RESPONSE_RELEVANCE`, and, for tool-using agents,
   `TOOL_SELECTION_ACCURACY` / `TOOL_PARAMETER_ACCURACY`. Only build custom evaluators once you have
   a gap the built-ins don't cover. ([Evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluators.html))
4. **Build a golden dataset** with expected responses/assertions/trajectories; run on-demand
   evaluations in dev and in CI. ([Dataset evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/dataset-evaluations.html))
5. **Gate rollout** on evaluation thresholds; promote pinned versions (see `testing-and-rollout.md`).
6. **Turn on online evaluation** in production with a **modest sampling percentage** (raise it after
   releases, lower it at steady state) and filters for high-risk flows; use **batch** evaluation for
   pre/post comparisons and regression runs.
   ([Evaluation types](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations-types.html), [SamplingConfig](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_SamplingConfig.html))
7. **Close the loop:** alert on score regressions alongside latency/token/error metrics, and treat a
   grounding/reasoning finding spike as an incident signal.

## GA vs Preview

- Bedrock Guardrails (contextual grounding), Bedrock evaluations, and AgentCore Evaluations are
  documented capabilities (status as of 2026-09; confirm at the sources). Automated Reasoning checks
  are **detect-only** by design — verify current behavior and supported models before relying on
  them. Some CDK evaluator constructs are `alpha` — do not make alpha modules a production default.
  ([Evaluator (CDK alpha)](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrock_agentcore_alpha/Evaluator.html))

## Pitfalls / anti-patterns

- Assuming Automated Reasoning **blocks** bad answers — it reports findings; you must act on them.
  ([Integrate Automated Reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/integrate-automated-reasoning-checks.html))
- Expecting contextual grounding to work without a reference source.
  ([Contextual grounding](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html))
- Evaluating only the final answer while ignoring the **trajectory** (tool choice/order).
  ([Dataset evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/dataset-evaluations.html))
- Evaluating only in dev — no online evaluation means silent production drift.
  ([AGENTOPS06-BP02](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp02.html))
- Scoring generation but never retrieval in RAG.
  ([RAG evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html))
- Trying to evaluate agents without instrumentation/traces.
- **Hand-rolling an LLM-as-a-judge before trying the built-in evaluators** — they need no
  configuration and are maintained/improved for you.
  ([Evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluators.html))
- Expecting to tweak a built-in evaluator's prompt/model — configurations are immutable by design;
  derive a custom evaluator from it instead if you need your own model.
  ([Evaluators](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluators.html))
- **Sampling 100% of production traffic by default** — every sampled session runs judges, so this is
  a cost surprise. Sample a percentage and use filters instead.
  ([SamplingConfig](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_SamplingConfig.html))
- Changing the sampling rate mid-comparison, which shifts the denominator and makes score trends
  misleading.
- Using online evaluation for regression testing — use **batch** with ground truth for that.
  ([Evaluation types](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations-types.html))

## Verify at the live source

- AgentCore Evaluations: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html
- Bedrock evaluations: https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html
- Guardrails: https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html

## Sources

- https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/integrate-automated-reasoning-checks.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
- https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02-bp01.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-judge-create.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations-types.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluators.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/dataset-evaluations.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/create-evaluator.html
- https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_SamplingConfig.html
- https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateOnlineEvaluationConfig.html
- https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrockagentcore/OnlineEvaluationConfigProps.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/supported-frameworks-telemetry.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_Evaluate.html
- https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06-bp02.html
- https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_bedrockagentcore.BuiltinEvaluator.html
- https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrock_agentcore_alpha/Evaluator.html
