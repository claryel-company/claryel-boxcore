# Security policy

## Reporting a vulnerability

Do not open a public issue for a vulnerability that may expose credentials, customer data, private topology, destructive hardware operations or an exploitable deployment path.

Use GitHub private vulnerability reporting for this repository when available. If that interface is unavailable, contact the CLARYEL organisation administrators through a non-public channel and include only the minimum information required to establish a secure reporting path.

Do not include real credentials, customer data, private addresses, serial numbers or production logs in an initial report.

## Supported status

This repository is an early public baseline and is not production-ready. No deployment should rely on an experimental capability without independent review, local safeguards and a tested recovery path.

Canonical capability status is defined in `docs/STATUS_MODEL.md`.

## Security invariants

- Git contains no secret values, customer content or voice recordings.
- Natural-language input never directly executes arbitrary shell actions.
- Voice input never bypasses schema validation, policy, review or approval.
- High-risk, unknown and destructive operations are denied or require explicit human approval according to policy.
- Disk repartitioning, data deletion, key rotation, backup destruction and public exposure cannot be approved by voice alone.
- Hardware-management actions require a declared capability, isolated credentials, local authorisation and audit evidence.
- Remote access is optional, outbound-first where practical, separately authenticated and revocable.
- Configuration rollback does not replace backup and recovery of mutable data.
- Public examples use synthetic identifiers, domains, addresses and data.
- Support tooling does not require access to customer content.

## Public-export checks

Every private-to-public export requires:

1. exact source provenance;
2. secret and credential scanning;
3. personal-data, customer-data and private-topology review;
4. licence and third-party-rights review;
5. dependency and supply-chain review;
6. replacement of real data with synthetic fixtures;
7. public tests and human approval.

## Severity guidance

Treat the following as potentially critical:

- bypass of approval or policy gates;
- remote arbitrary code execution;
- exposure of secret values or customer content;
- unauthorised public network exposure;
- unauthorised out-of-band hardware control;
- rollback or recovery behaviour that destroys mutable data;
- supply-chain compromise of a released configuration.

## Disclosure lifecycle

1. Private receipt and acknowledgement.
2. Reproduction and severity classification.
3. Private remediation, regression tests and affected-version analysis.
4. Coordinated release, credential rotation and operational mitigation where applicable.
5. Public advisory after users have a safe upgrade or containment path.

## Security boundaries outside this repository

Customer operations, support tickets, private topology and the wider commercial security audit remain outside the public repository. Public status may state that a finding is withheld for security, but must not reveal exploit details before remediation.