---
id: <<workspace_slug>>.install
name: Install & onboarding
type: doc
layer: C0
status: current
owner: shared
created: <<CREATED_DATE>>
tags: [install, onboarding, setup, requirements, agent-scope]
related:
  - {ref: AGENTS.md, dimension: why, polarity: derived_from}
---

# Install & onboarding

**Commonplace**: a blank, client-shareable folder-based agent workspace, a founder control plane you
onboard once and run. This file covers requirements, the first run, and the honest agent scope.

## Requirements

- **Python 3** — the `.claude/hooks/` reflexes and the onboarding `apply.py` run on the system
  `python3` (no virtualenv assumed).
- **PyYAML** — `pip install -r requirements.txt`. Used by the memory reaper hook and by the onboarding
  engine (which reads `placeholders.yml`).
- **git** — the workspace is a git repo; onboarding discovers and snapshots files via `git ls-files`,
  and the per-folder loop/journal discipline assumes version control.

## Runtime / agent scope (honest)

This workspace is **Claude Code-first**: the runtime reflexes live in `.claude/` (hooks + skills) and
[`CLAUDE.md`](CLAUDE.md) is the canonical adapter. [`GEMINI.md`](GEMINI.md) is a thin adapter/pointer.
The real IP — the doctrine, schemas, templates, registers, and the control-plane design — is
agent-neutral and readable by any agent, but the **wired automation targets Claude Code**; other agents
get the documents with reduced reflex coverage. A neutral-core / per-agent-adapter split is a future
improvement, not a v1 claim.

## First run (onboarding)

1. On GitHub, click **Use this template** to create your own repository from Commonplace, then clone it
   and open the folder in Claude Code.
2. The [`.uninitialised`](.uninitialised) sentinel + the `SessionStart` gate
   ([`.claude/hooks/onboarding-gate.py`](.claude/hooks/onboarding-gate.py)) prompt the agent to run the
   **onboarding** skill ([`.claude/skills/onboarding/SKILL.md`](.claude/skills/onboarding/SKILL.md))
   before anything else.
3. The skill interviews you for the workspace identity (name, entity, owner, agent name, root-env, and
   the optional shared-context path), then runs
   [`apply.py`](.claude/skills/onboarding/apply.py) to fill every `<<TOKEN>>` placeholder
   deterministically (with a pre-flight snapshot and validation), seeds the registers, writes the first
   journal entry, and removes the sentinel.
4. You're live. The runtime `{{...}}` markers (e.g. `{{YYYY-MM-DD}}`) are intentional and are filled
   per-artefact as you work — they are not onboarding tokens.

## Before distributing your own copy

Run the pre-distribution gates ([`tools/README.md`](tools/README.md)) — both must exit `0`:

```bash
python3 tools/scrub-check.py   # zero in-house terms across contents, ids, filenames
python3 tools/okf-check.py     # OKF-compatible frontmatter + body-link mirroring
```

## Related

- [<<WORKSPACE_NAME>>](AGENTS.md)
