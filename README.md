# sample-bedrock-agentcore-agent-skill

A **community sample** Agent Skill (packaged as an [Agent Plugins](https://agent-plugins.org) v1
plugin) that helps you build AI agents on **Amazon Bedrock** and **Amazon Bedrock AgentCore**. It
is a decision router: point your agent (or yourself) at it and it maps a use case to the right stack and the right reference file.

> This is a community sample and **not** an official AWS distribution. It is not released, endorsed,
> or supported by AWS. Content was authored clean-room from official primary sources; see
> [`PROVENANCE.md`](PROVENANCE.md).

## What's inside

```
plugin.json                         # Agent Plugins v1 manifest (validates against the 1.0.0 schema)
skills/bedrock-agentcore-agents/
  SKILL.md                          # the router: decision tree + progressive disclosure
  references/                       # one file per domain, loaded on demand
  assets/                           # decision-tree diagram, Terraform + IAM templates, agent.py, checklist
PROVENANCE.md                       # file -> source-URL ledger + clean-room method
LICENSE                             # MIT-0 (MIT No Attribution)
```

The skill under `skills/bedrock-agentcore-agents/` is self-contained: copy that folder on its own
and it still works.

## Domains covered

Model choice + Bedrock Converse API · tools with Strands `@tool` / MCP · RAG with Bedrock Knowledge
Bases · multi-agent patterns · serverless production on AgentCore Runtime · AgentCore Memory ·
Gateway + Identity · Guardrails · observability · testing & rollout · Terraform-first IaC ·
security/IAM/cost · and when a managed alternative (Bedrock Agents, Flows, Responses API) fits
better than code-first.

## Install & use

This is a standard **Agent Skill**, so it works in any client that supports the
[Agent Skills](https://github.com/agentskills/agentskills) standard. Install it once, then just
describe what you want to build — the client loads the skill when your request matches its
`description` (progressive disclosure: metadata first, then `SKILL.md`, then references on demand).

```bash
git clone <this-repo>
git clone https://github.com/ThejashreeNeralakere/sample-bedrock-agentcore-agent-skill.git
cd sample-bedrock-agentcore-agent-skill

### What to copy

**Copy exactly one folder: `skills/bedrock-agentcore-agents/`**

It is self-contained — all internal links are relative and one level deep — so it works on its own
with no dependency on anything else in this repo. Copy the **whole folder**, not individual files:

```
skills/bedrock-agentcore-agents/        <-- COPY THIS ENTIRE FOLDER
├── SKILL.md                            required  the router; the client reads this first
├── references/   (19 files)            required  loaded on demand by SKILL.md
└── assets/       (9 files)             optional  templates you copy when building
    ├── decision-tree.md
    ├── service-selection-matrix.md
    ├── model-selection-guide.md
    ├── agent/agent.py
    ├── iam/bedrock-invoke-least-privilege.json
    ├── terraform/{guardrail,knowledge-base,agentcore-runtime-role}/
    └── checklists/production-readiness.md
```

`SKILL.md` alone will load, but it routes to `references/` — so dropping those loses the actual
content. Keep the folder intact.

**Do not copy these into your skills directory** (they are repo-level, not part of the skill):

| Not copied | Why |
| --- | --- |
| `plugin.json` | Agent Plugins manifest — **only** used when installing as a Kiro Power (see below), where you point at the repo root instead of copying |
| `PROVENANCE.md`, `LICENSE`, `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` | Repo governance/provenance; the skill declares `license: MIT-0` in its own frontmatter so licensing travels with it |
| `tests/`, `.kiro/specs/` | Repo validation and authoring history |

**One exception — Kiro Power:** you don't copy anything. You point Kiro at the **repo root** (the
folder containing `plugin.json`) and it reads `plugin.json` + `skills/` itself.

### Kiro

Kiro supports both the plugin wrapper (a **Power**) and plain skills
([Powers](https://kiro.dev/docs/powers/), [Skills](https://kiro.dev/docs/skills)).

**As a Power** (keyword activation + one-click updates):
1. Open the **Powers** panel (Ghosty icon with the lightning bolt)
2. **Add Custom Power** → **Import power from a folder** (or from this repo's Git URL)
3. Select the repo root (the folder containing `plugin.json`) → **Install**

**As a plain skill:**
```bash
cp -r skills/bedrock-agentcore-agents ~/.kiro/skills/     # all workspaces
cp -r skills/bedrock-agentcore-agents .kiro/skills/       # this workspace only
```
Also available as the `/bedrock-agentcore-agents` slash command. Manage under
**Agent Steering & Skills**.

### Claude Code

Skills live in `.claude/skills/`
([docs](https://code.claude.com/docs/en/slash-commands)):
```bash
cp -r skills/bedrock-agentcore-agents ~/.claude/skills/   # personal, all projects
cp -r skills/bedrock-agentcore-agents .claude/skills/     # project-scoped
```

### Codex

Codex reads skills from `~/.agents/skills` (global) or `.agents/skills` (repo)
([docs](https://developers.openai.com/codex/concepts/customization/)):
```bash
mkdir -p ~/.agents/skills
cp -r skills/bedrock-agentcore-agents ~/.agents/skills/   # global
cp -r skills/bedrock-agentcore-agents .agents/skills/     # repo-scoped
```
Codex uses the same progressive disclosure model and can select the skill implicitly from its
description, or you can invoke it explicitly.

### GitHub Copilot

Copilot looks in `.github/skills`, `.claude/skills`, or `.agents/skills` (project) and
`~/.copilot/skills` or `~/.agents/skills` (personal)
([docs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-skills)):
```bash
cp -r skills/bedrock-agentcore-agents ~/.copilot/skills/  # personal
cp -r skills/bedrock-agentcore-agents .github/skills/     # project
```
Agent skills work with the Copilot cloud agent, Copilot code review, the Copilot CLI, the Copilot
app, and agent mode in VS Code.

> **Tip — one location for Codex *and* Copilot:** both read `~/.agents/skills`, so a single copy
> there covers both.

### Verify the copy

After copying, confirm the skill landed intact (adjust the path for your client):

```bash
SKILL_DIR=~/.claude/skills/bedrock-agentcore-agents   # or ~/.kiro/skills/... , ~/.agents/skills/... , ~/.copilot/skills/...

test -f "$SKILL_DIR/SKILL.md" && echo "SKILL.md: ok" || echo "SKILL.md: MISSING"
echo "references: $(ls "$SKILL_DIR"/references/*.md 2>/dev/null | wc -l | tr -d ' ')  (expect 19)"
echo "assets:     $(find "$SKILL_DIR/assets" -type f 2>/dev/null | wc -l | tr -d ' ')  (expect 9)"
```

The folder name must stay `bedrock-agentcore-agents` — it has to match the `name` in `SKILL.md`
frontmatter, or clients will reject the skill.

### Then prompt naturally

You don't open reference files by hand. Try:

- "Build a customer-support agent on AWS that answers from our PDFs and remembers each customer
  across sessions."
- "Productionize my Strands agent on AgentCore Runtime with guardrails, observability, and Terraform."
- "Which built-in evaluators should I use to catch hallucinations?"
- "Write least-privilege IAM for a Bedrock agent."

**How to tell the skill loaded.** The answer should cite official AWS/Strands URLs, lead with the
managed-vs-code-first decision, prefer the Converse API over `InvokeModel`, mention the AgentCore
Runtime ARM64 + `/invocations` + `/ping` container contract, and flag Preview features instead of
defaulting to them. Generic advice with no citations means it didn't load.

### Reading it directly (no client)

1. Open [`skills/bedrock-agentcore-agents/SKILL.md`](skills/bedrock-agentcore-agents/SKILL.md)
2. Follow the decision tree to the reference file(s) for your use case
3. Use the `assets/` templates as starting points when you build

## Important: volatile facts

This sample never hard-codes prices, quotas, current model IDs, or GA/Preview status. Where those
matter, it links to the live source (AWS console, model cards, pricing, quotas). **Always confirm
time-sensitive details at the source before relying on them.** Anything labeled **Preview** should
not be used as a production default.

## Provenance & licensing

- Authored only from official primary sources (AWS docs/blogs, Strands docs, official AWS GitHub
  orgs, the Terraform Registry, and package indexes). Every recommendation carries an inline
  citation; the full mapping is in [`PROVENANCE.md`](PROVENANCE.md).
- Licensed under **MIT-0 (MIT No Attribution)** — see [`LICENSE`](LICENSE).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Note: contributing this sample to `aws-samples` requires
confirming with **AWS Open Source Program Office (OSPO)** and signing the **Contributor License
Agreement (CLA)** first — this has not been done yet.
