# Threat model

## Assets

- customer data and local AI knowledge;
- credentials, keys, tunnel tokens and recovery material;
- desired-state integrity and Git history;
- deployment and approval authority;
- hardware-control and out-of-band interfaces;
- backups, recovery points and mutable application state;
- public release and software-supply-chain integrity;
- public evidence and funding-status accuracy.

## Trust assumptions

- The customer-controlled node is the only place that may hold decrypted customer content.
- Git-compatible desired-state repositories contain technical configuration and typed secret references only.
- Human approval is required for high-, medium- and unknown-risk changes according to policy.
- External services may fail or be compromised and are therefore replaceable adapters.
- NixOS configuration rollback does not automatically restore mutable application data.
- A private prototype provides no public trust until its reviewed implementation and tests are released.

## Primary adversaries and failure sources

- accidental or ambiguous administrator input;
- prompt injection through documents, webpages, sensor text or voice input;
- malicious or compromised contributor accounts;
- compromised forge, CI runner, cache or dependency;
- unauthorised local or remote user;
- compromised remote-access or hardware-management provider;
- unsafe update, migration or recovery logic;
- accidental disclosure during private-to-public export;
- misleading status or funding claims.

## Threats and controls

| Threat | Primary controls | Residual risk |
|---|---|---|
| Misheard or ambiguous voice request | Explainable plan, text confirmation, schema validation and risk-based approval | Human may still approve a poor plan; diff quality and warnings remain critical |
| Prompt injection through local content | Separate administrative channel, constrained schema, allowlisted actions and no direct shell execution | Model interpretation remains untrusted input |
| Arbitrary command smuggling | No free-form command field, action allowlist, policy denial and generated configuration review | New adapters can expand attack surface and require review |
| Malicious Git commit | Branch protection, verified review, policy checks, tests and pinned dependencies | Forge or reviewer compromise remains possible |
| Secret committed to Git | References-only design, scanners, synthetic examples and rejection policy | Novel secret formats can evade scanners; human review remains required |
| Customer content copied into configuration | Strict schemas, data-boundary review and separate mounts | Metadata fields require continued minimisation review |
| Unsafe activation | Build before activation, dry run, bounded health checks and rollback target | A health check may miss semantic failure |
| Rollback corrupts mutable state | Migration gates, backup/restore contracts and separation of generation rollback from data recovery | Some application migrations may be irreversible |
| Compromised remote-access provider | Optional adapter, outbound-first connection, local authentication and rapid revocation | Provider metadata and account compromise remain risks |
| Abuse of Intel AMT, Redfish or IPMI | Disabled by default, separate credentials, isolated management path, least privilege and audit | Firmware vulnerabilities and vendor-specific behaviour remain |
| Supply-chain compromise | Pinned inputs, dependency review, reproducible builds, SBOM and release metadata | Reproducibility depends on complete source and build transparency |
| Privacy leak from capability discovery | No hostname, address, serial number or topology; ephemeral identifier; minimal fields | CPU and platform combinations can still contribute to fingerprinting |
| Public export leaks private information | Clean history, secret/PII/topology/licence review, synthetic fixtures and human approval | Contextual identifiers may escape automated detection |
| Website overstates implementation | Canonical status model and separate source/deployment/browser states | Manual copy can drift from repository evidence |
| Grant status is misstated | Machine-readable requested/not-awarded state and review gate | External pages may cache outdated text |

## Forbidden ordinary workflow actions

The standard Voice-to-GitOps workflow cannot authorise:

- deletion of customer data or backups;
- disk repartitioning or filesystem destruction;
- key rotation or recovery-key invalidation;
- disabling security, logging or approval controls;
- exposing a service to the public internet;
- enabling out-of-band hardware control;
- changing the policy engine or its own approval requirements;
- arbitrary shell execution.

A future exceptional workflow would require a separately designed threat model, multi-party approval where appropriate and an explicit recovery plan.

## Security boundaries

### Natural-language boundary

Language models and speech recognition are untrusted proposal generators. Their output must conform to a versioned change-plan schema and is evaluated as data.

### Git boundary

A commit is a proposed technical state, not deployment authority. The target node selects only an approved, pinned revision after local policy evaluation.

### Build boundary

Build success is not activation success. Activation requires declared service and hardware health evidence.

### Data boundary

Customer content does not participate in infrastructure decisions unless an explicitly authorised, minimised signal is produced locally. Raw content is not sent to the forge or support plane.

### Hardware boundary

Discovery is read-only and privacy-minimised. Management actions use separate adapters and credentials and are disabled unless both capability and local policy permit them.

## Recovery analysis

Every stateful service must declare:

- mutable paths and ownership;
- migration direction and reversibility;
- backup preconditions;
- restore procedure and integrity checks;
- expected recovery time and data-loss window;
- interaction with NixOS generation rollback.

A rollback that restores system configuration while leaving data incompatible is a failed recovery.

## Future robotics boundary

Domestic and industrial robot integration is outside the current grant scope. Any future adapter must keep sensitive sensor streams local, expose explicit capabilities, require consent and prevent direct unreviewed model-to-actuator control.