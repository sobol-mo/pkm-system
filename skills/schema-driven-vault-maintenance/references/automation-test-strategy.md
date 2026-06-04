When adding new KnowledgeVault automation, design the acceptance harness before the automation itself.

Why
The main failure mode is not script crashes. It is silent workflow drift: markdown looks valid, but the vault contract was violated.

Core invariants to protect
- raw evidence stays separate from curated knowledge
- entity routing stays type-correct: thought, source, quote, person, concept enrichment, implementation, analysis
- deterministic mechanics update index.md, connection-map.md, and log.md when required
- uncertainty is stated explicitly instead of being silently upgraded into fact
- raw captures are not rewritten into interpretation

Three-layer acceptance model
1. Mechanical correctness
- expected files created
- no unexpected files created
- frontmatter fields present where required
- folder/type mapping valid
- Relations section present where required
- raw <-> curated links resolve
- no broken relative links introduced

2. Workflow-contract correctness
- raw-first preservation respected
- no workflow misrouting such as thought treated as source
- no invented metadata
- existing pages preferred over duplicates when exact target already exists
- ambiguous inputs handled conservatively

3. Semantic adequacy
- workflow class chosen correctly
- relation extraction is defensible
- no over-creation of concepts
- wording does not overstate certainty

Recommended test harness structure
- fixtures/: canonical input cases
- manifests/: expected created/modified/untouched files plus prohibited outcomes
- expected/: golden snippets or expected surface patterns when useful
- run_fixture.py: executes automation on an isolated temp vault
- check_results.py: validates diff + checker outputs

Recommended first MVP fixture
thought-simple
- one short original thought from Maxim
- verifies the core boundary between raw capture and curated thought workflow
- should prove that no fake source metadata is invented and no unrelated pages change

Required negative tests
- missing metadata must not be hallucinated
- ambiguous input must not be over-promoted into curated truth
- relation-only requests must not trigger full ingest side effects
- broken evidence must block strong claims

Regression rule
bug once -> fixture forever

Recommended implementation order
1. define fixture format
2. define manifest/oracle format
3. build deterministic checker command with JSON output
4. create thought-simple fixture
5. run harness against a no-op or stub implementation first
6. only then implement the real automation
