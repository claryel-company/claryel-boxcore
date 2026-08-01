# CLARYEL Box Core

[![Validate public baseline](https://github.com/claryel-company/claryel-boxcore/actions/workflows/validate.yml/badge.svg)](https://github.com/claryel-company/claryel-boxcore/actions/workflows/validate.yml)

> **Status:** early public baseline; not production-ready. Private experiments are never described as public implementation. The requested NGI Fediversity support is not an award.

<!-- CLARYEL-NAVIGATION:START -->
## CLARYEL project navigation

This repository is an accepted public implementation owner inside the CLARYEL project. Before structural work, read the central architecture and routing in [`claryel-company/claryel-platform`](https://github.com/claryel-company/claryel-platform), especially `ASSUMPTIONS.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `REPOSITORIES.md`, `TASK_ROUTING.md`, `DEVELOPMENT_RULES.md`, `TERMINOLOGY.md` and `repository-catalog.yaml`.

Local ownership is declared in [`REPOSITORY.yaml`](REPOSITORY.yaml); agent rules are in [`AGENTS.md`](AGENTS.md); durable handoff is in [`NEXT_STEPS.md`](NEXT_STEPS.md).
<!-- CLARYEL-NAVIGATION:END -->

## Speak. Review. Deploy. Roll back.

CLARYEL Box Core is a free and open NixOS control plane for private AI and hardware-integrated edge systems operated by households, professionals and small organisations.

Its defining control loop is deliberately safer than direct voice administration:

`local voice or text intent → constrained change plan → Git-compatible diff → schema and policy validation → risk-based approval → pinned NixOS build → dry run → atomic activation → service and hardware health checks → success or rollback`

The project does not claim to invent NixOS, GitOps, self-hosting, Home Assistant or fleet management. It connects them at a boundary that remains underserved: explainable local intent, user-owned desired state, physical-world integration, bounded hardware profiles and recovery for one or a small number of owner-controlled nodes.

## Why this fits NGI Fediversity

- **Reproducibility:** pinned NixOS generations and explicit hardware profiles.
- **User control:** configuration is portable; secrets and content remain local.
- **Service portability:** Git providers, remote-access providers and hardware vendors are replaceable adapters.
- **Safe operation:** natural-language requests create reviewable proposals, never unreviewed shell actions.
- **Open public value:** the grant-funded core remains independently usable without a CLARYEL subscription.
- **Real-world validation:** the same open core is intended to support a commercial appliance and public reference deployment, creating a long-term maintenance incentive.

See [`docs/GRANT_ALIGNMENT.md`](docs/GRANT_ALIGNMENT.md) and [`docs/COMPETITIVE_LANDSCAPE.md`](docs/COMPETITIVE_LANDSCAPE.md).

## Trust planes

| Plane | Contains | Explicitly excludes |
|---|---|---|
| Public source | Open code, schemas, generic profiles, tests, documentation and release evidence | Customer-specific configuration and private topology |
| User-owned desired state | Declarative technical configuration for one or more systems | Secret values, documents, voice recordings and RAG content |
| Local secret | Credentials, keys and recovery material | Git history and hosted configuration services |
| Local data | Documents, databases, object stores, vector indexes, prompts and voice data | Public repositories and support tooling |
| Optional access | Replaceable WireGuard, Cloudflare Tunnel or other adapters | Ownership of configuration truth or customer content |

## Public evidence already present

- architecture, governance, grant boundary and threat model;
- desired-state and hardware-profile JSON Schemas;
- initial risk policy for forbidden, high-, medium- and low-risk changes;
- experimental Nix flake and non-destructive NixOS module;
- privacy-minimised node capability service clean-reengineered from the private Node Agent with provenance;
- synthetic examples that contain no customer data or secret values;
- public CI, repository-language enforcement and secret scanning;
- budget, milestones, implementation status and clean-export inventory.

## Honest implementation status

| Capability | Status | Public evidence |
|---|---|---|
| Architecture, governance, schemas and grant boundary | `implemented` | Documents, schemas and deterministic validation |
| Nix flake and baseline NixOS module | `experimental` | Non-destructive module and flake checks |
| Node capability service | `experimental` | Go implementation, tests and provenance record |
| Voice-to-GitOps runtime | `planned` | Change-plan contract and risk policy; no public runtime claim |
| Home Assistant and MQTT adapter | `private-testing` | Public boundary defined; sanitised adapter not yet released |
| Validated hardware profiles | `planned` | Schema and validation method published; evidence pending |
| Atomic activation, health validation and rollback controller | `planned` | Architecture and milestone contract published |
| Commercial support, CMDB, logistics and SLA | `outside-scope` | Intentionally retained in private commercial systems |

Canonical meanings are in [`docs/STATUS_MODEL.md`](docs/STATUS_MODEL.md) and the detailed snapshot is in [`PUBLICATION_STATUS.md`](PUBLICATION_STATUS.md).

## Competitive position

The strongest neighbouring projects solve important parts of the same landscape:

- SelfPrivacy automates the lifecycle of self-hosted services.
- Nix Fleet targets central management of partially offline NixOS fleets.
- NixEdgeOpt optimises placement and migration across multiple NixOS nodes.
- End-to-end NixOS boot security strengthens trusted and verified boot.
- Nocloud and bewCloud provide user-facing self-hosted applications.

CLARYEL Box Core is differentiated by the complete auditable loop from local human intent to an approved Git change, reproducible hardware-aware activation, Home Assistant sensors and actuators, state-aware recovery and optional out-of-band management—without placing customer content in the configuration or support planes. It is designed to consume and complement neighbouring work rather than duplicate it.

## Project and funding boundary

Requested support: **EUR 50,000**. No advance is requested. This is a requested amount, not an award.

Funded scope: public NixOS core, Voice-to-GitOps contracts and runtime, Home Assistant/MQTT integration, hardware profiles, atomic activation, health validation, rollback, backup/recovery contracts, testing, documentation and public reference evidence.

Separately financed: commercial CLARYEL Box operations, customer equipment, support tickets, CMDB, warehouse/logistics, SLA workflows, adjacent CLARYEL products, general website runtime and the wider commercial security audit.

- [`GRANT_SCOPE.md`](GRANT_SCOPE.md)
- [`BUDGET.md`](BUDGET.md)
- [`MILESTONES.md`](MILESTONES.md)
- [`docs/DEMO_AND_EVIDENCE_PLAN.md`](docs/DEMO_AND_EVIDENCE_PLAN.md)

## Website

- Project site: **https://boxcore.claryel.space**
- Public repository: **https://github.com/claryel-company/claryel-boxcore**
- Ecosystem map: **https://claryel.space/universe/**

The managed website runtime is owned by the private `claryel-space` repository. This public repository owns versioned public facts and evidence. Repository source, merged Pull Request, deployed site and browser validation are separate delivery states.

## Documentation

- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`THREAT_MODEL.md`](THREAT_MODEL.md)
- [`OPEN_SOURCE_SCOPE.md`](OPEN_SOURCE_SCOPE.md)
- [`HARDWARE_COMPATIBILITY.md`](HARDWARE_COMPATIBILITY.md)
- [`SECURITY.md`](SECURITY.md)
- [`GOVERNANCE.md`](GOVERNANCE.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- [`docs/COMPETITIVE_LANDSCAPE.md`](docs/COMPETITIVE_LANDSCAPE.md)
- [`docs/GRANT_ALIGNMENT.md`](docs/GRANT_ALIGNMENT.md)
- [`docs/PRIVATE_EXPORT_INVENTORY.md`](docs/PRIVATE_EXPORT_INVENTORY.md)
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md)
- [`NEXT_STEPS.md`](NEXT_STEPS.md)

## Validation

```bash
python3 scripts/validate_public_baseline.py
go test ./...
nix flake check --no-build
```

CI additionally validates example documents against their schemas, tests the Rego policy and scans the complete public history for secrets.

## Licence

Public code is released under Apache-2.0. Documentation is released under CC BY-SA 4.0 unless a file states another compatible licence. See [`LICENSES/README.md`](LICENSES/README.md).