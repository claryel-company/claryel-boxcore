# Proposed milestones

The final structure is subject to NLnet negotiation and the Memorandum of Understanding. Every milestone ends in public, independently verifiable results rather than activity-only reporting.

## M1 — Architecture, trust and release baseline

**Deliverables:** architecture, threat model, public/private boundary, language and licence policy, desired-state and change-plan schemas, status model, CI and clean-export process.

**Acceptance:** public documents and schemas are internally consistent; English-only, secret and provenance checks pass; requested funding is not represented as awarded.

## M2 — Reproducible NixOS baseline

**Deliverables:** pinned flake, baseline module, service packaging and CPU-only x86_64 profile.

**Acceptance:** a clean supported system evaluates and builds the pinned configuration; generated artefacts identify the exact source revision and dependencies.

## M3 — Voice-to-GitOps and policy

**Deliverables:** constrained local intent contract, explainable change plan, Git-compatible diff, policy engine and approval gates.

**Acceptance:** synthetic low-, medium-, high-, unknown- and forbidden-risk scenarios produce the expected deterministic result; natural-language input cannot invoke arbitrary shell actions.

## M4 — Home Assistant and MQTT integration

**Deliverables:** local voice entry, dashboard status, sensor input, safe actuator simulation and MQTT contract.

**Acceptance:** a public demo proposes, reviews and applies an approved non-destructive change; a hostile or ambiguous request fails closed.

## M5 — Atomic activation, rollback and recovery

**Deliverables:** build, dry run, activation, service and hardware health checks, failed-deployment rollback, backup/restore contracts and recovery evidence.

**Acceptance:** automated tests demonstrate successful activation, deterministic configuration rollback and a separate mutable-data recovery procedure without overwriting user content.

## M6 — Hardware profiles and optional out-of-band recovery

**Deliverables:** x86_64, aarch64, CPU, iGPU, discrete GPU, storage/NAS profiles and capability-gated Intel AMT, Redfish and IPMI adapters.

**Acceptance:** each published profile declares exact capabilities, firmware assumptions, limitations, safety gates, tested revision and privacy-minimised evidence. Unsupported capabilities fail closed.

## M7 — Public reference deployment and release

**Deliverables:** CLARYEL-operated reference deployment, release artefacts, public compatibility matrix, operator documentation, accessibility evidence, contributor onboarding and final known-limitations register.

**Acceptance:** the open core, tests, documentation and evidence are available without a subscription; source, release, deployment and browser validation states are reported separately; rollback references are documented.

## Cross-milestone release gates

Every milestone must pass:

1. licence and third-party-rights review;
2. secret, PII and topology scanning;
3. deterministic tests and schema validation;
4. status and claim review;
5. documentation and accessibility review appropriate to the deliverable;
6. explicit rollback or correction path;
7. public provenance for any private-to-public export.
