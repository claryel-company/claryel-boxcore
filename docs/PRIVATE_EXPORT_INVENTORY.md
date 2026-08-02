# Private-to-public export inventory

**Snapshot:** 2026-08-01
**Rule:** clean file-level export or independent public re-engineering only; private Git history is never copied.

This inventory records candidate capability boundaries, not permission to publish. Every actual export requires a record in `PROVENANCE.md` with the exact reviewed source commit, licence decision, sanitisation and tests.

| Source repository | Candidate public value | Material retained privately | Decision |
|---|---|---|---|
| `claryel-platform` | Generic architecture principles, terminology, repository boundary and public ADR decisions | Organisation-wide governance details and private repository metadata | Publish the Box Core boundary and reference central decisions; do not create a second project-wide catalogue |
| `claryel-box` | Generic service catalogue, state boundaries, non-destructive simulation and health-check contracts | Deployment-specific runtime, hosts, storage layout, production environment and customer data | Re-engineer as independently useful NixOS modules; do not copy production Compose files unchanged |
| `claryel-installer` | Audit, plan, apply, verify, rollback and storage-safety contracts | Device identifiers, exact private disk layouts, recovery locations and commercial deployment controls | Export interfaces and synthetic failure tests after sanitisation |
| `claryel-autoinstall` | Bootstrap stages, supported-platform matrix and unattended-install contracts | Private repository-token flow, exact internal repository set and host bootstrap | Replace private synchronisation with a public Git-compatible bootstrap contract |
| `claryel-agent-fabric` | Administrative-intent, change-plan and orchestration contracts | Private role prompts, internal orchestration topology and commercial agents | Export deterministic interfaces and adversarial tests only |
| `claryel-node-agent` | Privacy-minimised hardware discovery, health model and approved local-action interface | Fleet identifiers, remote credentials, topology and customer telemetry | Publish synthetic probes and schemas; keep operational fleet data private |
| `claryel-integrations` | Home Assistant, MQTT, Git, Forgejo, hosted forge and optional remote-access interfaces | Vendor credentials, customer endpoints and commercial adapters | Export protocol contracts, local simulators and revocation behaviour only |
| `claryel-remote-infrastructure` | Consent, audit and least-privilege concepts for optional support sessions | Tickets, conversations, SLA, workforce queues, remote sessions and telemetry | Outside Box Core implementation; publish only boundary and consent contracts |
| `claryel-servicehub` | Generic equipment-profile vocabulary and lifecycle status concepts | CMDB, warehouse, inventory, purchases, logistics, maintenance and customer assets | Outside Box Core runtime; use only generic public vocabulary |
| `claryel-space` | Managed-site content contract, user-facing localisation, public status and Universe relation | Shared website runtime, Cloudflare configuration, identity internals and production topology | Website runtime and translations stay in Space; canonical project facts stay here |
| `claryel-web-community` | Voice-first public workflow concepts, Git-compatible changes and contribution lessons | Product-specific plans, account limits and unrelated website-builder implementation | Cross-link and share stable open contracts without duplicating ownership |
| `claryel-funding` | Public grant-scope, budget, milestone and evidence-publication schemas | Customer funding cases, source documents, identifiers and private financial plans | Publish only approved CLARYEL records and generic schemas |
| `claryel-boxcore` | Reviewed open-core code, schemas, documentation, examples, tests and evidence | No customer-specific content; embargoed security fixes may be temporarily withheld | Authoritative public destination |

## Current export records

| Record | Source | Destination | Status |
|---|---|---|---|
| `BCX-0001` | privacy-minimised Node Agent capability discovery | `internal/discovery/` and `cmd/boxcore-node/` | Public experimental implementation; provenance recorded |

No other private capability is claimed as publicly implemented.

## Export priority

1. Versioned schemas, deterministic policy and synthetic examples.
2. Generic NixOS modules newly implemented in public.
3. Sanitised Home Assistant/MQTT and hardware-discovery contracts.
4. Safe activation, health, rollback and mutable-state recovery patterns.
5. Additional private-tested implementation only after security, licence, provenance and independent-utility review.

## Mandatory export questions

Before approving a candidate, answer:

1. Is the capability owned by Box Core or by another repository?
2. Can it function without private infrastructure or customer data?
3. Are all third-party rights compatible with public release?
4. Does the public result include tests, documentation and a useful failure mode?
5. Can provenance be recorded without exposing confidential context?
6. Does publication create a security risk that requires an embargo?
7. Would re-engineering produce a cleaner and more portable result than copying the private implementation?

A negative answer blocks export until the condition is resolved.
