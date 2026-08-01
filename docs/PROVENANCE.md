# Public export provenance

This register records reviewed private-to-public exports without copying private Git history. A provenance record establishes origin and review; it does not by itself establish production readiness.

## BCX-0001 — privacy-minimised node capability service

| Field | Value |
|---|---|
| Source owner | `claryel-company/claryel-node-agent` |
| Reviewed source commit | `bfd46ea40e6aebe48931c160dfb9361d2450cadd` |
| Reviewed source files | `cmd/claryel-node-agent/main.go`, `internal/discovery/discovery.go`, `internal/discovery/discovery_test.go` |
| Public destination | `cmd/boxcore-node/`, `internal/discovery/` |
| Export type | Clean re-engineering; no private history copied |
| Public licence | Apache-2.0 |
| Security changes | Removed raw hostname, addresses, serial numbers, topology, credentials, telemetry and mutation methods; retained loopback default; restricted HTTP interface to GET/HEAD; added timeouts, response hardening and tests |
| Identifier design | Initial public version used a truncated hostname-derived hash; the grant-readiness revision replaces it with a random process-ephemeral identifier to reduce persistent fingerprinting and cross-log linkability |
| Private material excluded | Internal service names, fleet identifiers, credentials, private topology, customer telemetry, remote execution and private worker adapters |
| Public validation | Go unit tests, race test, vet, public repository validation and full-history secret scan |
| Public status | `experimental` |

## Required fields for future records

Every later export adds a separate record containing:

- stable export identifier;
- source owner and exact reviewed private commit;
- reviewed source files and public destination;
- export or re-engineering method;
- functional-owner approval;
- secret, personal-data and topology review;
- licence and third-party-rights decision;
- dependency and supply-chain review;
- security changes and excluded material;
- public validation evidence;
- canonical implementation status.

## Integrity rule

Never rewrite a provenance record to imply that a later public implementation was identical to the original private source. Add a dated amendment or a new record when the public design materially changes.

## Confidentiality rule

The register may identify an authorised private source repository and exact commit for auditability, but it never reproduces inaccessible source, private URLs, customer identifiers, credentials, topology or embargoed security details.