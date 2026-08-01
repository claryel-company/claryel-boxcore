# Public implementation and delivery status

**Snapshot date:** 2026-08-01

This is an early public baseline. Private experiments are useful background but are not public implementation until reviewed code, tests and evidence are merged here.

## Capability status

| Capability | Status | Current public evidence | Next evidence threshold |
|---|---|---|---|
| Architecture, threat model and project boundary | `experimental` | Public documents and deterministic consistency checks | External review and evidence from the first complete runtime path |
| Desired-state and hardware-profile schemas | `experimental` | Versioned JSON Schemas and synthetic example | Runtime consumers, negative fixtures and external review |
| Change-plan contract | `experimental` | Versioned schema and synthetic examples | Runtime producer and consumer tests |
| Risk policy | `experimental` | Public Rego policy and policy tests | Integration with a public change-plan evaluator |
| Nix flake | `experimental` | Public flake targeting the supported NixOS release | Reproducible build evidence on clean runners |
| Baseline NixOS module | `experimental` | Non-destructive module with local state boundaries | NixOS VM integration tests and upgrade evidence |
| Node capability service | `experimental` | Go service, tests and provenance record | Authenticated local integration and compatibility evidence |
| Service catalogue | `planned` | Boundary documented | Generic service contracts and package tests |
| Voice-to-GitOps runtime | `planned` | Contract, schema, policy and threat model only | Public constrained interpreter and end-to-end test |
| Home Assistant/MQTT adapter | `private-testing` | Public boundary and milestone only | Sanitised adapter, safe simulation and public tests |
| Atomic activation and health controller | `planned` | State machine and milestone contract | Public controller and failure-injection tests |
| Mutable-state backup and recovery | `planned` | Separation from configuration rollback documented | Service-specific backup/restore tests |
| Hardware discovery | `experimental` | Privacy-minimised local capability probe | Bounded profile matching and evidence records |
| Validated hardware profiles | `planned` | Schema and validation procedure | Profile-specific public evidence |
| Intel AMT, Redfish and IPMI adapters | `planned` | Capability and trust boundary documented | Disabled-by-default public adapter and simulator tests |
| Remote support, CMDB, logistics and SLA | `outside-scope` | Commercial boundary documented | Not a public-core deliverable |
| Customer data, prompts, voice and RAG | `outside-scope` | Local data boundary documented | Must never enter this repository |

## Delivery status

Capability status and delivery status are separate dimensions.

| Surface | State | Evidence available in this repository |
|---|---|---|
| Public source baseline | `merged` | Initial public history exists |
| Grant-readiness revision | `source-change-in-review` | Focused branch and Pull Request evidence pending |
| Release artefact | `not-released` | No tagged production release is claimed |
| Managed website source | `owned-elsewhere` | Private managed-web repository owns runtime and deployment |
| Project site deployment | `not-publicly-validated` | Exact managed-web workflow and live-domain evidence must be recorded separately |
| Reference NixOS deployment | `not-publicly-validated` | Planned grant evidence |

## Application and funding status

| State | Value |
|---|---|
| Application submission | Confirmed by applicant before 2026-08-01 12:00 CEST |
| Submission receipt | Exists; retained in the private application record |
| Requested | EUR 50,000 |
| Advance requested | No |
| Negotiated | Not established |
| Awarded | No award claimed |
| Paid | EUR 0 claimed |
| Spent under this grant | EUR 0 claimed |

The submitted application package is not modified retroactively by later repository or website improvements. See `docs/APPLICATION_SUBMISSION_STATUS.md`.

## Honesty rules

- A submission receipt is not an eligibility decision or award.
- A private prototype is not public implementation.
- A source marker is not a passing test.
- A passing test is not a release.
- A merged Pull Request is not a deployment.
- A deployment is not browser validation.
- A requested grant is not an award.
- A hardware model name is not compatibility evidence.

Every status transition must cite the exact public commit, checks, release or workflow run, date and remaining limitations.