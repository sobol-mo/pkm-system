---
name: session-close-bundle
description: Use when closing a Digital Mind PKM work block or Hermes session; record completed work, preserve one continuation, verify artifacts, and close the session without losing state.
version: 1.0.0
author: Digital Mind project
license: MIT
metadata:
  adapted_from: multi-agent-system/skills/session-close-bundle
  hermes:
    tags: [pkm, session, handoff, continuity, state]
---

Purpose

Close a PKM work block so the next curator can continue from project and STATE artifacts without chat history. This is the PKM-specific procedure; MAS transport closure remains governed by the deployed curator contract and the applicable STATE SOP.

When to use

Use at the end of a logical PKM work block, before handing a task back to the requester, or when the Hermes session is ending. Use it even when the chat session may continue after the work block.

Authority boundaries

The PKM project owns ontology meaning, vault reconciliation, PKM skills, and canonical-vault writes.
MAS owns deployed identity, STATE routing, leases, sessions, task transitions, and return delivery.
The curator may update PKM project continuity files only when the task explicitly includes project maintenance or session close.
Do not modify course materials, MAS role packages, or unrelated project repositories.
Do not infer Maxim's approval, ontology decisions, or canonical-vault write authority from session closure.

Procedure

1. Read the applicable PKM project router, current SESSION_HANDOFF.md, BACKLOG.md when task state matters, and the deployed curator AGENTS.md.
2. Record completed PKM project work in the project-defined history location. If no DEVLOG.md exists, keep the durable completion summary in SESSION_HANDOFF.md and do not invent a second history file.
3. Keep SESSION_HANDOFF.md limited to one active continuation or an explicit no-active-item decision. Include last verified state, exact next action, blockers, repository state, and governing artifacts. Remove completed detail from the continuation section.
4. Update BACKLOG.md only when this work changed an item's status, acceptance, blocker, or completion state. Do not create, reorder, or refine unrelated items.
5. If the completed block may contain reusable knowledge, invoke project-knowledge-handoff. Record no_reusable_yield when the result is transient, mutable project state, duplicated, unsupported, or not bounded. Do not create a handoff merely because a session ended.
6. For a STATE task, verify the exact task, lease, session, handoff, result, and inbox notice paths. Return the PKM result and handoff before terminally closing the task. Archive consumed inbox residue according to the applicable MAS SOP.
7. Re-read every changed artifact and verify exact paths, digests, requested mode, write authority, and read-back evidence. Distinguish runtime success from semantic completion.
8. Run the focused PKM validation required by the task. For canonical-vault work, run the vault health checker after the write and read back the changed pages. For contracts, run `python3 skills/project-knowledge-handoff/scripts/validate_contracts.py --fixtures` or the task-specific validation command.
9. Review git status and the diff in every repository touched. Use `git-agent-commit`, never bare `git commit`, when the task authorizes a project commit. Push only when the project workflow and task authorize it.
10. Close the Hermes session only after durable project and STATE artifacts are consistent. A successful model response is not session closure.

Required closeout record

State what changed, what was verified, what remains deferred, the exact next action, and the repository/STATE status. Preserve unresolved ontology conflicts and approval gaps explicitly. Do not report a canonical write unless the exact approved request or envelope was written and read back successfully.

Verification checklist

- project router and authority boundaries were followed
- SESSION_HANDOFF.md contains only current continuation
- BACKLOG.md reflects only changed work state
- reusable knowledge was assessed without forcing an ingest
- STATE task, lease, session, handoff, result, and inbox residue are terminally consistent
- exact write authority and requested mode were verified
- focused PKM validation and read-back evidence exist
- commit authorship and push policy were followed when applicable
- no project skill or runtime copy was created
