# Folder Philosophy: Type over Topic

## Core Principle

The PKM wiki's folders encode **entity type** (what a page *is*) — never **topic** (what it's *about*). This is a deliberate design decision that resolves the fundamental tension in Zettelkasten/PKM methodology.

## Why Type-Based, Not Topic-Based

A topic-based tree inevitably fails for any rich knowledge base:

```
AI/                    ← where does agent-memory go? it fits here
  memory/
    agent-memory.md
engineering/           ← but it's also an engineering problem
  LLM/
    agent-memory.md
research/              ← and it's frontier research too
  frontier-problems/
    agent-memory.md
philosophy/            ← and it connects to Digital Mind philosophy
  digital-mind/
    agent-memory.md    ← SAME NOTE, FOUR PLACES = contradiction
```

Type-based solves this:

```
concepts/agent-memory.md  ← one canonical location because it IS a concept
```

The topic (AI, engineering, research, philosophy) emerges from **links and relations** on the page, not from folder nesting.

## How This Relates to MOC (Map of Content)

MOCs are topic-based navigation pages. They collect links to notes from any type folder, grouped by aspect. Together they form a dual navigation system:

| Layer | What it solves | Example |
|-------|---------------|---------|
| Type-based folders | "Where does this file live?" | `concepts/agent-memory.md` (unambiguous) |
| Links + Relations | "What is this connected to?" | `--related_concept--> [execution-loop]` |
| MOCs | "How do I browse this topic?" | `agentic-ai-system.md` as hub with 12 components |
| Connection Map | "What's the full graph?" | `connection-map.md` with clusters |

## Practical Consequences for Ingests

When creating a new wiki page:
1. Identify page type first (is it a concept? person? implementation? quote? thought? analysis? source?)
2. Place it in the corresponding folder
3. Add relations to encode topic connections
4. Update connection-map.md, index.md, glossary.md

Do NOT create topic-based subfolders (e.g. `concepts/AI/`, `concepts/philosophy/`). Type-based folders are flat per type.

## History

This principle emerged organically during the wiki's evolution (April-May 2026) and was formalized in the May 27 MOC discussion. The wiki began with Karpathy's llm-wiki three-layer pattern and the type-based routing came from the original community implementation's entity types (Concept, Implementation, Person, etc.).
