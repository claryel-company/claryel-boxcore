# Language policy

## Decision

**Public repositories are English-only.**

This applies to canonical source code, documentation, code and configuration comments, issues, Pull Requests, release notes, security advisories and public governance records.

## Rationale

Box Core is an international infrastructure and security project. A single public source language:

- makes review accessible to the widest contributor pool;
- prevents security-critical meaning from drifting between parallel source texts;
- keeps search, static analysis and contribution tooling predictable;
- avoids presenting an unreviewed translation as an independent architectural decision;
- reduces maintenance cost while the public core is still small.

## Website localisation boundary

**User-facing website translations** are not canonical public source documentation. They belong to the separately governed **managed-web localisation** layer owned by `claryel-company/claryel-space`.

The managed project website may continue to publish twenty locales, including Russian, because website accessibility and source-repository governance solve different problems.

The website localisation layer may consume versioned English facts from this repository and produce translated presentation content. It must not silently change technical scope, implementation status, funding status, security guarantees or legal meaning.

## Generated translated artefacts

A translated document may be published as a generated artefact only when all of the following are true:

1. the English source is identified and versioned;
2. the translation is clearly marked as non-canonical;
3. automated or human review appropriate to the content has occurred;
4. the translated artefact is not required to build, test or review the public source;
5. security, legal and funding statements remain traceable to the English source.

Generated translations are not maintained as parallel canonical files in this repository.

## Private internal documentation

Private CLARYEL repositories may retain bilingual English/Russian working documentation where required by the architecture owner. That internal policy does not apply to public repositories.

## Enforcement

`scripts/validate_public_baseline.py` rejects Cyrillic text in public source files and requires this policy. CI blocks non-compliant changes.

## Exceptions

The following are allowed only when technically necessary and explicitly reviewed:

- immutable third-party names or test data required to reproduce an encoding defect;
- language-code identifiers such as `ru` or `uk`;
- links to translated user-facing pages;
- generated artefacts outside the canonical source tree.

An exception must be narrowly scoped, documented in the Pull Request and must not reintroduce bilingual canonical source.
