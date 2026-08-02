# CLARYEL Box Core agent rules

Before any analysis or change:

1. Resolve the active-only repository scope and stop if it cannot be proven. Do not analyse or reference archived repositories.
2. Open `claryel-company/claryel-platform` and read `ASSUMPTIONS.md`, `ARCHITECTURE.md`, `DECISIONS.md`, ADR-0032, ADR-0034, related ADRs, `REPOSITORIES.md`, `TASK_ROUTING.md`, `DEVELOPMENT_RULES.md`, `TERMINOLOGY.md` and `repository-catalog.yaml`.
3. Read this repository's `README.md`, `REPOSITORY.yaml`, `ARCHITECTURE.md`, `OPEN_SOURCE_SCOPE.md`, `PUBLICATION_STATUS.md`, `SECURITY.md`, `docs/STATUS_MODEL.md`, `docs/LANGUAGE_POLICY.md`, `USER_GUIDES/README.md` and `NEXT_STEPS.md`.
4. Confirm that `claryel-company/claryel-boxcore` is the functional owner of the requested public open-core capability before changing it.

## Documentation language

All durable project documentation, user instructions, agent guidance, release notes and explanatory code or configuration comments are English only. During direct interaction with the architecture owner, command comments may be presented in English followed by Russian, but the Russian presentation must not be committed, stored in prompts or retained in generated repository artefacts. Managed product localisation is outside this public technical repository. ADR-0034 is authoritative.

## Mandatory rules

1. Treat this repository as public at all times.
2. Never copy private Git history. Clean-export or re-engineer reviewed files into an independent public history.
3. Never publish credentials, personal data, customer data, private topology, serial numbers, private repository URLs, support tickets or unpatched security findings.
4. Every private-to-public export records provenance, exact reviewed source commit, licence review, sanitisation and excluded material without exposing inaccessible content.
5. Use the canonical capability statuses defined in `docs/STATUS_MODEL.md`: `planned`, `experimental`, `validated`, `production-ready`, `private-testing`, `withheld-security` and `outside-scope`.
6. Keep delivery status separate from implementation status. A source change, merged Pull Request, deployment and browser validation are distinct states.
7. Never present the requested EUR 50,000 as awarded funding.
8. Git-managed configuration must never contain secret values or customer content.
9. Voice requests may propose changes but may not bypass schema validation, policy, review, approval or rollback controls.
10. Arbitrary shell execution, destructive storage actions and out-of-band hardware control are denied by default.
11. Hardware-management adapters must be capability-gated, locally authorised, auditable and disabled by default.
12. Every material change uses a focused branch, deterministic validation and a Pull Request.
13. Update `NEXT_STEPS.md`, `PUBLICATION_STATUS.md` and relevant evidence records with every material release.
14. Update role-based user instructions whenever a user-visible workflow, permission, failure mode or recovery path changes.
15. Do not claim public implementation based on private prototypes, plans, source markers or screenshots.

## Repository boundary

This repository owns the reusable public open core, schemas, policy contracts, hardware profiles, generic adapters, documentation, grant scope and public evidence. Commercial support operations, customer configurations, CMDB, logistics, SLA workflows, private topology, customer data and confidential security work remain in private CLARYEL repositories.

## Required completion evidence

A completion report must identify the final commit, Pull Request, checks, workflow runs, release or deployment state, browser evidence when applicable, rollback reference and remaining limitations.
