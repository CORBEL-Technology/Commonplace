# Reflex hooks

The reflexes that enforce the constitution at the tool-call boundary, so the load-bearing invariants
do not depend on the agent remembering them. Wired in [`../settings.json`](../settings.json).
Discipline (per `AGENTS.md`): silent by default, narrow matchers, no write-only logs, notify only
when a human is needed.

> Installing or changing hooks edits system settings, so it is an operator-approved change.

## The hooks

| Hook | Event | What it does | Can block? |
|---|---|---|---|
| `journal-guard.py` | `PreToolUse` | Blocks any Edit/Write/MultiEdit/Bash that would edit, overwrite, delete, or move an EXISTING `20_memory/journal/` entry. Creating a NEW entry is allowed (append-only). The reflex behind the immutability invariant. | **yes** (exit 2) |
| `session-brief.py` | `SessionStart` | Injects only open decision-queue items + open loops, and only if any exist. Silent otherwise. Situational awareness at near-zero cost. | no |
| `session-digest.py` | `SessionEnd` | Appends one terse L1 journal event (reason, last commit, working tree) so the session is captured as truth for the reaper. Silent. | no |
| `reaper.py` | `SessionEnd` | The deterministic fast memory pass (membership, decay, supersession, quarantine, tiering, build marker). Spec: `60_workflows/memory-reaper.md`. Hook-safe (a failure never disrupts session end). | no |
| `registry-drift.py` | `SessionEnd` (optional) | Advisory drift sensor: flags any ops component not catalogued in `50_registers/component-registry.md`. Silent when clean. | no |

## Hook runtime

The hooks run under the system `python3` (no venv). Four are standard-library only; `reaper.py`
additionally imports **PyYAML** (`import yaml`). Install it once with `python3 -m pip install pyyaml`
(the repo-root [`requirements.txt`](../../requirements.txt) carries it). If PyYAML is missing,
`reaper.py` raises an `ImportError` at SessionEnd and memory consolidation stops until it is installed;
the other four hooks are unaffected.

## Workspace root resolution

Each hook resolves the workspace root from the `<<WORKSPACE_ROOT_ENV>>` environment variable if set,
else two levels up from the hook file (the repo root). Set the env var only if the hooks are invoked
from outside the repo.

## Placeholders to fill at instantiation

These files carry placeholders alongside the rest of the template:

- `<<WORKSPACE_ROOT_ENV>>` — the env-var name for the root override (e.g. `ACME_ROOT`).
- `<<WORKSPACE_NAME>>` — the brief label printed by `session-brief.py`.
- `<<workspace_slug>>` — the build-marker id namespace (`reaper.py`) and the journal `where:` field
  (`session-digest.py`).
- `<<agent_slug>>` — the lowercase agent handle written to the journal `who:` field
  (`session-digest.py`).

## Tests

`reaper.py` and `registry-drift.py` have test files in the reference workspace
(`test_reaper.py`, `test_registry-drift.py`). They are not carried by the template; add them back
once the instance has real atoms/components to test against, or port them from the reference
workspace.
