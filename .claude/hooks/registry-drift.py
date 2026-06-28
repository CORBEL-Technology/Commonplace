#!/usr/bin/env python3
"""registry-drift.py — flags components not catalogued in the component registry.

A registry that rots is worse than none. This is the drift sensor: it walks the repo for
durable moving parts (scripts, systemd units, automation workflows, hooks) and reports any whose
path is absent from 50_registers/component-registry.md, so a new component cannot quietly
escape the catalogue. Advisory only — it never blocks (exit 0).

Hook discipline (AGENTS.md): silent when clean; speaks only when a human is needed.
SessionEnd hook (optional) + runnable by hand: python3 .claude/hooks/registry-drift.py

The workspace root is taken from the <<WORKSPACE_ROOT_ENV>> env var if set, else inferred from this
file's location (repo root = two levels up from .claude/hooks/).
"""
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("<<WORKSPACE_ROOT_ENV>>") or Path(__file__).resolve().parents[2])
REGISTRY = ROOT / "50_registers" / "component-registry.md"

# Scope: OPS dirs only (the control plane that runs the workspace). Self-contained projects/apps
# are deliberately NOT scanned — they carry their own internal catalogue. Adding a project dir here
# would wrongly demand it be catalogued in the ops registry; keep this list to ops dirs.
# Conservative candidate globs: durable moving parts only (not docs, schemas, or tests).
GLOBS = [
    "70_integrations/**/*.sh", "70_integrations/**/*.py",
    "70_integrations/**/*.service", "70_integrations/**/*.timer", "70_integrations/**/*.socket",
    "70_integrations/automation/n8n/*.json",
    ".claude/hooks/*.py",
]


def candidates(root):
    """Repo-relative paths of durable components, excluding tests and bytecode."""
    out = set()
    for g in GLOBS:
        for p in root.glob(g):
            rel = p.relative_to(root).as_posix()
            if p.name.startswith("test_") or "__pycache__" in rel:
                continue
            out.add(rel)
    return sorted(out)


def uncatalogued(root=ROOT, registry=REGISTRY):
    """Candidate paths whose exact string is absent from the registry. Empty list == no drift."""
    text = registry.read_text() if registry.exists() else ""
    return [c for c in candidates(root) if c not in text]


def main():
    missing = uncatalogued()
    if missing:
        print("registry-drift: components missing from 50_registers/component-registry.md:",
              file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
    return 0          # advisory: never block the session


if __name__ == "__main__":
    sys.exit(main())
