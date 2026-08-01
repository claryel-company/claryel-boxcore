# Project governance

## Principles

- Open by default, private by necessity.
- Public claims follow public evidence.
- Safety and user control precede automation convenience.
- One capability has one authoritative owner.
- Hosted services and hardware vendors are replaceable adapters.
- Public repositories use English-only source and documentation.
- User-facing translations are produced by the separately governed managed-web localisation layer.

## Roles

### Maintainers

Maintainers approve releases, public exports, security-sensitive changes, contract versions and implementation-status transitions.

### Contributors

Contributors may propose code, documentation, tests, hardware profiles and validation evidence through reviewed Pull Requests. Translation work belongs to the managed website localisation repository, not this public source repository.

### Hardware validators

A hardware validator reproduces a profile on declared equipment and publishes non-sensitive evidence. Validators never publish serial numbers, management credentials, private network topology or customer identifiers.

### Community and documentation coordinator

The coordinator improves contributor onboarding, triages public issues, coordinates tests and releases, and ensures documentation remains usable. The role does not receive authority over customer systems or private data.

## Decision process

- Small compatible changes use a focused Pull Request and maintainer review.
- Public contract changes require versioning, migration notes and architecture review.
- Cross-repository ownership, trust-boundary or release-policy changes require a project-platform ADR.
- Security embargoes follow `SECURITY.md`.
- A capability status changes only when the evidence threshold in `docs/STATUS_MODEL.md` is met.

## Status transitions

A capability may move from `planned` to `experimental` only when public code and tests exist. It may move to `validated` only with reproducible external evidence. `production-ready` requires a documented release, supported upgrade and rollback path, security review, declared compatibility and operational evidence.

Private implementation cannot skip the public evidence requirements. `private-testing` records useful background without implying public availability.

## Grant transparency

Requested, negotiated, awarded, paid and spent amounts are distinct states. The repository and website must use the exact current state and must not present requested support as awarded.

Grant-funded deliverables, time records, commits, releases and payment evidence are separated from existing company resources and other grants.

## Commercial boundary

Commercial CLARYEL services may provide qualified appliances, installation, migration, managed updates, monitoring, recovery, equipment replacement, integrations and support. They do not receive authority to restrict, revoke or make the open core dependent on a subscription.

## Conflict handling

Potential conflicts of interest, licence concerns and security-sensitive reports are disclosed to maintainers. Decisions affecting a contributor's own commercial interest require a second reviewer when available and a written rationale.

## Amendment

Governance changes require a Pull Request, impact analysis, public discussion appropriate to the change and an explicit effective date. Structural changes must also update the central CLARYEL architecture decision record.