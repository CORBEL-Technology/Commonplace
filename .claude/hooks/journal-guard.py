#!/usr/bin/env python3
"""PreToolUse reflex: enforce the journal append-only/immutable invariant.

Blocks the agent from editing, overwriting, deleting, or moving an EXISTING entry under
20_memory/journal/. Creating a NEW journal entry is allowed (append-only). Silent unless it blocks.
Fail-open on any parse error so it never wedges the agent on its own bug.

The workspace root is taken from the <<WORKSPACE_ROOT_ENV>> env var if set, else inferred from this
file's location (repo root = two levels up from .claude/hooks/).
"""
import sys, os, json, re
from pathlib import Path

ROOT = Path(os.environ.get("<<WORKSPACE_ROOT_ENV>>") or Path(__file__).resolve().parents[2])
JOURNAL = (ROOT / "20_memory" / "journal").resolve()


def under_journal(p):
    try:
        rp = Path(p).expanduser()
        if not rp.is_absolute():
            rp = ROOT / rp
        rp = rp.resolve()
        return rp == JOURNAL or JOURNAL in rp.parents
    except Exception:
        return False


def block(msg):
    sys.stderr.write("[journal-guard] " + msg + "\n")
    sys.exit(2)  # exit 2 blocks the tool call before it runs


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    tool = data.get("tool_name") or data.get("tool") or ""
    ti = data.get("tool_input") or data.get("toolInput") or {}

    if tool in ("Edit", "MultiEdit", "NotebookEdit"):
        fp = ti.get("file_path") or ti.get("notebook_path") or ""
        if fp and under_journal(fp):
            block(f"journal/ is append-only and immutable. Refusing to {tool} an existing journal "
                  f"entry ({fp}). A correction or retraction is a NEW journal entry.")
    elif tool == "Write":
        fp = ti.get("file_path") or ""
        if fp and under_journal(fp):
            try:
                exists = Path(fp).expanduser().exists()
            except Exception:
                exists = False
            if exists:
                block(f"journal/ is append-only. Refusing to overwrite an existing journal entry "
                      f"({fp}). Write a NEW entry instead.")
    elif tool == "Bash":
        cmd = ti.get("command") or ""
        if "20_memory/journal" in cmd:
            destructive = (
                re.search(r'\b(rm|mv|truncate|shred)\b', cmd)
                or re.search(r'sed\s+-i', cmd)
                or re.search(r'(?<!>)>(?!>)\s*[^|&;]*20_memory/journal', cmd)  # single '>' overwrite, not '>>'
            )
            if destructive:
                block("Refusing a Bash command that deletes, moves, or overwrites journal entries "
                      "(20_memory/journal is append-only). Append a NEW entry instead (>> is fine).")
    sys.exit(0)


if __name__ == "__main__":
    main()
