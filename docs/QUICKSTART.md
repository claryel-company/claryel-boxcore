# Public baseline quick start

This guide exercises the current experimental baseline. It does not install a production private-AI stack and does not claim the planned Voice-to-GitOps runtime.

## Prerequisites

- Git;
- Go version declared by `go.mod`;
- Nix with flakes enabled for Nix evaluation;
- Linux for meaningful capability output.

## Clone and validate

```bash
git clone https://github.com/claryel-company/claryel-boxcore.git
cd claryel-boxcore
python3 scripts/validate_public_baseline.py
go test -race ./...
go vet ./...
nix flake check --no-build
```

## Inspect the privacy-minimised node record

```bash
go run ./cmd/boxcore-node discover
```

Example shape:

```json
{
  "node_id": "ephemeral-0123456789abcdef",
  "os": "linux",
  "architecture": "amd64",
  "cpu_threads": 8,
  "capabilities": [
    "runtime.nixos-candidate",
    "system.health",
    "system.inventory.minimised"
  ]
}
```

The identifier is random for each process. The output intentionally excludes hostname, address, serial number, storage topology, credentials and customer telemetry.

## Run the read-only local service

```bash
go run ./cmd/boxcore-node serve --listen 127.0.0.1:8091
```

In another terminal:

```bash
curl --fail --silent http://127.0.0.1:8091/health | jq
curl --fail --silent http://127.0.0.1:8091/capabilities | jq
```

Only `GET` and `HEAD` are accepted. The service performs no privileged or mutating action.

Do not bind the experimental service to a public address without an independent security review and an explicit local authentication layer.

## Inspect the desired-state example

```bash
jq . examples/systems/home.json
```

The example contains typed references such as `local-secret://home-assistant/api-token`; it contains no secret value.

Validate it when `check-jsonschema` is available:

```bash
check-jsonschema \
  --schemafile schemas/desired-state.schema.json \
  examples/systems/home.json
```

## Inspect change plans

```bash
jq . examples/change-plan-low-risk.json
jq . examples/change-plan-high-risk.json
```

Validate both:

```bash
check-jsonschema \
  --schemafile schemas/change-plan.schema.json \
  examples/change-plan-low-risk.json \
  examples/change-plan-high-risk.json
```

These are synthetic contracts. No public interpreter currently generates them from speech or text.

## Evaluate policy

With OPA installed:

```bash
opa test policy
opa eval \
  --data policy/risk-policy.rego \
  --input examples/change-plan-low-risk.json \
  'data.claryel.boxcore.risk'
```

Expected high-level result for the low-risk example:

- `risk_level`: `low`;
- `automatic_approval_allowed`: `true`;
- `allow`: `true`.

The high-risk Redfish example requires a declared capability and explicit human approval.

## Evaluate the Nix flake

```bash
nix flake show
nix flake check --no-build
nix build .#boxcore-node
./result/bin/boxcore-node version
```

## Evaluate the NixOS module

A minimal test configuration can import the module:

```nix
{
  imports = [ /path/to/claryel-boxcore/nix/modules/boxcore.nix ];

  services.claryelBoxCore = {
    enable = true;
    systemId = "synthetic-node";
    desiredStatePath = "/etc/claryel-boxcore/desired-state";
    secretStorePath = "/var/lib/claryel-boxcore/secrets";
    approvalMode = "always-human";
  };
}
```

The current module creates protected local boundaries and runs a non-destructive baseline check. It does not deploy the planned service stack.

## Current limitations

- no public speech or text interpreter;
- no public Git proposal runtime;
- no activation and rollback controller;
- no public Home Assistant adapter;
- no validated hardware profile;
- no production-ready release.

See `PUBLICATION_STATUS.md` and `NEXT_STEPS.md` before relying on any capability.