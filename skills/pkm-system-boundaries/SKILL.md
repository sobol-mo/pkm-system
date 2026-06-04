---
name: pkm-system-boundaries
description: Decide boundaries between PKM system artifacts and PKM knowledge state, especially when a research/design repo starts turning into the live knowledge base.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [pkm, architecture, information-architecture, obsidian, git, sync]
    related_skills: [pkm, pkm-ingest, pkm-query, pkm-lint, multimodal-source-ingest, obsidian]
---

# PKM System Boundaries

## When to use

Use this skill when:
- a PKM or digital-mind project started as research/design and gradually became the live knowledge system
- one repository contains both system artifacts and the growing knowledge corpus
- git is being used both as version control and as cross-device sync for notes/data
- the user is unsure whether they are building the system, filling the system, or both
- backlog, architecture, implementation notes, and knowledge pages have started to mix

## Core distinction

Treat these as different entities:

System artifacts
Architecture, schemas, workflows, code, agents, prompts, migration scripts, backlog, operational docs.
These are naturally versioned in git.

Knowledge state
Concepts, links, thought pages, extracted sources, evolving personal knowledge content, and graph-like state.
This behaves more like application data than source code.

The main failure mode is pretending both are the same thing because markdown makes them look similar.

## Diagnostic signs of unhealthy mixing

- The project folder became the default place for storing any useful thought, not only system-design material.
- Backlog items mix research of the PKM itself with population of the PKM.
- Knowledge growth creates pressure against normal git workflows.
- Commits stop representing meaningful implementation changes and start representing state churn.
- The user keeps git mainly because push/pull is the fastest way to get the vault onto another device.

## Default recommendation

Separate meta-level from object-level.

Recommended split:
- system/ or meta/: architecture, design decisions, backlog, implementation notes, automation, schemas
- knowledge/ or wiki/: the live knowledge state
- inside knowledge/, any given topic such as Digital Mind is only one domain among others

If the live knowledge base spans many life domains, the top-level container should be PKM or knowledge-oriented, not named after one project that happened to start it.

## Three-layer refinement for live PKM deployments

In practice, two buckets are often not enough.
A durable PKM setup usually wants three distinct layers:

- setup/meta: repo-managed system artifacts, workflows, schemas, ADRs, automation
- canonical human-facing knowledge state: the vault or note corpus the human reads and edits across devices
- derived machine state: indexes, embeddings, graph DBs, caches, and other rebuildable serving artifacts

This matters because the canonical knowledge state and the derived machine state may both be non-versioned, but they do not have the same operational model.
The knowledge state is human-facing and sync-first.
The derived machine state is server-facing and rebuildable.

Do not collapse a synced PKM vault into generic server-side UserData just because both are non-versioned.
UserData-like runtime state is typically server-only and backup-oriented.
A PKM vault is cross-device human knowledge state and needs its own sync contract.

For systems built around Obsidian or markdown-first workflows, the usual recommendation is:
- keep setup/meta in git
- keep the canonical vault outside the system repo and outside server-only runtime data areas
- treat search indexes, vector stores, LightRAG/Chroma/SQLite artifacts, and similar machine layers as derived state generated from the canonical vault

## Versioning rule of thumb

Version the system.
Do not force source-control semantics onto the full live knowledge state unless there is a specific operational reason.

## Project-owned skill boundary for PKM systems

When a PKM project has its own agent workflows, treat those skills as part of the PKM system layer, not as ad hoc runtime state.

Default rule:
- canonical PKM project skills live in the project repo under `skills/`
- Hermes runtime paths such as `~/.hermes/skills/...` are deployment or compatibility bridges, not the source of truth
- avoid two writable copies of the same PKM skill in both places

Practical pattern:
- keep the canonical skill package in the project repo
- point Hermes at that repo-owned directory via `skills.external_dirs` when appropriate
- if old runtime paths must keep working, make them symlink bridges back to the project-owned directories

Pitfall:
Agents often drift back to `~/.hermes/skills/` because default skill-creation flows write there unless explicitly redirected. For PKM-system work, after creating or modifying a skill, verify that the canonical edit landed in the project-owned `skills/` tree rather than only in the runtime bridge path.

Git is a good fit for:
- code
- config
- schemas
- workflows
- curated docs
- export snapshots
- small human-reviewed subsets of knowledge

Git is a poor primary fit for:
- rapidly growing note/state collections
- graph-like content with constant link churn
- database-like records whose main need is sync and availability, not commit history

## If git is being used for sync

Name the reality clearly: this is replication convenience, not proof that git is the right storage model.

