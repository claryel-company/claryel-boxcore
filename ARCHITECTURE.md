# CLARYEL Box Core architecture

## 1. Purpose

CLARYEL Box Core provides a reproducible open infrastructure core for private AI and hardware-integrated edge systems. Technical desired state is declarative and portable; secret values and user content remain local.

The architecture targets one or a small number of owner-controlled nodes rather than a mandatory central fleet service. It is designed to remain useful with local Git, a self-hosted forge or a hosted forge, and with or without a commercial CLARYEL service.

## 2. Authoritative control loop

`voice or text intent → constrained local interpretation → explainable change plan → Git-compatible branch or commit → schema validation → policy evaluation → risk-based approval → pinned NixOS build → dry run → atomic activation → service and hardware health checks → success or rollback`

Hard invariant: natural-language input proposes a declarative change. It never directly authorises arbitrary shell execution, destructive storage operations, public exposure or out-of-band hardware control.

## 3. Trust planes

### 3.1 Public source plane

Contains open code, schemas, generic hardware profiles, synthetic examples, documentation, tests, release metadata and public evidence.

It excludes customer-specific configuration, private topology, credentials, customer content, support tickets and confidential security findings.

### 3.2 User-owned desired-state plane

A Git-compatible repository may describe several independent systems, such as a home, office, laboratory or community node. It stores technical desired state and references to local secrets, never secret values or user content.

The desired-state repository can be local, self-hosted or hosted. No forge is the architectural owner of configuration truth.

### 3.3 Local secret plane

Credentials, cryptographic keys, tunnel tokens and recovery material remain in a local secret store or hardware-backed facility. Git stores typed references only.

Secret resolution occurs on the target node after an approved revision has been selected. Secret material is not rendered into a public build log or change plan.

### 3.4 Local data plane

Documents, databases, object stores, vector indexes, model prompts, voice recordings, RAG content and other customer-controlled data remain on local encrypted storage.

NixOS generation rollback applies to declarative system configuration. Mutable application data has separate migration, backup and recovery contracts; backup is never misrepresented as configuration rollback.

### 3.5 Optional access plane

Remote-access adapters may include WireGuard, Cloudflare Tunnel or another compatible backend. They are optional, outbound-first where practical, independently authenticated and rapidly revocable. They do not own desired state or customer content.

### 3.6 Optional support plane

Commercial support may receive explicitly permitted health and configuration metadata. Access to customer content is neither required nor assumed. Support operations, SLA workflows and customer records remain outside this public repository.

## 4. Component ownership

| Component | Responsibility | Public status |
|---|---|---|
| Desired-state schemas | Define technical configuration and reject undefined fields | Implemented baseline |
| Change-plan schema | Represent intent, diff summary, risk, approvals, preconditions and rollback | Implemented contract |
| Risk policy | Deny forbidden actions and determine approval requirements | Experimental policy |
| NixOS modules | Package reproducible services and local boundaries | Experimental baseline |
| Voice-to-GitOps interpreter | Convert local intent into a constrained proposed change | Planned runtime |
| Deployment controller | Build, dry-run, activate, verify and roll back | Planned runtime |
| Home Assistant/MQTT adapter | Provide local interaction, sensors and actuator integration | Private-testing boundary |
| Hardware profiler | Discover non-sensitive capabilities and select validated profiles | Experimental discovery; profiles planned |
| Out-of-band adapters | Optional Intel AMT, Redfish and IPMI recovery actions | Planned, disabled by default |
| Evidence publisher | Produce privacy-filtered status, compatibility and recovery evidence | Planned |

## 5. Change contract

Every proposed change must identify:

1. the originating channel and human-readable intent;
2. the exact desired-state paths affected;
3. a bounded set of declarative actions;
4. preconditions and expected effects;
5. risk level and policy decision;
6. required approval identities or roles;
7. build and dry-run evidence;
8. service and hardware health checks;
9. rollback target and mutable-state recovery requirements.

Unknown actions fail closed and require explicit human review. Forbidden actions cannot be approved through the ordinary Voice-to-GitOps workflow.

## 6. Deployment state machine

`proposed → schema-valid → policy-evaluated → approved → built → dry-run-passed → activated → health-validating → healthy`

Failure transitions:

- validation failure → `rejected`;
- build or dry-run failure → `failed-before-activation`;
- activation or health-check failure → `rollback-required` → `rolled-back` or `manual-recovery-required`.

No state transition may infer success from a Git commit, CI marker or process exit alone. Activation success requires declared service and hardware evidence.

## 7. Hardware integration

Hardware profiles explicitly describe architecture, CPU, memory, storage, accelerators, TPM, secure boot, networking, sensors and optional management interfaces. A profile is not considered validated until it links to a tested commit, release, date and reproducible evidence.

Out-of-band actions are disabled by default. Enabling Intel AMT, Redfish or IPMI requires a declared compatible capability, isolated management path, separate credentials, local consent, least privilege and an audit trail.

## 8. Supply-chain and release integrity

- Pin Nix inputs and dependency versions appropriate to the supported release channel.
- Evaluate on x86_64-linux and aarch64-linux before claiming support.
- Produce a dependency and licence inventory for releases.
- Sign or otherwise verifiably identify release metadata.
- Keep private export provenance independent from public Git history.
- Treat a public release, deployed reference node and browser-visible website as separate evidence surfaces.

## 9. Public/private boundary

The public repository contains reusable implementation and evidence. Private repositories retain deployment-specific commercial runtime, customer configuration, support operations, CMDB, logistics, SLA workflows, private topology and confidential security work.

Clean export is file-level and reviewable. Private Git history is never copied. Each export record identifies the exact reviewed private commit, destination, sanitisation, licence decision, excluded material and public validation.

## 10. Website boundary

The managed website runtime belongs to `claryel-company/claryel-space`. This repository owns canonical project facts, documentation, machine-readable scope and evidence consumed by the project site at `boxcore.claryel.space`.

User-facing translations are maintained by the managed-web localisation layer. Public source repositories remain English-only.

## 11. Complementarity

Box Core is intended to integrate with or consume neighbouring work where appropriate:

- SelfPrivacy-class service catalogues can supply service definitions.
- Nix Fleet can complement Box Core when central fleet operation is required.
- NixEdgeOpt can complement an approved Box Core desired state with placement optimisation.
- verified-boot work can strengthen the trusted activation chain.
- Nocloud, bewCloud and other applications can run as packaged services.

This boundary avoids rebuilding projects that already have stronger ownership while preserving the distinct local intent, hardware and recovery control loop.
