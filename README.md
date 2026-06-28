# Commonplace

**A folder-based agent workspace.** Plain Markdown and git, that an AI agent operates as the
control plane for your business, and that you stay in front of.

Commonplace is CORBEL's flavour of a **Filesystem Agent Workspace (FAW)**: an open, file-based pattern
for an agent-run control plane. It is in the spirit of the
[Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf),
but extends it from *formatting knowledge* to *running a whole workspace*. FAW is the pattern;
Commonplace is the reference implementation you clone.

Not an autonomous AI CEO. Commonplace handles what does not need you and prepares what does, then
stops at a gate and hands you the decision. Preparation is automated; authority stays yours.

## Why

- **Plain files, no lock-in.** Markdown and YAML in a git repo. No app, no database, no service to
  depend on. Read every byte, diff every change, fork it, take it anywhere.
- **Deterministic first.** Ordinary code does the plumbing; the model enters only to summarise,
  draft, classify, or judge, never to decide or send. AI as a reasoning layer, not an authority layer.
- **It remembers.** An append-only journal is the truth; a reaper folds it into a memory that decays
  and surfaces what matters. Registers hold live state; canon holds what is settled.
- **Portable knowledge.** Frontmatter is OKF-compatible (the Open Knowledge Format), so the graph of
  what-relates-to-what travels with the files, not with a vendor.

Runs in **Claude Code** today. The doctrine, schemas, templates, and registers are agent-neutral; the
wired reflexes target Claude Code.

## Use it

Commonplace is a GitHub **template repository**:

1. Click **Use this template**, then **Create a new repository** (your own copy).
2. Clone it. Run `pip install -r requirements.txt` (one dependency: PyYAML).
3. Open the folder in **Claude Code**.
4. On the first session the workspace is uninitialised, so the agent runs the **onboarding** skill: it
   asks a handful of questions (your workspace name, your agent's name, and so on) and fills the
   template deterministically. No find-and-replace by hand.
5. You are live. Talk to your agent.

Before you ever share your own copy onward, two gates prove it is clean and portable:

```bash
python3 tools/scrub-check.py   # no in-house terms leak (you configure the list)
python3 tools/okf-check.py     # OKF-compatible frontmatter + linked knowledge graph
```

## What is inside

```text
AGENTS.md         the constitution: identity, routing, doctrine, the gate
00_meta/          how the workspace describes and governs itself
10_doctrine/      the agent's standing judgment (read, not run)
15_canon/         durable reference: your direction, brand, offerings
20_memory/        journal (append-only truth) + the folded, decaying memory
30_schemas/       the shape contract for every artefact
40_templates/     fill-in scaffolds: daily brief, decision packet, ...
50_registers/     live ledgers: decisions, loops, risks, records
60_workflows/     the run-by-hand playbooks
70_integrations/  slots for your email, CRM, and feeds (you wire these)
80_projects/      per-project trackers and their open loops
90_runs/          working artefacts
.claude/          reflex hooks + the onboarding skill
tools/            the pre-distribution gates
```

Every numbered folder has a README explaining it. Start at [`AGENTS.md`](AGENTS.md).

## How it thinks

- **Source-or-abstain.** No factual claim without a source. "I don't know" beats a confident guess.
- **Autonomy by reversibility.** The more reversible an action, the more the agent simply does it; the
  less reversible, the more it stops for you.
- **Capture-back.** Durable learning is written back to memory. Nothing evaporates.
- **One concept per file**, linked into a graph you can walk.

## Licence

MIT, © 2026 CORBEL Ltd. See [LICENSE](LICENSE). Contributions are welcome, see
[CONTRIBUTING.md](CONTRIBUTING.md).
