# Next steps

## Current documentation migration

- Date: `2026-08-02`
- Owner: CLARYEL Box Core Repository Maintainer
- Architecture authority: `claryel-company/claryel-platform` ADR-0034
- Scope: remove non-English durable documentation, apply the active-only boundary, update role instructions and enforce language and Markdown validation.

Completed on this branch:

- added a repository-local documentation-language validator and Pull Request gate;
- made English the only durable language for project documentation, user instructions, agent guidance and explanatory comments;
- documented that English-then-Russian command comments are transient direct-interaction output and must not be committed;
- updated `AGENTS.md` for ADR-0032, ADR-0034 and active-only navigation;
- updated `USER_GUIDES/README.md` for Documentation Owner, Repository Maintainer, Security and Compliance Operator, Product and Business Operator, External Contributor and End User roles;
- kept managed product localisation outside authoritative technical documentation;
- left archived repositories outside analysis and migration.

Acceptance evidence required before merge:

1. documentation-language and Markdown-structure workflow passes;
2. public baseline validation passes;
3. no Russian or other non-English prose remains in canonical documentation;
4. public status, security and repository ownership statements remain consistent;
5. the Pull Request records final checks and rollback.

## Public baseline completed previously

- English-only canonical public source and core documentation established.
- Trust-plane architecture, deployment state machine and mutable-data recovery boundary published.
- Capability, delivery and funding status reporting normalised.
- Nix input updated to NixOS 26.05 and the read-only node probe packaged.
- Hostname-derived node identifier replaced with a process-ephemeral identifier.
- Local HTTP service hardened with method restrictions, timeouts, security headers and tests.
- CI strengthened with Go race tests, vet, schema validation, Rego tests, Nix evaluation and full-history secret scanning.
- Grant alignment, competitive landscape, status, quick-start, evidence and FAQ documentation added.
- Versioned change-plan schema, synthetic examples and policy tests added.

## Ordered implementation backlog

### P0 — merge and release hygiene

- [ ] Merge the English-only documentation migration through the protected branch.
- [ ] Record the final commit, workflow runs and rollback reference.
- [ ] Resolve every deterministic, Go, Nix, schema, policy and secret-scanning failure before release.
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
- [ ] Publish the MQTT contract and a synthetic sensor or actuator simulator.
- [ ] Ensure actuator actions use allowlists, capability gates and explicit approval.

Acceptance: a non-destructive public demo succeeds, and hostile or ambiguous requests fail closed.

### P4 — hardware evidence

- [ ] Validate a CPU-only x86_64 profile.
- [ ] Validate one integrated-GPU profile and one discrete-GPU profile.
- [ ] Publish aarch64 and storage or NAS experimental profiles.
- [ ] Implement disabled-by-default Intel AMT, Redfish and IPMI simulators before real hardware control.

Acceptance: every claim links to an exact commit, release, firmware assumptions, test date, privacy-minimised evidence and rollback procedure.

### P5 — community and upstream work

- [ ] Open discussions with NixOS or nixpkgs, Home Assistant, MQTT and relevant Fediversity projects before duplicating reusable work.
- [ ] Publish contribution templates for hardware evidence, change-plan fixtures and security review.
- [ ] Record upstream issues and patches where ownership belongs upstream.

## Known limitations

- No public end-to-end Voice-to-GitOps runtime exists yet.
- No hardware profile is publicly validated yet.
- Atomic activation, health validation and recovery remain planned.
- The Home Assistant adapter remains in private testing.
- No production-ready release is claimed.
- NGI Fediversity support is requested, not awarded.

## Rollback

Before merge, close the Pull Request and retain `main`. After merge, revert the exact merge commit through a focused Pull Request, rerun the complete validation ladder and update status and evidence records. Do not restore bilingual durable documentation or analyse archived repositories.
