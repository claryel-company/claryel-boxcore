# CLARYEL Box Core implementation context

Read `AGENTS.md` first. The authoritative implementation context is in `ARCHITECTURE.md`, `OPEN_SOURCE_SCOPE.md`, `SECURITY.md`, `docs/STATUS_MODEL.md`, `docs/LANGUAGE_POLICY.md` and `NEXT_STEPS.md`.

## Product sentence

Local voice or text intent becomes an explainable Git-compatible change, passes schema and policy checks, receives approval according to risk, builds a pinned NixOS generation, deploys atomically, validates services and hardware, and rolls back on failure.

## Hard constraints

- This is a public English-only repository. Never introduce Russian, other working-language translations, secrets or private history.
- Customer data, voice recordings and secret values never enter Git-managed desired state.
- Natural-language input never directly executes arbitrary shell commands.
- High-, medium- and unknown-risk changes require explicit human approval.
- Hardware actions are capability-gated, separately authenticated and disabled by default.
- GitHub, Cloudflare and hardware vendors are replaceable adapters, not architectural owners.
- Home Assistant is an interaction and physical-world interface, not the owner of configuration truth.
- Configuration rollback and mutable-data recovery are separate mechanisms.
- Every public claim must expose a canonical implementation status and evidence.
- A merged commit is not proof of deployment, and a deployed page is not proof of browser validation.
