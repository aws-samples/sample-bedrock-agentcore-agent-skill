#!/usr/bin/env python3
"""Smoke test for the sample-bedrock-agentcore-agent-skill package.

Runs structural, self-containment, and provenance checks that do NOT require network
access, plus optional live checks when run with --online.

Usage:
    python3 tests/smoke_test.py            # offline structural checks
    python3 tests/smoke_test.py --online   # also HTTP-check every cited URL

Exit code 0 = all checks passed, 1 = at least one failure.

This is original tooling for the sample (no external sources). Dependencies are optional:
jsonschema and PyYAML improve coverage; the test falls back to manual checks if they are absent.
"""
from __future__ import annotations
import glob
import json
import os
import re
import sys
from urllib.parse import urlparse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join("skills", "bedrock-agentcore-agents")
SCHEMA_URL = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
INTENDED_REPO = "https://github.com/aws-samples/sample-bedrock-agentcore-agent-skill"

ALLOW_HOSTS = {
    "docs.aws.amazon.com", "aws.amazon.com", "github.com", "raw.githubusercontent.com",
    "strandsagents.com", "registry.terraform.io", "docs.hashicorp.com",
    "developer.hashicorp.com", "pypi.org", "npmjs.com", "agent-plugins.org", "aws.github.io",
}

# Repo-level docs (README/CONTRIBUTING) may additionally cite the official documentation of the
# agent clients this skill installs into. These are TOOLING/INSTALL references, not provenance for
# any AgentCore domain claim, so they are permitted only in repo docs — never in skill content.
CLIENT_DOC_HOSTS = {
    "kiro.dev",            # Kiro Powers / Skills
    "code.claude.com",     # Claude Code skills
    "docs.claude.com",     # Claude Agent SDK skills
    "developers.openai.com",  # Codex skills
    "docs.github.com",     # GitHub Copilot agent skills
}
REPO_DOC_FILES = {"README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"}
ALLOW_GH_ORGS = {"aws", "awslabs", "aws-samples", "aws-ia", "strands-agents", "agentskills", "hashicorp"}
URL_RE = re.compile(r'https?://[^\s)\]"\'>`]+')

results: list[tuple[bool, str]] = []


def check(cond: bool, label: str) -> None:
    results.append((bool(cond), label))
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")


def read(path: str) -> str:
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def all_content_files() -> list[str]:
    files = ["plugin.json", "LICENSE", "README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"]
    files += [os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, SKILL, "**", "*"), recursive=True)
              if os.path.isfile(p)]
    return files


