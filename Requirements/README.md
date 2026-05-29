# Digital Mind Requirements Baseline

This directory is the canonical source of truth for the early project definition stages.

The purpose of this layer is to prevent project truth from being scattered across `AGENTS.md`, `BACKLOG.md`, raw notes, and ADRs.

## Reading Order

1. [Vision and Scope](01-vision-and-scope.md)
2. [Business Requirements](02-business-requirements.md)
3. [System Requirements](03-system-requirements.md)
4. [Domain Model](04-domain-model.md)

## Source-of-Truth Rules

| Question | Canonical File | Notes |
|----------|----------------|-------|
| What is this project and why does it exist? | `01-vision-and-scope.md` | Product-level definition |
| What outcomes does Maxim expect? | `02-business-requirements.md` | Customer/business intent |
| What must the system do? | `03-system-requirements.md` | Functional and non-functional requirements |
| What are the core domain entities and boundaries? | `04-domain-model.md` | Conceptual model before implementation |
| Which architecture decisions were accepted? | `../Architecture/` | ADRs only, not product truth |
| What should the agent do next? | `../BACKLOG.md` | Actionable work items only |
| How should an agent operate in a session? | `../AGENTS.md` | Operational bootstrap only |
| What did Maxim think aloud before formalization? | `../PKM-idea.md` and `../raw/` | Historical/raw input, not canonical |

## Change Policy

- Update these files when project meaning, scope, requirements, or domain boundaries change.
- Do not encode active task state here; use `BACKLOG.md` for that.
- Do not encode architectural decisions here; use ADRs for that.
- When raw notes contradict this baseline, this baseline wins until Maxim explicitly changes it.
