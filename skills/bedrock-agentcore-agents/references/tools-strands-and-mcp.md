# Tool-using agents: Strands `@tool` and MCP

> Status labels are volatile — confirm at the linked live sources.

## When this applies

Your agent must do more than generate text — call APIs, query data, or act on systems.
(Router: "Agent needs tools?")

## Key decisions

- **`@tool` (in-process) vs MCP (out-of-process).**
  - **`@tool`**: define a Python function, decorate it, and Strands turns it into a tool with
    metadata derived from the signature and docstring. Best for logic that lives in your agent.
    ([@tool decorator](https://strandsagents.com/docs/api/python/strands.tools.decorator/), [Tools overview](https://strandsagents.com/docs/user-guide/concepts/tools/))
  - **MCP**: connect to a separate MCP server (local or remote) via the Strands MCP client. Best
    when the tool is shared, owned by another team, or already exists as a server.
    ([MCP with Strands](https://strandsagents.com/docs/learning/give-your-agent-tools-using-mcp/))
- **Direct MCP client vs AgentCore Gateway.** For enterprise access control over many tools, put
  **AgentCore Gateway** in front to convert APIs/Lambda/services into MCP tools behind one secure
  endpoint (see `agentcore-gateway-identity.md`). ([Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html))

## Recommended approach

### In-process tool with `@tool`

```python
# source: https://strandsagents.com/docs/api/python/strands.tools.decorator/
from strands import Agent, tool

@tool
def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in text."""
    return len(text.split())

agent = Agent(tools=[word_count])
agent("How many words are in this sentence?")
```

### Out-of-process tool over MCP

Strands provides an MCP client that connects to remote or local MCP servers; discovered MCP tools
are adapted into agent tools. ([MCP with Strands](https://strandsagents.com/docs/learning/give-your-agent-tools-using-mcp/), [MCP agent tool](https://strandsagents.com/docs/api/python/strands.tools.mcp.mcp_agent_tool/), [MCP example](https://strandsagents.com/docs/examples/python/mcp_calculator/))

At the model layer, tool use is also available directly through the Bedrock Converse API via
`toolConfig`, if you are not using a framework. ([Tool use with Converse](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html))

> Node/TypeScript note: Strands exposes an MCP client in its TypeScript API as well.
> ([McpClient](https://strandsagents.com/docs/api/typescript/McpClient/))

### AgentCore built-in tools (Code Interpreter & Browser)

Instead of building common capabilities yourself, AgentCore provides built-in tools that run in
secure, isolated environments:

- **Code Interpreter** — lets an agent write, execute, and debug code in a sandbox (supports
  Python, TypeScript, and JavaScript) for data processing and calculations. Use it via the
  high-level SDK client or boto3 directly.
  ([Built-in tools](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-tools.html), [Code Interpreter](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-tool.html), [Using directly](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-using-directly.html))
- **Browser** — lets an agent interact with web content in an isolated environment; you can also
  drive it programmatically with Playwright.
  ([Built-in tools how it works](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-tools-how-it-works.html), [Browser + Playwright](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-quickstart-playwright.html))

Both provide session isolation, so prefer them over hand-rolled code-exec or headless-browser
setups when you need those capabilities in production.

### Structured output (type-safe results)

When you need a typed, validated object back instead of free text, use Strands structured output:
define the schema and receive a validated object rather than parsing raw text yourself. Prefer this
over ad-hoc regex/JSON parsing of model responses.
([Structured output example](https://strandsagents.com/docs/examples/structured_output/), [structured_output tool API](https://strandsagents.com/docs/api/python/strands.tools.structured_output.structured_output_tool/))

## GA vs Preview

- Strands Agents is an open-source SDK (Apache-2.0) maintained in the `strands-agents` GitHub org;
  track releases there rather than assuming a fixed version. ([sdk-python](https://github.com/strands-agents/sdk-python))
- MCP is an open protocol; Strands' MCP support is documented in its user guide. Confirm which MCP
  capabilities are surfaced in the version you use. ([MCP with Strands](https://strandsagents.com/docs/learning/give-your-agent-tools-using-mcp/))

## Pitfalls / anti-patterns

- Vague tool docstrings/signatures — the model relies on them to decide when and how to call a
  tool. ([Tools overview](https://strandsagents.com/docs/user-guide/concepts/tools/))
- Trusting tool output blindly — treat external tool/MCP responses as untrusted input.
- Reinventing a shared tool as `@tool` in every agent when an MCP server (or Gateway target) would
  centralize it. ([Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html))

## Verify at the live source

- Strands releases/version: https://github.com/strands-agents/sdk-python
- Strands docs: https://strandsagents.com/docs/user-guide/concepts/tools/

## Sources

- https://strandsagents.com/docs/user-guide/concepts/tools/
- https://strandsagents.com/docs/api/python/strands.tools.decorator/
- https://strandsagents.com/docs/learning/give-your-agent-tools-using-mcp/
- https://strandsagents.com/docs/examples/python/mcp_calculator/
- https://strandsagents.com/docs/api/python/strands.tools.mcp.mcp_agent_tool/
- https://strandsagents.com/docs/api/typescript/McpClient/
- https://strandsagents.com/docs/examples/structured_output/
- https://strandsagents.com/docs/api/python/strands.tools.structured_output.structured_output_tool/
- https://github.com/strands-agents/sdk-python
- https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-tools.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-tools-how-it-works.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-tool.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-using-directly.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-quickstart-playwright.html
- https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-3-strands-agents-mcp/