def test_manifest() -> None:
    print("\n== plugin.json ==")
    doc = json.loads(read("plugin.json"))
    check(doc.get("$schema") == SCHEMA_URL, "manifest targets the 1.0.0 schema")
    check(doc.get("name") == "sample-bedrock-agentcore-agent-skill", "manifest name uses sample-* convention")
    name_ok = bool(re.match(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$", doc.get("name", ""))) \
        and 1 <= len(doc.get("name", "")) <= 64
    check(name_ok, "manifest name matches schema pattern/length")
    try:
        import jsonschema  # type: ignore
        import urllib.request
        schema = json.load(urllib.request.urlopen(SCHEMA_URL, timeout=30))
        errs = list(jsonschema.Draft202012Validator(schema).iter_errors(doc))
        check(not errs, "manifest validates against live schema" + ("" if not errs else f" ({errs})"))
    except Exception as exc:  # offline or no jsonschema
        allowed = {"$schema", "name", "version", "description", "author", "homepage",
                   "repository", "license", "keywords", "extensions"}
        check(set(doc) <= allowed, f"manifest has only allowed keys (schema check skipped: {type(exc).__name__})")


def test_skill_frontmatter() -> None:
    print("\n== SKILL.md frontmatter (Agent Skills spec) ==")
    txt = read(f"{SKILL}/SKILL.md")
    check(txt.startswith("---\n"), "SKILL.md starts with YAML frontmatter")
    fm_raw = txt.split("---\n")[1]
    try:
        import yaml  # type: ignore
        fm = yaml.safe_load(fm_raw)
    except Exception:
        fm = {}
        m = re.search(r'^name:\s*(\S+)', fm_raw, re.M)
        if m:
            fm["name"] = m.group(1)
    check(fm.get("name") == "bedrock-agentcore-agents", "name matches parent directory")
    desc = fm.get("description", "")
    check(0 < len(desc) <= 1024, f"description present and <=1024 chars (len={len(desc)})")
    body = txt.split("---\n", 2)[-1]
    check(len(body.splitlines()) < 500, f"SKILL.md body < 500 lines ({len(body.splitlines())})")


def test_links_and_self_containment() -> None:
    print("\n== links & self-containment ==")
    md = glob.glob(os.path.join(REPO, SKILL, "**", "*.md"), recursive=True)
    py = glob.glob(os.path.join(REPO, SKILL, "**", "*.py"), recursive=True)
    link_re = re.compile(r'\]\((?!https?://|#)([^)]+)\)')
    broken, escapes = [], []
    skill_abs = os.path.join(REPO, SKILL)
    for f in md + py:
        base = os.path.dirname(f)
        for m in link_re.finditer(open(f, encoding="utf-8").read()):
            target = m.group(1).split("#")[0]
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(resolved):
                broken.append((os.path.relpath(f, REPO), target))
            if not resolved.startswith(skill_abs):
                escapes.append((os.path.relpath(f, REPO), target))
    check(not broken, f"no broken intra-skill links ({broken})")
    check(not escapes, f"no links escape the skill root (self-contained) ({escapes})")


def test_router() -> None:
    print("\n== router resolves use cases -> reference files ==")
    txt = read(f"{SKILL}/SKILL.md")
    expected = [
        "model-selection-and-converse", "tools-strands-and-mcp", "rag-knowledge-bases",
        "multi-agent-patterns", "agentcore-runtime", "agentcore-memory",
        "agentcore-gateway-identity", "guardrails", "observability",
        "testing-and-rollout", "terraform-iac", "security-iam-cost", "managed-alternatives",
        "bedrock-inference-scaling", "frameworks-on-agentcore", "deployment-targets",
        "use-case-playbooks", "governance", "evaluation-and-hallucination",
    ]
    for name in expected:
        rel = f"references/{name}.md"
        routed = rel in txt
        exists = os.path.isfile(os.path.join(REPO, SKILL, rel))
        check(routed and exists, f"{rel} routed & present")


def test_provenance() -> None:
    print("\n== provenance coverage ==")
    prov = read("PROVENANCE.md")
    missing = [f for f in all_content_files() if os.path.basename(f) not in prov]
    check(not missing, f"every content file appears in PROVENANCE.md ({missing})")


def test_citation_hosts() -> None:
    print("\n== citation allow-list ==")
    off, gh = [], []
    # The manifest's own identity URLs (where this repo lives) are not provenance citations.
    self_urls = set()
    try:
        manifest = json.loads(read("plugin.json"))
        for field in ("repository", "homepage"):
            if manifest.get(field):
                self_urls.add(manifest[field])
                self_urls.add(manifest[field] + ".git")
    except Exception:  # noqa: BLE001
        pass
    files = glob.glob(os.path.join(REPO, SKILL, "**", "*"), recursive=True)
    files += [os.path.join(REPO, x) for x in ("README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "plugin.json")]
    for f in files:
        if not os.path.isfile(f):
            continue
        try:
            content = open(f, encoding="utf-8").read()
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        rel = os.path.relpath(f, REPO)
        allowed = ALLOW_HOSTS | (CLIENT_DOC_HOSTS if rel in REPO_DOC_FILES else set())
        for u in URL_RE.findall(content):
            if u in self_urls:
                continue
            host = urlparse(u).netloc.lower()
            if host and host not in allowed:
                off.append((rel, u))
            if host in ("github.com", "raw.githubusercontent.com"):
                parts = urlparse(u).path.strip("/").split("/")
                if parts and parts[0] not in ALLOW_GH_ORGS:
                    gh.append((rel, u))
    check(not off, f"all cited hosts on allow-list ({off})")
    check(not gh, f"all GitHub links point to official orgs ({gh})")


def test_no_hardcoded_model_ids() -> None:
    print("\n== volatile facts ==")
    mid = re.compile(r'\b(anthropic|amazon|meta|mistral|ai21|cohere)\.[a-z0-9-]+-v\d')
    hits = [os.path.relpath(f, REPO) for f in glob.glob(os.path.join(REPO, SKILL, "references", "*.md"))
            if mid.search(open(f, encoding="utf-8").read())]
    check(not hits, f"no hard-coded model IDs in references ({hits})")


def test_syntax() -> None:
    print("\n== asset syntax ==")
    for jf in glob.glob(os.path.join(REPO, SKILL, "**", "*.json"), recursive=True):
        try:
            json.load(open(jf, encoding="utf-8"))
            ok = True
        except Exception:
            ok = False
        check(ok, f"valid JSON: {os.path.relpath(jf, REPO)}")
    import py_compile
    for pf in glob.glob(os.path.join(REPO, SKILL, "**", "*.py"), recursive=True):
        try:
            py_compile.compile(pf, doraise=True)
            ok = True
        except Exception:
            ok = False
        check(ok, f"python compiles: {os.path.relpath(pf, REPO)}")
    for tf in glob.glob(os.path.join(REPO, SKILL, "**", "*.tf"), recursive=True):
        txt = open(tf, encoding="utf-8").read()
        check(txt.count("{") == txt.count("}"), f"balanced braces (HCL sanity): {os.path.relpath(tf, REPO)}")


def test_online() -> None:
    print("\n== online: every cited URL resolves ==")
    import urllib.request
    import ssl
    ctx = ssl.create_default_context()
    urls = set()
    for f in glob.glob(os.path.join(REPO, "**", "*"), recursive=True):
        if not os.path.isfile(f) or ".git" in f:
            continue
        try:
            urls.update(URL_RE.findall(open(f, encoding="utf-8").read()))
        except (UnicodeDecodeError, IsADirectoryError):
            pass
    urls.discard(INTENDED_REPO)
    # Exclude this repo's own identity URLs: they may be private or not yet published.
    try:
        manifest = json.loads(read("plugin.json"))
        for field in ("repository", "homepage"):
            if manifest.get(field):
                urls.discard(manifest[field])
                urls.discard(manifest[field] + ".git")
    except Exception:  # noqa: BLE001
        pass
    bad = []
    for u in sorted(urls):
        status = "?"
        for method in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(u, method=method, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
                    status = r.status
                    break
            except Exception as exc:  # noqa: BLE001
                status = getattr(exc, "code", type(exc).__name__)
        # Accept any non-error status: 2xx OK, 3xx is a valid redirect (docs sites move paths).
        if not (isinstance(status, int) and status < 400):
            bad.append((status, u))
    check(not bad, f"all {len(urls)} cited URLs reachable (2xx/3xx) ({bad})")


def main() -> int:
    print("Smoke test: sample-bedrock-agentcore-agent-skill")
    test_manifest()
    test_skill_frontmatter()
    test_links_and_self_containment()
    test_router()
    test_provenance()
    test_citation_hosts()
    test_no_hardcoded_model_ids()
    test_syntax()
    if "--online" in sys.argv:
        test_online()
    passed = sum(1 for ok, _ in results if ok)
    total = len(results)
    print(f"\n{'=' * 48}\nRESULT: {passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
