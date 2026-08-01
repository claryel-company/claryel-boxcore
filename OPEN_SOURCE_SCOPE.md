# Open-source scope and clean-export policy

## Public after review

The following categories are intended for publication when they pass the release gates:

- Nix flakes and generic NixOS modules;
- desired-state, change-plan, evidence and hardware-profile schemas;
- Voice-to-GitOps contracts and generic implementation;
- deterministic policy rules and approval model;
- generic Home Assistant and MQTT adapters;
- capability-gated Intel AMT, Redfish and IPMI adapters;
- synthetic bootstrap examples and test fixtures;
- tests, CI, documentation, threat model and public evidence;
- grant scope, budget, milestones and implementation status.

## Private by necessity

The following categories remain private:

- customer documents, databases, vector stores, prompts and voice recordings;
- credentials, keys, recovery material and secret values;
- customer-specific desired state and private repository metadata;
- production topology, addressing, VPN details and account identifiers;
- support tickets, conversations, CMDB, warehouse and logistics data;
- commercial SLA workflows and equipment-replacement operations;
- unresolved vulnerabilities and confidential audit findings;
- third-party material without compatible publication rights.

## Clean-export rule

Private Git history is never copied. A candidate component enters a clean public branch only after:

1. functional-owner approval;
2. secret and credential scanning;
3. personal-data, customer-data and private-topology review;
4. licence and third-party-rights review;
5. dependency and SBOM review;
6. removal of internal names, identifiers and environment-specific paths;
7. replacement of real data with synthetic fixtures;
8. public tests and documentation;
9. provenance recording of the exact reviewed private source commit, destination and exclusions;
10. human approval of the public diff.

A private source commit proves provenance, not public implementation. Public implementation exists only after the reviewed code and tests are merged here.

## Public repository language

Public repository source, documentation, issues, release notes and comments are English-only. This rule keeps the public development surface internationally reviewable and prevents translation drift in security-critical source.

User-facing website translations may be produced in the separately governed managed-web localisation repository. They do not change the language of this public source repository.

## Status vocabulary

Canonical status definitions are in `docs/STATUS_MODEL.md`. Do not invent local synonyms such as `in-progress`, `ready`, `complete` or `beta` for implementation evidence.

## Licence model

Public code is released under Apache-2.0. Public documentation is released under CC BY-SA 4.0 unless a file states another compatible licence. See `LICENSES/README.md`.

A later licence refinement may improve compatibility, but it may not remove freedoms from already published grant-funded results.

## Export refusal conditions

A component is not exported when:

- it cannot be separated from customer or confidential data;
- publication would expose an unresolved security weakness;
- CLARYEL does not own or cannot relicense the required rights;
- the public result would be a misleading stub without independent utility;
- the capability belongs to another repository owner;
- validation cannot be reproduced without private infrastructure.

The refusal reason is recorded as `withheld-security`, `outside-scope` or an explicit known limitation without publishing the sensitive detail.