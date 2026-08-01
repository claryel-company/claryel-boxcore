# Contributing to CLARYEL Box Core

This repository combines infrastructure, local AI, hardware control and private-data boundaries. Contributions therefore require unusually explicit safety and evidence.

## Before opening a change

1. Read `AGENTS.md`, `ARCHITECTURE.md`, `THREAT_MODEL.md`, `OPEN_SOURCE_SCOPE.md`, `SECURITY.md`, `docs/STATUS_MODEL.md` and `PUBLICATION_STATUS.md`.
2. Open or reference an issue that states the user outcome, trust boundary, implementation status and acceptance evidence.
3. Keep one functional change per Pull Request.
4. Use English for source, documentation, issues, release notes and comments.
5. Never paste customer data, real credentials, private topology, production logs, serial numbers or unresolved vulnerability details.

## Required Pull Request content

- user-visible outcome and exact scope;
- canonical implementation status;
- tests or reproducible validation evidence;
- security, privacy and rollback impact;
- compatibility and migration impact;
- documentation and synthetic examples;
- licence and third-party provenance;
- remaining limitations and follow-up work.

## Private-to-public exports

Only authorised CLARYEL maintainers may approve an export from a private repository. Every export must add a record to `docs/PROVENANCE.md` and pass:

- secret and credential scanning;
- personal-data and customer-data review;
- private-topology and identifier review;
- licence and third-party-rights review;
- dependency and supply-chain review;
- public tests and human approval.

Private Git history is never copied.

## Validation

```bash
python3 scripts/validate_public_baseline.py
go test ./...
nix flake check --no-build
```

The Pull Request CI also validates JSON examples against schemas, tests the Rego policy, checks that public text is English-only and scans the complete history for secrets.

## Review priorities

1. No private, customer or security-embargoed information.
2. No unreviewed voice-to-shell, model-to-actuator or public-exposure path.
3. Safe defaults, explicit capability gates and least privilege.
4. Reproducibility, health validation, rollback and mutable-state recovery.
5. Honest status and independently useful open results.
6. Complement existing projects instead of duplicating stronger upstream ownership.