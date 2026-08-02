# Frequently asked questions

## Is CLARYEL Box Core production-ready?

No. The repository is an early public baseline. Architecture, schemas and some experimental components exist; the end-to-end Voice-to-GitOps, activation, recovery and hardware-validation work remains incomplete.

## Has NGI Fediversity support been awarded?

No award is claimed. EUR 50,000 is the requested amount in the application package.

## Does voice directly control a server?

No. Voice is one untrusted input channel. It must produce a constrained, human-readable change plan. Schema validation, deterministic policy, tests and risk-based approval occur before any build or activation.

## Can the system run arbitrary shell commands from a prompt?

Not through the ordinary change-plan contract. `run-shell`, policy self-modification, disabling approval, disabling audit and destructive operations are forbidden by the public policy.

## What is stored in Git?

Technical desired state, schemas, reviewed changes and evidence references. Git must not contain secret values, documents, databases, prompts, voice recordings, private RAG content or customer data.

## Where are secrets stored?

In a local customer-controlled secret store or hardware-backed facility. Desired state contains typed references such as `local-secret://service/token`, never the value.

## Where does customer content remain?

On customer-controlled local encrypted storage. The forge, website and CLARYEL support plane do not require content access.

## Is rollback the same as backup?

No. NixOS generation rollback restores declarative system configuration. Databases and files require separate migration, backup and restore contracts. A configuration rollback that leaves data incompatible is a failed recovery.

## Why NixOS?

NixOS provides declarative whole-system configuration, pinned generations, reproducible builds and atomic switching. Box Core adds local intent, policy, approval, hardware evidence and mutable-state recovery boundaries for the target use case.

## Why use Git?

Git provides portable history, reviewable diffs and replaceable hosting. GitHub is supported as an adapter, but local Git and self-hosted forges remain architectural targets.

## Why use Home Assistant?

Home Assistant already provides mature local web and mobile applications, voice pipelines, sensors, actuators and integrations. Box Core uses it as an interface to the physical world while keeping technical desired state and deployment authority outside Home Assistant.

## Is Cloudflare required?

No. Cloudflare Tunnel may be an optional outbound access adapter. WireGuard or other compatible mechanisms can be used. No access provider owns configuration truth or customer content.

## Is Intel vPro required?

No. Intel AMT is an optional capability on compatible systems. Redfish and IPMI are additional adapters. All out-of-band actions are disabled by default and require isolated credentials, declared capability, local consent and audit evidence.

## What hardware is supported today?

No hardware profile is publicly validated yet. The repository publishes the schema and validation procedure. The intended order begins with CPU-only x86_64, then integrated GPU, discrete GPU, aarch64 and storage/NAS profiles.

## How is Box Core different from SelfPrivacy?

SelfPrivacy focuses on easy lifecycle management for self-hosted services. Box Core focuses on the constrained intent-to-Git control loop, private AI, hardware and physical-world integration, strict trust planes and complete-node recovery. Compatible service definitions should be reused rather than duplicated.

## How is Box Core different from nix-fleet?

nix-fleet targets central management of partially offline NixOS fleets. Box Core starts with one or a small number of owner-controlled systems, local risk approval, physical devices and customer-content isolation. Fleet transport can be integrated later.

## How is Box Core different from NixEdgeOpt?

NixEdgeOpt optimises placement and migration across many nodes from service objectives. Box Core converts human administrative intent into a bounded configuration proposal and validates the complete node. An approved Box Core state could later use NixEdgeOpt.

## Does the commercial CLARYEL Box replace the open core?

No. The commercial product is a qualification, delivery and support channel for the same public core. It may sell appliances, installation, migration, managed updates, monitoring, recovery, replacement and support. A subscription is not required to install, inspect, fork or operate the open result.

## Why is the public repository English-only while the website has many languages?

Public source needs one canonical review language. User-facing translations belong to the managed website localisation layer. The website may serve twenty locales, while source, issues and public technical documentation remain English-only.

## Can private code be copied into this repository?

Not with its private history. A component must be clean-exported or re-engineered after owner approval, secret and personal-data review, topology review, licence review, dependency review, synthetic fixtures, public tests and provenance recording.

## How can I contribute?

Start with `CONTRIBUTING.md`. Useful early contributions include schema review, negative test fixtures, NixOS VM tests, policy review, synthetic hardware evidence and accessibility review of the project site.

## How are public claims verified?

Every capability uses the status model in `docs/STATUS_MODEL.md`. Source, merge, release, deployment and browser validation are reported separately. Private prototypes do not satisfy public evidence.
