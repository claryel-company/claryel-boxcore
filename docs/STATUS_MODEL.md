# Status model

Box Core reports three independent dimensions: capability implementation, delivery evidence and funding. Combining them into one label creates misleading claims.

## Capability implementation status

| Status | Meaning | Minimum evidence |
|---|---|---|
| `planned` | A public contract, design or milestone exists, but no public implementation is available | Scope, owner, acceptance criteria and known risks |
| `experimental` | Public implementation and tests exist, but compatibility, security or operational evidence is incomplete | Source, automated tests, documentation and explicit limitations |
| `validated` | The public implementation has reproducible evidence on declared software or hardware | Exact commit/release, environment, procedure, results and independent or repeated reproduction |
| `production-ready` | A maintained release is suitable for the declared supported use | Security review, supported upgrade and rollback, compatibility matrix, recovery evidence and maintenance policy |
| `private-testing` | Relevant implementation exists privately, but is not a public deliverable | Public boundary and publication condition only; no public implementation claim |
| `withheld-security` | Publication is temporarily delayed for a concrete security reason | Non-sensitive status, accountable owner and review trigger |
| `outside-scope` | The capability is customer-specific, commercial, owned elsewhere or intentionally excluded | Clear owner and boundary |

## Invalid shortcuts

Do not use `done`, `ready`, `complete`, `in progress`, `beta` or `working` as implementation evidence. Those words may describe a task or presentation state, but they do not replace the canonical capability statuses.

## Delivery status

Delivery describes where a specific revision exists:

| Status | Meaning |
|---|---|
| `source-change-in-review` | A branch or Pull Request contains the change |
| `merged` | The exact change is on the protected default branch |
| `released` | A tagged or otherwise identified release artefact exists |
| `deployed` | The exact release or merge commit was deployed through the governed workflow |
| `browser-validated` | The deployed result passed the declared browser and accessibility audit |
| `rolled-back` | The deployment was reverted to an identified safe revision |
| `owned-elsewhere` | Another repository owns the delivery surface |
| `not-released` | No public release is claimed |
| `not-publicly-validated` | Public operational evidence does not yet exist |

A merged Pull Request is not a deployment. A deployment is not browser validation. A source marker is not test evidence.

## Funding status

| Status | Meaning |
|---|---|
| `draft` | Application material is being prepared |
| `submitted` | The application was accepted by the submission system |
| `requested-not-awarded` | A requested amount is public, but no award is claimed |
| `negotiation` | Scope or budget is being discussed before an agreement |
| `awarded` | A written award or signed agreement exists |
| `paid-partial` | At least one verified payment was received |
| `paid-final` | The final agreed payment was received |
| `closed` | The funded project and final reporting are complete |

Requested, negotiated, awarded, paid and spent amounts are separate facts.

## Evidence record

Every status transition records:

- capability or surface identifier;
- previous and new status;
- exact commit or release;
- test, workflow, deployment or external evidence;
- date and responsible reviewer;
- supported environment;
- remaining limitations;
- rollback or correction reference.

## Current top-level state

As of 2026-08-01:

- the public repository is an early baseline;
- no production-ready Box Core release is claimed;
- the end-to-end Voice-to-GitOps runtime is planned;
- the requested NGI Fediversity amount is EUR 50,000 and is not presented as awarded.