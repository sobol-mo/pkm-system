# Vision and Scope

Status: Baseline draft
Last updated: 2026-05-28

## Product Name

User-facing name: **Digital Mind**.

Technical name: **Personal Ontology**.

Repository/project shorthand: **PKM**.

## Vision

Digital Mind is a system for preserving and operating on Maxim's conceptual worldview as a structured network of concepts and typed relationships.

The system is not a generic note-taking tool. It is intended to become a durable external model of how Maxim understands the world: values, beliefs, definitions, interpretations, technical knowledge, life knowledge, endorsed quotes, and their relationships.

Digital Mind is also intended to become a **unified knowledge field** for Maxim's work and life: the structured context from which AI agents can understand goals, roles, constraints, artifacts, processes, expectations, and domain knowledge.

The project therefore supports two connected purposes:

- preserving Maxim's worldview and conceptual identity
- providing deep structured context for agents that act on Maxim's behalf

## Core Hypothesis

Personality can be approximated as:

```text
personality = concepts + typed relationships between concepts + temporal evolution
```

Two people may use the same concepts but differ in how those concepts relate.

Example:

```text
[Money] --sufficient_for--> [Happiness]
[Money] --instrument_for--> [Happiness]
```

The concepts are the same. The worldview is different because the relationship type is different.

## Problem Statement

Maxim's thoughts, definitions, sources, quotes, and reflections are currently distributed across Telegram, conversations, raw notes, research files, and ad hoc documentation.

This makes it hard to:

- preserve the continuity of Maxim's thinking across time
- distinguish raw captures from reviewed beliefs and definitions
- query how a concept relates to other concepts in Maxim's worldview
- let an AI assistant reason inside Maxim's conceptual framework
- onboard agents into Maxim's real context without relying on prompt-only instructions
- manage agents by goals, expectations, and performance criteria rather than micromanaged steps
- leave a coherent worldview archive for future readers

The project needs a canonical structure that separates raw input, curated knowledge, requirements, architecture, operational state, and derived runtime artifacts.

## Target Outcome

Digital Mind should make Maxim's worldview inspectable, queryable, and maintainable.

It should also provide a structured knowledge foundation for multi-agent systems, where agents can rely on curated project/domain knowledge instead of shallow prompts or generic internet knowledge.

The desired end state is a portable knowledge vault where a human or AI agent can answer questions such as:

- What does Maxim mean by this concept?
- Which sources shaped this belief?
- Which quotes does Maxim endorse, and what values do they express?
- How did Maxim's view on a concept change over time?
- Which concepts are central in Maxim's worldview?
- What goal is this agent expected to achieve?
- Which project facts, processes, artifacts, and constraints should guide this agent's work?
- How should an agent be evaluated for this role?

## Scope Strategy

The project follows **Scope B by design, Scope A by implementation order**.

Scope A, implemented first:

- worldview
- values
- beliefs
- interpretations
- endorsed quotes
- conceptual relations

Scope B, supported by design:

- technical knowledge
- facts and sources
- skills and practices
- experiences
- people
- academic and professional knowledge
- roles, processes, artifacts, goals, expectations, and evaluation criteria for agents

The reason is practical: worldview is the core differentiator, but Maxim's worldview and technical knowledge are inseparable in real use.

## In Scope

- raw capture of Maxim's thoughts and external sources
- curated wiki pages for concepts, people, quotes, thoughts, sources, analyses, and implementations
- typed relations between knowledge objects
- temporal representation of beliefs and values
- agent-assisted ingest, query, lint, rebuild, and export workflows
- agent role/onboarding context built from curated knowledge
- goal-oriented agent operation supported by documented objectives, constraints, and success criteria
- portable markdown-first storage
- derived graph/vector/runtime representations built from canonical files

## Out of Scope For The Current Baseline

- public product launch
- multi-user collaboration
- social-network features
- replacing Maxim's full daily journal
- training a model on private data
- making a database the canonical source of truth
- committing automated vault state changes as meaningful project history

## Success Criteria

The project is successful at the first baseline stage when:

- a new agent can understand the project by reading the canonical documents in `Requirements/`
- raw ideas, requirements, architecture decisions, backlog, and wiki content no longer compete as sources of truth
- a new concept, quote, or thought can be ingested into the vault with typed relations
- Maxim can ask a question about his worldview and receive an answer grounded in wiki pages
- project decisions can be traced to requirements or ADRs instead of conversational residue

## Open Product Questions

- Should concept names be stored in Russian, English, or bilingually?
- What is the minimum useful ontology for the first working version?
- Which interface should be primary for daily use: Telegram, Obsidian, CLI, or OpenClaw skill?
- What is the first export format for legacy use: folder archive, static site, PDF, or JSON?
