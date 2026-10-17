"""Minimal Strands + Bedrock Converse agent skeleton (illustrative).

This is a starting point, not production code. Adapt it, and verify volatile values
(model IDs, Regions) at their live sources before relying on them.

Sources:
- Strands @tool decorator: https://strandsagents.com/docs/api/python/strands.tools.decorator/
- Strands tools overview:   https://strandsagents.com/docs/user-guide/concepts/tools/
- Bedrock Converse API:      https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html
- Tool use with Converse:    https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html
- Find/confirm model IDs:    https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
"""

from strands import Agent, tool


@tool
def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in text.

    A clear docstring and type hints matter: the model uses them to decide when and how
    to call the tool.
    """
    return len(text.split())


def build_agent() -> Agent:
    # Strands is model-driven; select a Bedrock model your Region supports. The model ID is
    # illustrative — look it up in the console model catalog / Supported foundation models page.
    # See references/model-selection-and-converse.md for how to resolve model IDs at runtime.
    return Agent(
        system_prompt="You are a concise assistant. Prefer tools over guessing.",
        tools=[word_count],
    )


if __name__ == "__main__":
    agent = build_agent()
    result = agent("How many words are in this sentence?")
    print(result)

# Node/TypeScript note: Strands also provides a TypeScript SDK and an MCP client
# (https://strandsagents.com/docs/api/typescript/McpClient/). The tool + agent concepts are the same.
#
# Deploy: host this agent on AgentCore Runtime (see references/agentcore-runtime.md); the AgentCore
# starter toolkit wraps an entrypoint function as a Runtime-compatible HTTP service.
