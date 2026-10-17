# Contributing

Thanks for your interest in improving this community sample. Contributions must preserve the
clean-room provenance that lets this repository be licensed MIT-0.

## Before contributing to aws-samples

This sample is structured for potential contribution to `aws-samples`, but that is **not yet
cleared**. Before any contribution to an AWS org:

1. Confirm with the **AWS Open Source Program Office (OSPO)**.
2. Sign the **Contributor License Agreement (CLA)**.

Do not open a PR to an AWS org until both are done.

## Clean-room rules (non-negotiable)

1. **Author only from official primary sources** on this allow-list:
   - `docs.aws.amazon.com`, `aws.amazon.com/blogs`
   - `strandsagents.com` and the `strands-agents` GitHub org
   - official AWS GitHub orgs: `aws`, `awslabs`, `aws-samples`, `aws-ia`
   - `registry.terraform.io` (`hashicorp/aws`, `hashicorp/awscc`)
   - boto3 docs, `pypi.org`, `npmjs.com`
   - format specs `agent-plugins.org` and the `agentskills` spec (for package structure only)
2. **Never** consult, copy, paraphrase, or restructure any pre-existing third-party AgentCore skill
   or plugin. If someone pastes such content, do not use it as a source.
3. Use **original phrasing**; only short, attributed quotes from docs — no large verbatim copying.
4. Every best practice, recommendation, and code snippet needs an **inline citation** to the
   official URL it was written from.
5. **Never hard-code volatile facts** (prices, quotas, current model IDs, GA/Preview status) —
   point to the live source instead.
6. **Label features GA or Preview**, and never recommend a Preview feature as a production default.

## Provenance is part of the change

When you add or edit an authored file:
- Add or update its row in [`PROVENANCE.md`](PROVENANCE.md) (file → source URLs, verification date).
- Live-verify each cited URL; if a URL can't be verified, flag it inline as `[unverified: <url>]`
  and mirror it in the `PROVENANCE.md` "Flagged / unverified" section.

## Skill format

- Keep `SKILL.md` under ~500 lines; push detail into `references/`.
- Keep intra-skill links relative and one level deep so the skill stays self-contained.
- Validate `plugin.json` against the Agent Plugins 1.0.0 schema and `SKILL.md` frontmatter against
  the Agent Skills specification.

## Smoke test

Run the package validator before opening a PR:

```bash
python3 tests/smoke_test.py            # offline: schema, frontmatter, links, provenance, syntax
python3 tests/smoke_test.py --online   # also HTTP-checks every cited URL returns 200
```

It exits non-zero on any failure. Optional deps (`jsonschema`, `PyYAML`) improve coverage; the test
falls back to manual checks if they are absent.

## Reporting issues

Open an issue describing the problem and the official source that supports the correction.
