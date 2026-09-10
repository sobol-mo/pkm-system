---
name: project-knowledge-handoff
description: Use when closing project work that may yield reusable PKM knowledge. Decide whether a handoff is warranted, then prepare or validate the PKM-owned immutable contract without writing to the vault.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pkm, project, handoff, knowledge-yield, validation]
    related_skills: [pkm, pkm-ingest, pkm-system-boundaries]
---

Purpose

This is the PKM-owned procedure that participating projects call from their own session-close workflow. It decides whether completed work produced reusable knowledge and defines the handoff boundary. It does not make this check a global MAS gate and does not authorize producer-side vault writes.

Authority

The producing project owns its completed work context, authoritative artifacts, and bounded candidate selection.
Digital Mind owns ontology meaning, reconciliation, ingest rules, validation, and canonical vault writes.
MAS may route the package but does not own its semantic meaning.
Maxim retains ontology decisions and approval of any canonical write bound to the exact envelope digest.

Knowledge-yield decision procedure

At the close of a logical work block, inspect only completed, source-backed outputs. Decide whether they contain stable knowledge that is useful outside the immediate task.

Use these criteria together:

1. Stability: the claim, concept, relation, decision, pattern, process, goal, constraint, or artifact meaning is no longer transient work-in-progress.
2. Reusability: a future agent, project, course module, or decision could use it without replaying the whole work block.
3. Evidence: an immutable producer artifact supports it.
4. Boundedness: the producer can name explicit identifiers or another finite selection.
5. Authority safety: the candidate can be proposed without copying mutable project state or bypassing PKM review.

Record exactly one decision:

no_reusable_yield
The close workflow ends without creating a PKM task or envelope. Briefly record why the output is task-local, transient, duplicated, unsupported, or mutable project state.

reusable_yield
Create one pkm-knowledge-handoff.v1 envelope. Point it to immutable producer artifacts. Do not copy their semantic content into the envelope. Select consultation, proposal, or canonical_ingest according to the authority already granted for this work block.

Stop and defer when stability, identity, relation meaning, evidence, or human authority is unresolved. Put the question in unresolved_questions; consultation may be requested, but consultation is read-only and is not approval.

Never treat repository paths, branches, current status, milestones, assignments, runtime state, or backlog entries as reusable semantic yield merely because they are documented.

Handoff construction

1. Freeze each referenced producer artifact at an immutable repository commit.
2. Compute the SHA-256 digest of the exact referenced file.
3. Create a unique handoff_id and identify the producing project and completed work block.
4. Classify the yield categories and state a concise reuse rationale.
5. Choose a registered payload profile. The first profile is course-concepts.v1.
6. Add immutable payload references with repository identity, commit, path, and digest.
7. Add explicit included_identifiers or a finite bounded_selection, never an unbounded repository scan.
8. Set requested_mode explicitly.
9. Require pkm-knowledge-handoff-result.v1.
10. Validate the envelope before transport.
11. Store the exact envelope digest in the external task and handoff record, never inside the envelope itself.

Mode meanings

consultation requests read-only mapping, reuse, conflict, and unsupported-relation findings. It grants no write or ontology authority.
proposal requests a bounded reconciliation and proposed vault change set. It grants no canonical write.
canonical_ingest requests an already authorized ingest. The external approval must bind Maxim's decision to the exact envelope digest. The curator still validates, reconciles, writes, and reads back under PKM rules.

Course profile

course-concepts.v1 identifies the module, approved concept artifact reference, terminology registry reference, included concept identifiers, and the invariant preserve_instructor_approved_meaning=true. Referenced artifacts remain authoritative. The profile does not duplicate concept definitions or translations.

Validation

Install the declared Python dependency from requirements.txt in the project environment.

Run:

python3 skills/project-knowledge-handoff/scripts/validate_contracts.py --fixtures

Validate an individual JSON document by passing its path instead of --fixtures.

The validator applies the generic envelope or result schema, dispatches the registered payload profile, rejects duplicate or dangling reference identifiers, and checks that the course profile selection matches the generic envelope selection.

Result handling

Accept only pkm-knowledge-handoff-result.v1. It must identify the originating envelope and exact digest, report entity and relation outcomes, conflicts, validation outcomes, and exact read-back paths. A successful transport or task completion without this result is not proof of canonical ingest.

Boundaries

Do not modify MAS routing, persistent agent contracts, course workflow files, producer artifacts, or the canonical vault while implementing or validating this PKM-owned foundation.
Do not create a PKM task when the knowledge-yield decision is no_reusable_yield.
Do not let a producer write directly to the vault.
Do not infer ontology types or relations from the payload profile.
The canonical ontology remains Requirements/05-knowledge-graph-schema.md.

Owned files

references/contracts/pkm-knowledge-handoff.v1.schema.json
references/contracts/course-concepts.v1.schema.json
references/contracts/pkm-knowledge-handoff-result.v1.schema.json
fixtures/positive/
fixtures/negative/
scripts/validate_contracts.py
