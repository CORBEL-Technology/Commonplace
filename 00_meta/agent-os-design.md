---
id: <<workspace_slug>>.meta.agent-os-design
name: Agent OS design — constitution / reflexes / playbooks / cognition / memory
type: design-spec
layer: C0
status: current
owner: shared
created: <<CREATED_DATE>>
source: design principle (operator) + verified Claude Code hook reality
tags: [agent-os, hooks, skills, subagents, constitution, instrumentation]
related:
  - {ref: AGENTS.md, dimension: what, polarity: explains}
  - {ref: 10_doctrine/autonomy-and-gates.md, dimension: how, polarity: requires}
  - {ref: 20_memory/README.md, dimension: where, polarity: requires}
---

# Agent OS design

How this workspace becomes intelligent **by instrumenting the environment**, not by lengthening the
prompt. The principle:

> `AGENTS.md` describes **judgment**. Hooks enforce **reflexes**. Skills hold **playbooks**.
> Subagents handle **heavy cognition**. The journal + registers hold **memory/evidence**.

## The mapping

| Principle layer | Lives in | Status |
|---|---|---|
| **Constitution** (judgment) | `AGENTS.md` | exists |
| **Reflexes** (enforce) | `.claude/settings.json` + `.claude/hooks/` | **installed** (journal-guard, session-brief, session-digest) |
| **Playbooks** | `.claude/skills/` (the `60_workflows/` specs graduate here when invoked often) | deferred |
| **Heavy cognition** | `.claude/agents/` subagents | deferred (no input/consumer yet) |
| **Memory / evidence** | `20_memory/journal/` (events) + `50_registers/` (observations, decisions, backlog, metrics) | **exists — reuse, do not rebuild** |

The key fit: **hooks are the sensory organs that append to the immutable journal.** The reaper folds
the journal; the subconscious spots trends. There is no parallel `ops/metrics/` tree — that collapses
into reuse of the journal + registers. No new evidence tree.

## Verified Claude Code hook reality

**Real events:** `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`,
`PostToolUseFailure`, `Stop`, `SubagentStop`, `SessionEnd`, `PreCompact`, `FileChanged`,
`Notification`, `PermissionDenied`.

**Can block (exit 2):** `PreToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`.
`PreToolUse` may return `permissionDecision` (allow/deny/ask) and fires **before** permission-rule
evaluation; deny/ask settings rules are still evaluated after the hook. Everything else
(`PostToolUse`, `PostToolUseFailure`, `FileChanged`, `SessionEnd`, `Notification`,
`PermissionDenied`) is **observational** — cannot undo or block.

**Context cost:** zero by default; a hook only adds tokens when it returns `additionalContext`
(large output is saved to a file, not injected). **Configured** in `.claude/settings.json`
(project) / `.claude/settings.local.json` (local) with matchers + types (command/http/prompt/agent).
Verify the live binary's event names before relying on any of the above — hook surfaces drift across
versions, and even a verifier can hallucinate events.

## Hook discipline (the rule that keeps this from re-bloating)

- **Silent by default.** Write to the journal/registers; return `additionalContext` only when it
  changes the current decision.

- **Block only the unsafe**, with **narrow matchers** (not a blanket BLOCK on whole tool classes —
  that is chatty and obstructive).

- **No write-only dead logs** — wire a consumer in the same step, or don't write.
- **Notify only when a human is needed.**

## Staged plan

### NOW (built / shipped with the template)

- **`AGENTS.md`** is the full constitution (operating loop, proactivity + prioritisation hierarchy,
  sensor doctrine, the OS map, definition of done). Judgment only.

- **`50_registers/improvement-backlog.md`** — where proactivity output lands, with a prose priority
  tag (do-now / suggest / log / ignore).

- **Reflex hooks** (installing them edits system settings, so it needs operator approval):
  1. **`PreToolUse` journal-immutability guard** — block `Edit`/`Write`/`rm`/`mv` targeting
     `20_memory/journal/*`. Turns the load-bearing append-only invariant into a reflex. Narrow
     matcher; silent unless it blocks.
  2. **`SessionEnd` journal digest** — append one journal event (what changed, decisions, files) so
     the session is captured as truth for the reaper. Silent (writes to `journal/`).
  3. **`SessionStart` brief** — a boot-orientation block (who you are, load shared context, read
     `00_meta/staging.md`, re-verify the newest handover) plus open `decision-queue` items and the
     per-project `## Open` loops aggregated from `80_projects/*/loops.md` (`## Closed` excluded). A few
     lines; situational awareness at near-zero cost.

