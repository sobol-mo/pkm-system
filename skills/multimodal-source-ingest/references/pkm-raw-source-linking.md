PKM raw/source linking

Problem class
When a PKM repo splits raw/ and wiki/sources/, link text can look correct while the markdown target path is wrong. A common failure is copying an existing broken pattern like ../raw/... from a source page under wiki/sources/.

After KnowledgeVault migration, the same bug class appears in reverse: copied source pages may keep legacy `../../raw/...` links even though canonical vault pages under `sources/` now need `../raw/...` and `../assets/raw/...`.

Canonical relative paths
- from wiki/sources/<note>.md to raw/<note>.md -> ../../raw/<note>.md
- from wiki/sources/<note>.md to raw/assets/<file> -> ../../raw/assets/<file>
- from raw/<note>.md back to wiki/sources/<note>.md -> ../wiki/sources/<note>.md

Canonical vault relative paths
- from sources/<note>.md to raw/<note>.md -> ../raw/<note>.md
- from sources/<note>.md to assets/raw/<file> -> ../assets/raw/<file>
- from raw/<note>.md back to sources/<note>.md -> ../sources/<note>.md

Durable rule
Resolve links from the file's real filesystem location, not from the conceptual layer name. Do not trust previously written examples without checking the relative depth.

Deterministic checks
- audit wiki/sources for suspicious source->raw links containing ../raw/
- audit raw for backlinks that do not use ../wiki/sources/
- verify that each edited raw/source pair links both ways
- verify that linked target files actually exist

Migration note
After moving content into `KnowledgeVault`, run the deterministic checker/fixer against the vault root so legacy raw/source links are normalized to the canonical vault layout.

Useful grep patterns
- wiki/sources wrong raw path: \(\.\./raw/
- raw expected backlink area: wiki/sources/
- source pages that embed raw assets: ../../raw/assets/

Pre-commit idea
Fail the commit if any file under PKM/wiki/sources/ contains ../raw/ because that path depth is wrong for this repo layout.

Session note
This exact bug repeated across multiple source pages because a broken pattern was copied forward. The real fix is template plus validator, not better memory from the model.
