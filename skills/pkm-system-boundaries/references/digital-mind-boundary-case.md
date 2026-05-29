Context
A project named Digital Mind started as research and design work for a personal ontology / digital personality system. Over time, the same repository began to hold structured knowledge content, linked concepts, processed sources, and thoughts across broader life domains.

Observed boundary shift
- The repo stopped being only about designing the system.
- It started functioning as the system's live knowledge environment.
- The user noticed that Digital Mind had become both the topic of research and one domain inside a broader PKM.

Key architectural insight
The real distinction is not project vs notes. It is system artifacts vs knowledge state.

System artifacts in this case
- AGENTS instructions
- backlog
- architecture decisions
- workflow definitions
- implementation and deployment planning

Knowledge state in this case
- concepts
- quotes
- people pages
- thought pages
- processed sources
- cross-links between knowledge objects

Versioning insight
The user identified that versioning all knowledge content feels wrong in essence and poor for scale. Git was being kept mainly because push/pull was the fastest cross-device sync path for Obsidian viewing.

Reusable lesson
When git is primarily serving replication convenience for a growing knowledge corpus, say that clearly. Do not mistake a sync workaround for the correct storage boundary.

Practical recommendation pattern
- separate a system repo from live knowledge state
- keep git for code/config/docs/snapshots
- treat the knowledge corpus as state, even if it remains markdown-backed
- rename the top-level container to reflect PKM/knowledge scope, with Digital Mind as one domain plus a separate meta-project if needed
