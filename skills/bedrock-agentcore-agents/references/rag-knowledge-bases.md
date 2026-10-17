# RAG with Amazon Bedrock Knowledge Bases

> Status labels, supported models/Regions, and prices are volatile — confirm at the linked sources.

## When this applies

The agent must answer from your private or proprietary data with citations, not just model
knowledge. (Router: "Agent needs private knowledge?")

## Key decisions

- **Managed vs Customer-managed Knowledge Base.**
  - **Managed Knowledge Base**: AWS manages ingestion, indexing, storage, and retrieval; adds
    features like multi-modal ingestion, connectors (S3, SharePoint, Confluence, Google Drive,
    OneDrive, Web Crawler), document-level ACL filtering at retrieval, and native integration with
    AgentCore Gateway and Observability. ([Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))
  - **Customer-managed Knowledge Base**: you run your own RAG pipeline and vector store (for
    example Amazon OpenSearch Serverless, Aurora, or Neptune) with full control — and full
    operational responsibility. ([Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))
- **Retrieve vs RetrieveAndGenerate.** Use retrieve-only when you want to inject context into your
  own prompt/agent; use retrieve-and-generate when you want Bedrock to produce a cited answer.
  ([Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))

## Recommended approach

1. Pick managed vs customer-managed using the criteria above; most teams start managed for the
   lower operational burden. ([Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))
2. Choose embedding, re-ranking, and generation models from the supported list for your Region.
   ([Supported models & Regions for KBs](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-supported.html))
3. Keep source citations in responses so answers can be traced back to documents.
   ([Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))
4. To expose the KB as a tool to any MCP-compatible agent without custom code, use the native
   AgentCore Gateway integration (Managed KB). ([Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))
5. Layer Guardrails contextual grounding checks to catch answers not grounded in retrieved sources
   (see `guardrails.md`). ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))

## GA vs Preview

- Amazon Bedrock Knowledge Bases is a generally available capability (status as of 2026-09; confirm
  at the source). Specific connectors, parsing features, and agentic-retrieval capabilities evolve —
  check the overview for current availability. ([Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))

## Pitfalls / anti-patterns

- Assuming customer-managed gets managed-only features — third-party connectors, document-level
  permissions, and native Gateway integration are called out as Managed-only.
  ([Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html))
- Skipping grounding checks in RAG — use contextual grounding to reduce hallucination.
  ([Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html))
- Not evaluating retrieval quality before rollout (see `testing-and-rollout.md`).
  ([RAG evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html))

## Verify at the live source

- KB supported models/Regions: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-supported.html
- Pricing: https://aws.amazon.com/bedrock/pricing/

## Sources

- https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-supported.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html
