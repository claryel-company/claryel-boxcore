# Hardware compatibility

No hardware profile is considered supported merely because a device class appears in this document. Support claims require reproducible public evidence.

## Evidence levels

Use the canonical implementation status from `docs/STATUS_MODEL.md`. Hardware evidence adds two independent qualifiers:

- **CLARYEL-validated:** reproduced by CLARYEL on the declared model, firmware and release.
- **Community-reproduced:** independently reproduced by a contributor with public non-sensitive evidence.
- **Commercially qualified:** covered by a separately documented commercial support policy; this does not change the open-source implementation status.

## Initial matrix

| Profile | Architecture | Public status | Intended use |
|---|---|---|---|
| Generic CPU-only server | x86_64-linux | `planned` | Local services and small models without GPU acceleration |
| Intel integrated GPU | x86_64-linux | `planned` | Low-power local inference and media processing |
| AMD integrated GPU | x86_64-linux | `planned` | Alternative integrated acceleration profile |
| NVIDIA discrete GPU | x86_64-linux | `planned` | Larger local models and accelerated inference |
| Generic ARM node | aarch64-linux | `planned` | Low-power edge, Home Assistant and control-plane roles |
| Virtual machine | x86_64/aarch64 | `planned` | Evaluation, development and migration |
| Compatible NAS | vendor-dependent | `planned` | Storage, backup or virtualised deployment |
| Intel AMT | compatible x86_64 devices | `planned` | Optional inventory, power, diagnosis and recovery outside the operating system |
| Redfish | compatible servers | `planned` | Standards-based server inventory and recovery control |
| IPMI | compatible servers | `planned` | Legacy out-of-band management behind strict local controls |

## Required profile fields

Each public profile declares:

- profile identifier and schema version;
- exact architecture and required instruction sets;
- minimum and recommended memory;
- storage layout and mutable-data boundaries;
- accelerator type, runtime and driver requirements;
- TPM, secure boot and encryption capabilities;
- network and management interfaces;
- Home Assistant sensor and actuator capabilities;
- out-of-band management support;
- power and thermal observations where relevant;
- known limitations and destructive-operation gates;
- installation, upgrade, rollback and disaster-recovery procedure;
- exact tested commit, release, date and evidence URL.

Serial numbers, private management addresses, credentials, customer identifiers and private topology are prohibited from public evidence.

## Validation procedure

A profile is validated only after all applicable steps pass:

1. firmware and BIOS assumptions are recorded;
2. installation or rebuild is reproducible from the documented input;
3. declared services start and health checks pass;
4. storage and mutable-data boundaries match the profile;
5. accelerator runtime and representative workload are tested;
6. upgrade and rollback are exercised;
7. backup and restore are tested separately from configuration rollback;
8. management interfaces remain inaccessible unless explicitly enabled;
9. privacy-minimised evidence is published.

## Out-of-band policy

Intel AMT, Redfish and IPMI are optional adapters, not dependencies. Every remote action requires:

- a declared compatible capability;
- isolated management networking or an equivalent protected path;
- separate credentials stored outside Git;
- least-privilege policy and explicit local consent;
- an auditable request and result;
- a tested revocation and rollback path.

Power, boot and recovery actions remain disabled by default.

## Data safety

Hardware profile selection never authorises disk repartitioning, data deletion, key rotation, public network exposure or backup destruction. Those operations require separate explicit workflows and cannot be approved by voice alone.

## Current evidence gap

The repository currently publishes the schema and validation method, but no profile has public validation evidence. All matrix entries therefore remain `planned` until a profile-specific evidence record is merged.