### AWAIT-NEED (specced, switch on when the input exists)

- `UserPromptSubmit` task-router (deterministic classify) — once prompt volume justifies it.
- `PostToolUse` metric/data-stream detection + a `metric-scout` subagent — once the journal has real
  volume for it to scan (a subagent with no journal to read is pointless now).

- `FileChanged` data-stream scout — once there are real data streams to map.
- `.claude/skills/` — graduate a `60_workflows/` spec to a skill when it is invoked repeatedly.
- `PreCompact` snapshot — useful insurance once sessions carry heavy context.

### DEFER (no data / over-strict)

- Any statistical graduation apparatus (no events logged yet — use plain counts if/when fed).
- A broad `PreToolUse` BLOCK on send/publish/push (over-strict vs the gate's CONFIRM; match narrowly
  on `--force` / protected branches only, and only once such tooling exists here).

- `risk-reviewer` / `simplifier` subagents — reuse a review skill / a doctrine line first.

## Prioritisation (prose hierarchy, not a formula)

Proactivity without prioritisation is noise. Rank by, in order: **blocking** (unblocks the founder or
a commitment) → **strategic** (advances the locked direction) → **opportunistic** (nice-to-have).
Within that, gate each surfaced improvement: **do-now** (clearly high-impact + low-risk + reversible)
· **suggest** (worth a Decision Packet) · **log** (to the backlog) · **ignore**. No multiplicative
score with inputs we don't yet measure — that reads precise and gets hand-waved. Promote to a real
score only when the inputs (confidence, recurrence, cost-to-delay) are actually tracked.

## Emergent-intelligence refinements

The aim: a small artificial ecology where observations are born cheaply, patterns compete for
survival, useful priors bias attention, and only repeatedly-useful behaviours graduate to policy or
automation. Folded in as doctrine/targets, not new infrastructure (they activate with the await-need
feedback hooks):

- **Observation budget (3 levels).** L1 raw event: always append cheap facts (command, file, test
  result, duration). L2 semantic observation: only when anomalous / repeated / risky / inefficient /
  goal-relevant. L3 pattern candidate: only by deterministic fold after thresholds. Stops narrating
  every tiny thing.
- **Anti-superstition feedback.** The feedback hooks MUST log `prior.used` and `prior.outcome` as
  SEPARATE events; never self-validate a prior because an action was taken. Confidence moves on a
  real outcome (caught regression / confirmed signal), not on mere use. See
  `20_memory/subconscious/README.md`.
- **Nudge limits.** Priors enter context as hypotheses only: ≤3 per turn, ≤80 words, confidence
  >~0.55, source-linked, never cited as fact.
- **Promotion ladder.** observation→pattern (≥3 occurrences / 2+ distinct sessions / 14d / avg-conf
  ≥0.6) → prior (≥5 / 45d / ≥0.7 / 2+ successful uses) → **policy candidate (human review required)**.
  Decay: half-life ~14d; archive below conf 0.25 or unused 30d. These are targets; wire into
  `homeostasis.yml` only when the journal actually feeds them (no data yet — plain counts until then).
- **Prior→policy graduation requires human review** unless purely local, reversible, low-risk — the
  gate, applied to self-modification.

## What stays in `AGENTS.md` vs moves out

- **Stays (judgment):** mission, the one vocabulary, hard invariants, the gate's *intent*, the
  operating loop, the prioritisation hierarchy, the sensor doctrine, the OS map, definition of done.

- **Moves out (enforcement/inventory):** the gate's *enforcement* → a `PreToolUse` hook; long
  playbooks → skills; heavy audits → subagents; events/metrics → the journal + registers.

## Related

- [<<WORKSPACE_NAME>>](../AGENTS.md)
- [Autonomy & gates — the single decision gate](../10_doctrine/autonomy-and-gates.md)
- [Memory structure — the model](../20_memory/README.md)
