# Business Requirements

Status: Baseline draft
Last updated: 2026-05-28

## Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| Maxim Sobol | Owner, primary user, final decision-maker | Preserve and operate on personal worldview |
| Calen / OpenClaw agents | Assistant/operator | Ingest, maintain, query, and improve the knowledge system |
| Future family readers | Legacy audience | Understand Maxim's worldview, values, and intellectual trajectory |
| Academic/professional audience | Secondary audience | Learn from the architecture and methodology of AI-assisted knowledge systems |

## Business Objectives

### BR-01: Preserve Maxim's Worldview

The system must preserve not only information, but Maxim's interpretation of information: concepts, values, beliefs, quotes he endorses, and the typed relationships between them.

Rationale: The unique value of the project is worldview preservation, not generic note storage.

### BR-02: Reduce Context Loss Across Sessions

The system must give agents a stable project context at the start of each session.

Rationale: Work becomes chaotic when the agent reconstructs project truth from scattered files and stale conversation memory.

### BR-03: Support Reflective Thinking Over Time

The system must preserve how beliefs and conceptual relationships evolve.

Rationale: Maxim's worldview is temporal. Old beliefs should not be overwritten as if they never existed.

### BR-04: Enable Agent Reasoning Inside Maxim's Conceptual Framework

The system must allow an AI assistant to answer, analyze, and propose actions using Maxim's own concepts and relations.

Rationale: The long-term goal is not retrieval alone, but a useful assistant that reasons with accumulated personal context.

### BR-05: Remain Portable And Vendor-Independent

The system must remain usable without dependence on a specific LLM provider, database, note app, or SaaS platform.

Rationale: Digital Mind is intended to outlive current tools and remain transferable to future systems or heirs.

### BR-06: Keep Raw Evidence Separate From Curated Knowledge

The system must distinguish raw captures from curated wiki pages and formal project documents.

Rationale: Trust requires knowing whether a statement is Maxim's raw thought, an extracted concept, a reviewed requirement, or an architectural decision.

### BR-07: Support Academic And Professional Reuse

The system should produce architecture, requirements, and workflow artifacts that can later support teaching, research, or publication.

Rationale: The project also functions as a case study for AI systems design and personal knowledge infrastructure.

### BR-08: Treat PKM Skills As Project Assets

The skills used to maintain the wiki must be owned by the Digital Mind project, not only by a production agent environment on the VPS.

Rationale: Maxim needs both VPS-based agents and localhost development agents to use, inspect, and improve the same operational skills. If skills live only inside the VPS production environment, project behavior becomes hard to reproduce locally and the system drifts into environment-specific hidden state.

### BR-09: Provide A Unified Knowledge Field For Agents

Digital Mind must function as the structured knowledge field behind Maxim's agents, not only as a personal archive.

Rationale: Agents should not operate only from task-specific prompts. They need access to durable project/domain knowledge: facts, concepts, processes, artifacts, goals, constraints, and expectations.

### BR-10: Support Goal-Oriented Agent Management

The system should support treating agents like role-based collaborators: they can be created for a role, onboarded from project knowledge, evaluated against expectations, and retired or changed if they do not perform.

Rationale: Maxim wants to manage agents by goals and outcomes rather than micromanaging implementation steps. This requires structured knowledge about roles, responsibilities, context, and success criteria.

## Business Rules

| ID | Rule |
|----|------|
| BSR-01 | Maxim is the final authority for worldview claims and project direction. |
| BSR-02 | Raw inputs must not be silently rewritten into canonical beliefs. |
| BSR-03 | A quote endorsed by Maxim is a first-class personality signal, not merely a source citation. |
| BSR-04 | If a source contradicts existing wiki content, the contradiction must be flagged before updating curated knowledge. |
| BSR-05 | Files in the canonical vault are the primary record; databases and indexes are compiled artifacts. |
| BSR-06 | Requirements describe intent and expected behavior; ADRs describe accepted design decisions. |
| BSR-07 | Active tasks belong in `BACKLOG.md`, not in `AGENTS.md` or requirements documents. |
| BSR-08 | PKM-specific skills are part of the project system layer and should be versioned with the project. |
| BSR-09 | Agent prompts are not the canonical source of role, process, or project knowledge; curated files are. |
| BSR-10 | Agents should receive goals, constraints, and success criteria from the knowledge system whenever possible. |

## Value Drivers

- Personal reflection: capture and refine Maxim's own thinking.
- Legacy: allow future family readers to understand Maxim's worldview.
- AI utility: give assistants durable, structured context.
- Agent management: onboard and evaluate agents using structured project knowledge.
- Academic value: provide a real system for studying AI-assisted knowledge architecture.
- Professional value: develop reusable patterns for agentic systems and context engineering.

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Documentation drift | Agents receive contradictory context | Maintain a canonical source-of-truth map in `Requirements/README.md` |
| Scope explosion | The system becomes too broad to implement | Implement worldview core first while designing for broader knowledge |
| Tool lock-in | Future portability is lost | Keep markdown files canonical and databases derived |
| Environment lock-in | Localhost agents cannot reproduce VPS agent behavior | Store PKM-specific skills with the project system and deploy/sync them to runtime environments |
| Ontology overengineering | Capture becomes too slow for daily use | Start with a small relation set and evolve deliberately |
| Prompt-only agent behavior | Agents act without deep project understanding | Store goals, roles, constraints, and process knowledge as curated knowledge objects |
| Unreviewed AI interpretation | The system stores claims Maxim does not endorse | Separate raw, extracted, reviewed, and endorsed states |
