# Decision tree (visual)

Mermaid rendering of the `SKILL.md` router. Illustrative — see `SKILL.md` and the `references/`
files for the authoritative, cited detail.

```mermaid
flowchart TD
    A[Need an agent behavior] --> B{Do you need to write agent code?}
    B -- No, fastest/managed --> M[Managed:<br/>Harness / Bedrock Agents / Flows /<br/>Responses API]
    M --> MR[references/managed-alternatives.md]
    B -- Yes, custom control --> C[Code-first: Strands + Converse]

    C --> D{What do you need next?}
    D --> D1[Pick / call a model] --> R1[references/model-selection-and-converse.md]
    D --> D2[Add tools] --> R2[references/tools-strands-and-mcp.md]
    D --> D3[Private knowledge / RAG] --> R3[references/rag-knowledge-bases.md]
    D --> D4[Multiple agents] --> R4[references/multi-agent-patterns.md]
    D --> D5[Ship serverless] --> R5[references/agentcore-runtime.md]
    D --> D6[Memory] --> R6[references/agentcore-memory.md]
    D --> D7[Secure tools / auth] --> R7[references/agentcore-gateway-identity.md]
    D --> D8[Safety controls] --> R8[references/guardrails.md]
    D --> D9[Observe in prod] --> R9[references/observability.md]
    D --> D10[Test & roll out] --> R10[references/testing-and-rollout.md]
    D --> D11[Provision as code] --> R11[references/terraform-iac.md]
    D --> D12[IAM & cost] --> R12[references/security-iam-cost.md]
```

Sources: this diagram is a restatement of `SKILL.md`, which cites its underlying AWS/Strands docs.
