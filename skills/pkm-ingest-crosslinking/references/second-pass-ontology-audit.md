# Second-pass ontology audit pattern

Use when first-pass ingest produced source summary plus obvious named frameworks, but the user asks whether the source was integrated systemically.

Trigger signals:
- user asks whether all useful concepts were extracted
- source teaches philosophy, psychology, quality-of-life practice, or a practical framework
- first pass extracted only large named ideas while techniques remain in prose
- people or quotes are mentioned but not linked to existing vault pages

Audit steps:
1. Read the full raw evidence, not only the source summary.
2. Make a candidate list in five buckets:
   - standalone concepts
   - repeatable techniques or practices
   - people and attributed quotes
   - cases/examples/anecdotes
   - meta-principles or relation hubs
3. Search existing vault pages for each candidate by name, alias, slug, and distinctive phrase.
4. Decide for each candidate: update existing page, create new page, leave as source-page bullet, or ask Maxim.
5. Update source relations, affected concept/person pages, index, connection-map, and log.
6. Run vault health checker and report the health result plus any semantic limitations.

Quality bar:
A good pass does not merely add more pages. It changes the source from summary-driven extraction into graph-useful ontology: reusable techniques and principles become reachable from existing concepts and people.

Concrete failure this prevents:
A video on Stoicism and stupidity extracted Dunning-Kruger, Brandolini, Cipolla, Stoicism, and Amygdala Hijack, but initially missed Socratic Method, Strategic Silence, Agreement as Weapon, Separating Person from Behavior, Praemeditatio Malorum, Cognitive Reframing, Seneca's Delay Rule, Evening Self-Review, Attention as Capital, Stimulus-Response Gap, Self-Doubt as Protection, Understanding through Ignorance, Slow Breathing Downregulation, McArthur Wheeler Case, Socrates, and Bertrand Russell.