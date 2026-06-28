---
id: <<workspace_slug>>.meta.log
name: Workspace change log
type: log
layer: C1
status: current
owner: shared
created: <<CREATED_DATE>>
tags: [log, changelog]
---

# Workspace change log

Append-only history of structural changes to this workspace: doctrine edits, schema/workflow
additions, hook installs, migrations. One dated section per change set, newest at the top. Generic
OS improvements should also flow upstream to the Workspace-Template (see the upstreaming rule in the
template `README.md`).

## <<CREATED_DATE>> — Instantiated from the Workspace-Template

- Created this workspace from the canonical blank template. Filled the identity placeholders; wired
  the instance integrations and the shared-context path.
- Now-tier reflex hooks present (`journal-guard` PreToolUse, `session-brief` SessionStart,
  `session-digest` SessionEnd). Memory model, doctrine, schemas, templates, and workflow specs
  carried from the template. Canon, registers, and memory start blank.
