# Next steps

## Current request

- **Date:** 2026-08-01
- **Owner:** CLARYEL architecture owner
- **Working branch:** `grant-readiness-english-only-2026-08-01`
- **Scope:** review the public repository and project site against the NGI Fediversity proposal; remove Russian from public source; strengthen documentation, security, status and evidence; publish competitor differentiation; add a classic 2D grant view through the managed website repository.

## Completed on this branch

- Replaced bilingual public source and core documentation with English-only canonical text.
- Published a stricter trust-plane architecture, deployment state machine and mutable-data recovery boundary.
- Normalised capability, delivery and funding status reporting.
- Updated the Nix input to NixOS 26.05 and packaged the read-only node probe.
- Replaced the hostname-derived node identifier with a process-ephemeral identifier.
- Hardened the local HTTP service with method restrictions, timeouts, security headers and tests.
- Strengthened CI with Go race tests, vet, schema validation, Rego tests, Nix evaluation and full-history secret scanning.
- Added grant-alignment, competitive-landscape, status, language, quick-start, evidence and FAQ documentation.
- Added a versioned change-plan schema, synthetic examples and policy tests.

## Parallel cross-repository work

### `claryel-company/claryel-platform`

Required:

1. Accept an ADR that supersedes bilingual source for public repositories while preserving bilingual private/internal working documentation.
2. Register `claryel-boxcore` as the authoritative public open-core owner.
3. Update the central architecture, generated repository views and repository acceptance evidence.

Acceptance:

- central governance checks pass;
- Box Core ownership does not duplicate `claryel-box`, Installer, Integrations or Node Agent;
- public-source English policy and multilingual website ownership are explicit.

### `claryel-company/claryel-space`

Required:

1. Add an accessible 2D/classic grant brief without removing the twelve-view immersive presentation.
2. Publish comparison, scope, status, workplan and evidence links from canonical Box Core facts.
3. Keep all twenty user-facing website locales, including Russian, under the managed-web localisation contract.
4. Validate deterministic checks, browser workflows, Worker dry run, deployment and exact-domain audit.

Acceptance:

- the view selector works by pointer, touch and keyboard;
- `?view=classic` is restorable and essential content does not depend on WebGL or animation;
- requested funding is clearly marked as not awarded;
- source, deployment and browser evidence are reported separately.

## Ordered implementation backlog

### P0 — merge and release hygiene

- [ ] Open the focused Pull Request for this branch.
- [ ] Resolve every deterministic, Go, Nix, schema, policy and secret-scanning failure.
- [ ] Obtain maintainer review and merge through the protected branch.
- [ ] Record the final commit, workflow runs and rollback reference in this file.
- [ ] Tag no production-ready release until the documented threshold is met.

### P1 — runnable Voice-to-GitOps core

- [ ] Implement the constrained local intent interpreter that emits `change-plan.schema.json`.
- [ ] Implement deterministic policy evaluation and approval records.
- [ ] Implement a Git-compatible proposal workflow that also supports local and self-hosted forges.
- [ ] Add adversarial tests for prompt injection, command smuggling and policy self-modification.

Acceptance: synthetic low-, medium-, high-, unknown- and forbidden-risk requests produce deterministic reviewed results, and no free-form shell execution path exists.

### P2 — NixOS activation and recovery

- [ ] Add NixOS VM integration tests for the baseline module.
- [ ] Implement pinned build, dry run, activation and declared health checks.
- [ ] Implement deterministic configuration rollback.
- [ ] Publish service-specific mutable-state backup and restore contracts.

Acceptance: injected deployment failure restores the prior generation, while a separate tested restore procedure protects mutable data.

### P3 — physical-world integration

- [ ] Publish a generic Home Assistant adapter and local Assist entry point.
- [ ] Publish the MQTT contract and a synthetic sensor/actuator simulator.
- [ ] Ensure actuator actions use allowlists, capability gates and explicit approval.

Acceptance: a non-destructive public demo succeeds, and hostile or ambiguous requests fail closed.

### P4 — hardware evidence

- [ ] Validate a CPU-only x86_64 profile.
- [ ] Validate one integrated-GPU profile and one discrete-GPU profile.
- [ ] Publish aarch64 and storage/NAS experimental profiles.
- [ ] Implement disabled-by-default Intel AMT, Redfish and IPMI simulators before real hardware control.

Acceptance: every claim links to an exact commit, release, firmware assumptions, test date, privacy-minimised evidence and rollback procedure.

### P5 — community and upstream work

- [ ] Open discussions with NixOS/nixpkgs, Home Assistant, MQTT and relevant Fediversity projects before duplicating reusable work.
- [ ] Publish contribution templates for hardware evidence, change-plan fixtures and security review.
- [ ] Record upstream issues and patches where ownership belongs upstream.

## Known limitations

- No public end-to-end Voice-to-GitOps runtime exists yet.
- No hardware profile is publicly validated yet.
- Atomic activation, health validation and recovery remain planned.
- The Home Assistant adapter remains in private testing.
- No production-ready release is claimed.
- The NGI Fediversity support is requested, not awarded.

## Rollback

Before merge, rollback means closing the Pull Request and retaining `main`. After merge, revert the exact merge commit through a focused Pull Request, rerun the complete validation ladder and update status/evidence records. No customer data or migrations are affected by the current repository-only revision.
