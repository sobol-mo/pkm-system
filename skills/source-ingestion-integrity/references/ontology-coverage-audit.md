# Ontology Coverage Audit

Use this reference when a source was already ingested but the user questions whether extraction was too shallow.

## Trigger

Run this audit when:
- the source is a philosophy, psychology, life-improvement, technical, or systems-thinking source
- the first pass extracted only obvious named frameworks
- the user asks whether all useful concepts were extracted
- practical techniques may still be buried in the transcript/article

## Audit question

Do not ask only:
What pages were created?

Ask:
What reusable ontology is present in the source, and which parts are still trapped in prose?

## Candidate classes

Extract candidates across these classes:

1. Named frameworks
Examples: Dunning-Kruger Effect, Brandolini's Law, Stoicism.

2. Techniques and practices
Examples: Socratic Method, Strategic Silence, Agreement as Weapon, Delay Rule, Evening Self-Review, slow breathing.

3. Meta-principles
Examples: attention as capital, self-doubt as protection against Dunning-Kruger, separating person from behavior, understanding through ignorance.

4. Neuropsychological mechanisms
Examples: amygdala hijack, stimulus-response gap, prefrontal cortex recovery, parasympathetic downregulation.

5. People, quotes, and cases
Examples: Socrates, Bertrand Russell, Mark Twain attribution, McArthur Wheeler lemon-juice case.

6. Relation hubs
Examples: a Stoic conflict-management system that organizes several techniques under one practice stack.

## Decision table

For every candidate:
- existing page with same meaning: enrich/link it
- existing related page but narrower candidate: create a focused page and link hierarchy
- valuable technique without page: create concept/technique node
- uncertain value: ask Maxim instead of burying or over-creating
- minor mention: keep as source-page bullet and note as non-promoted mention

## Failure pattern from the Stoicism video session

The first extraction captured major frameworks but missed several graph-worthy life-improvement techniques:
- Socratic Method
- Strategic Silence / Selective Engagement
- Agreement as Weapon
- Separating Person from Behavior
- Praemeditatio Malorum
- Cognitive Reframing / Removing Judgment
- Seneca's Delay Rule
- Evening Self-Review
- Attention as Capital
- Stimulus-Response Gap
- Self-Doubt as Protection Against Dunning-Kruger
- Understanding through Ignorance
- Slow Breathing / Parasympathetic Downregulation
- Bertrand Russell person/quote
- Socrates person/method
- McArthur Wheeler case

Lesson:
A summary-driven model tends to extract big labels and skip practical ontology.
A source-ingestion specialist must perform a second-pass ontology coverage audit before claiming completeness.

## Report format

When reporting an audit, include:
- extracted well
- missed but should be promoted
- present but source-page only is enough
- uncertain candidates to ask Maxim about
- exact next repair pass recommended