Do not over-interpret the presence of markdown files in a repo as evidence they should all stay versioned together.

Typical next step:
- keep git for the system repo
- move live knowledge state to a sync-oriented store or vault workflow
- optionally keep scheduled or manual exports/snapshots of the state in git for backup, audit, or portability

## Decision framework

Ask these questions:
1. Is this file describing how the system works, or is it the changing content the system holds?
2. Would a commit history here be used to understand design decisions, or only because sync is convenient?
3. If this content scaled 100x, would git still be the intended operating model?
4. Is the current top-level name describing the container, or only the project that started it?

If answers split between system and state, separate them.

## Migration guidance

Minimal migration path:
1. Freeze the naming problem first: identify the container and the domain.
2. Move architecture/backlog/implementation material into a dedicated system area.
3. Reclassify the current knowledge corpus as state, not project documentation.
4. Decide whether the knowledge state remains markdown-first, becomes DB-backed, or uses a hybrid model.
5. Keep cross-device access as an explicit requirement, but solve it with a sync strategy rather than accidental git semantics.
6. If machine indexes or graph stores exist, classify them as derived state and keep them separate from the canonical human-edited corpus.

Practical default for Obsidian-style PKM:
- repo: setup/meta only
- synced vault: canonical notes, sources, idea dumps, domain folders
- server runtime: rebuildable retrieval/indexing layer fed from the synced vault

## Drift Guardrail

This project has an automated drift guard to catch when PKM skills end up outside the project-owned tree.

### Deterministic check

`scripts/check_pkm_drift.py` — checks whether `~/.hermes/skills/note-taking/` contains any real (non-symlink) directories that look like PKM skills not owned by `pkm-system`.

- Exit 0 = clean
- Exit 1 = drift detected
- Exit 82 = error

A cron job (`pkm-drift-detector`, runs every 60m) alerts this topic when drift is found.
The cron uses a trampoline at `~/.hermes/scripts/check-pkm-drift.sh`; the real implementation stays project-owned.

### Rules for agents in this topic

This Telegram topic is dedicated to PKM project work only.
Before any action:

1. Load `pkm-system/AGENTS.md` and the relevant PKM skills (`pkm-ingest`, `pkm-system-boundaries`, etc.)
2. Run `check_pkm_drift.py` (or verify the cron shows clean) before creating new PKM scripts or skills
3. Before `skill_manage(action='create')` for anything PKM-related, check whether an existing project skill covers the need — extend it rather than create a standalone copy
4. If you must create a new skill, put it in `~/.hermes/agents-projects/pkm-system/skills/<name>/`, NOT in `~/.hermes/skills/note-taking/` directly
5. If you write a reusable script, put it in `~/.hermes/agents-projects/pkm-system/scripts/`. Use a minimal trampoline in `~/.hermes/scripts/` only when a Hermes runtime constraint (e.g. cron) requires it
6. After any PKM-related write, verify it landed in the project-owned tree, not only in a runtime bridge path

### What drift looks like

A real directory (not a symlink) inside `~/.hermes/skills/note-taking/` whose name overlaps with PKM project concerns.
The opposite — a project-owned skill that has no bridge symlink — is not drift, just a missing bridge.

## Pitfalls

- Calling the drift a mistake. Often it is discovery of the real system boundary.
- Keeping everything together because early structure was convenient.
- Treating sync needs as versioning needs.
- Letting one topic name become the container name for all future knowledge.
- Designing from file format similarity instead of lifecycle similarity.

## Output pattern

When advising the user, be explicit:
- state that the issue is boundary confusion, not user inconsistency
- distinguish system artifacts from knowledge state
- say whether the current repo is acting as VCS, sync layer, or both
- recommend a top-level separation and name the two halves
- avoid forcing an immediate storage technology choice if the architectural distinction can be made first

## References

- references/digital-mind-boundary-case.md — concrete case where a Digital Mind research repo evolved into a broader PKM knowledge environment and git was retained mainly for cross-device replication
- references/pkm-vault-vs-userdata-vs-derived-state.md — practical boundary guide for separating synced human-facing vaults from server-only runtime data and rebuildable machine indexes

## Overlap notice

`pkm-system-boundaries` and `pkm-ingest` both define session-start conventions for PKM project work. `pkm-ingest` carries the automation-boundary and thought-note rules. `pkm-system-boundaries` carries the drift-guardrail and topic-awareness rules. These are complementary concerns (what vs. when to check), not duplicates — the boundary is clean if the agent loads both before PKM work.
