# Demonstration and evidence plan

The public reference deployment is a validation method, not a marketing-only demo. Every demonstrated capability must link to a reproducible source revision, inputs, checks and known limitations.

## Demo 0 — current read-only public baseline

**Goal:** show that the repository can expose privacy-minimised local capabilities without mutation.

**Inputs**

- `cmd/boxcore-node`;
- a supported Linux development environment;
- no credentials or private services.

**Procedure**

```bash
go test -race ./...
go run ./cmd/boxcore-node discover
go run ./cmd/boxcore-node serve --listen 127.0.0.1:8091
curl --fail --silent http://127.0.0.1:8091/health
curl --fail --silent http://127.0.0.1:8091/capabilities
```

**Expected evidence**

- ephemeral node identifier;
- operating system, architecture and CPU-thread count only;
- no hostname, address, serial number, credential or topology;
- GET/HEAD-only HTTP boundary;
- no privileged mutation.

**Current status:** `experimental`.

## Demo 1 — low-risk Voice-to-GitOps proposal

**Goal:** convert a synthetic local request to enable loopback-only metrics into an explainable change plan.

**Steps**

1. Submit the synthetic intent from `examples/change-plan-low-risk.json`.
2. Produce a plan conforming to `schemas/change-plan.schema.json`.
3. Validate the affected desired-state paths.
4. Evaluate `policy/risk-policy.rego`.
5. Confirm classification as `low`.
6. In `automatic-low-risk` mode, create a Git-compatible proposal without human approval.
7. Build and dry-run the pinned NixOS generation.
8. Activate, verify loopback-only metrics and record the result.
9. Inject a failed health check and verify rollback.

**Required evidence**

- original synthetic intent;
- generated plan and exact diff;
- policy decision;
- approved revision;
- Nix build result;
- activation and health output;
- rollback target and result;
- confirmation that no customer content or secret values were processed.

## Demo 2 — hostile or ambiguous request

**Goal:** prove that natural-language input cannot bypass policy.

Test cases:

- request to run an arbitrary shell command;
- prompt injection embedded in a local document;
- request to disable approval or logging;
- request to expose a service publicly;
- ambiguous request affecting several services;
- request containing a secret value;
- request requiring an undeclared hardware capability.

**Acceptance**

- forbidden actions are rejected;
- unknown actions fail closed and require human review;
- customer content is not copied into the plan;
- no branch, build or activation occurs after a denial;
- the public report contains synthetic data only.

## Demo 3 — Home Assistant and MQTT

**Goal:** show a safe physical-world integration without controlling a real customer device.

**Fixture**

- synthetic temperature sensor;
- simulated relay or light;
- local Home Assistant instance;
- local MQTT broker;
- no cloud account.

**Flow**

1. A local request proposes enabling the synthetic integration.
2. Box Core generates an inspectable desired-state diff.
3. Policy identifies the declared sensor and actuator capabilities.
4. Human approval is required for actuator enablement.
5. The NixOS generation is built and activated.
6. Home Assistant reports the synthetic sensor and actuator.
7. A failed validation removes the integration through rollback.

**Safety evidence**

- allowlisted topics and entity identifiers;
- no arbitrary service calls;
- actuator disabled by default;
- bounded rate and state transitions;
- local-only network path;
- separate secret reference.

## Demo 4 — stateful service recovery

**Goal:** demonstrate that configuration rollback and mutable-data recovery are different and both work.

**Fixture**

A synthetic database with generated records and a versioned migration.

**Failure cases**

- service fails before migration;
- migration succeeds but health validation fails;
- previous NixOS generation is incompatible with the migrated data;
- restore checksum fails;
- backup is unavailable.

**Acceptance**

- Box Core never describes generation rollback as a data restore;
- irreversible migration requires a recovery contract and human approval;
- backup integrity is verified before activation;
- failure produces either a known-safe rollback or `manual-recovery-required`;
- data-loss window and recovery time are reported.

## Demo 5 — hardware profiles

Validate in order:

1. x86_64 CPU-only node;
2. one integrated-GPU node;
3. one discrete-GPU node;
4. one aarch64 node;
5. one storage/NAS or virtualised node;
6. a synthetic out-of-band adapter;
7. real Intel AMT, Redfish or IPMI only after simulator and trust-boundary tests.

Each evidence record includes firmware assumptions, exact profile, commit, release, date, test procedure, results, power/thermal notes where relevant, limitations, upgrade, rollback and recovery.

## Demo 6 — forge and access portability

**Goal:** prove that hosted providers are adapters.

Run the same desired-state proposal through:

- local Git without a network forge;
- a self-hosted Git-compatible forge;
- a hosted forge adapter.

For optional access, demonstrate at least one local VPN path and one outbound tunnel adapter. Secret values remain local and provider revocation is tested.

## Public evidence structure

Each record uses:

```text
Evidence ID
Capability and canonical status
Source commit and release
Environment and declared hardware profile
Synthetic input or public fixture
Procedure
Expected result
Observed result
Security and privacy review
Failure and rollback result
Known limitations
Reviewer and date
```

## Website evidence

The managed site at `boxcore.claryel.space` is a separate delivery surface. Site evidence must record:

- exact `claryel-space` source commit;
- Pull Request and required checks;
- Cloudflare dry-run and deployment workflow;
- deployed commit or artefact identifier;
- exact-domain HTTP validation;
- desktop Chromium, Android-class Chromium, desktop WebKit and iPhone-class WebKit audit;
- keyboard, reduced-motion and classic-view accessibility;
- rollback reference.

A source page, merged Pull Request, deployed site and browser audit are never collapsed into one status.

## Privacy rules

- use synthetic identifiers and data;
- remove hostnames, serial numbers, addresses and private topology;
- do not publish raw prompts containing private content;
- minimise hardware fingerprints;
- obtain explicit permission for any third-party validator evidence;
- delay security-sensitive detail until remediation is available.