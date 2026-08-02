# NGI Fediversity alignment

**Proposal:** CLARYEL Box Core: Voice-to-GitOps NixOS for Private AI and Hardware-Integrated Edge Systems
**Requested support:** EUR 50,000
**Funding state:** requested, not awarded

Official programme page: https://nlnet.nl/fediversity/
Applicant guide: https://nlnet.nl/fediversity/guideforapplicants/
Eligibility: https://nlnet.nl/fediversity/eligibility/

## Programme fit

NGI Fediversity focuses on an open, portable, trustworthy hosting stack built around NixOS and reproducible deployment. Box Core directly targets that layer: public NixOS modules, portable desired state, local user control, replaceable providers, hardware-aware profiles, safe activation and recovery.

The proposal is not for a closed appliance. Every grant-funded software result remains independently usable under a recognised free and open-source licence.

## Evaluation criteria mapping

### Technical excellence and feasibility

**Strengths**

- a precise end-to-end control loop and trust-plane architecture;
- versioned desired-state, hardware-profile and change-plan schemas;
- deterministic risk policy with forbidden and approval-gated actions;
- an experimental Nix flake, non-destructive NixOS module and read-only node capability service;
- public CI, secret scanning and clean-export provenance;
- explicit separation of NixOS generation rollback from mutable-data recovery;
- bounded first target: CPU-only x86_64 before broader hardware validation.

**Risks**

- the public Voice-to-GitOps runtime does not yet exist;
- Home Assistant/MQTT integration remains in private testing;
- activation, health validation and rollback controller remain planned;
- hardware diversity and stateful recovery can exceed the available effort;
- the project is founder-led.

**Controls**

- milestone acceptance is evidence-based;
- unsupported capabilities fail closed;
- private prototypes cannot satisfy public acceptance criteria;
- wider products and robotics are excluded;
- the project can reduce scope during MoU negotiation without weakening the open-core result.

### Relevance, impact and strategic potential

**User problem**

Small organisations and households increasingly want local AI, storage and automation but lack a safe way to operate heterogeneous systems. Direct shell administration is inaccessible; cloud control can expose sensitive content; opaque appliances reduce portability and recovery.

**Public impact**

- reproducible private-AI and edge nodes on user-controlled hardware;
- safer administration for non-specialists without direct voice-to-shell execution;
- portable configuration independent of one forge, tunnel provider or hardware vendor;
- reusable schemas, policy and hardware evidence for other NixOS projects;
- practical Home Assistant integration for physical-world systems;
- public failure and recovery evidence from a continuously used reference deployment.

**Strategic value**

Box Core links reproducible software delivery to owner-controlled physical infrastructure. This is useful for households, professional offices, community organisations and small enterprises that cannot justify a large platform team but require privacy and recoverability.

### Cost effectiveness and value for money

- no customer equipment, workstation, VAT, advertising or general overhead is charged;
- existing infrastructure and prototypes are contributed as background;
- technical work is costed at EUR 56.25 per hour including applicable labour-related costs;
- every milestone produces public code, tests, documentation and evidence;
- the same open core reduces the cost and risk of CLARYEL's commercial appliance, creating a maintenance incentive;
- the proposal is prepared to refine scope and amount during negotiation.

See `BUDGET.md` for the complete work-package mapping.

## Open-source completeness

Funded:

- NixOS modules and packaging;
- Voice-to-GitOps contracts and runtime;
- policy and approval gates;
- Home Assistant/MQTT integration;
- hardware profiles and evidence;
- activation, health, rollback and recovery contracts;
- CI, tests, documentation, accessibility and reference deployment.

Not funded:

- commercial appliance operations;
- customer equipment and customer deployments;
- support tickets, CMDB, logistics and SLA workflows;
- adjacent CLARYEL products;
- general website runtime;
- the wider external commercial security audit;
- robotics integration.

The open result does not require a CLARYEL subscription.

## Interoperability and upstream strategy

Box Core should consume and contribute to existing work rather than fork avoidably:

- NixOS/nixpkgs for modules and packages;
- Home Assistant and MQTT for local interaction and physical devices;
- SelfPrivacy-style catalogues for service definitions where compatible;
- nix-fleet for optional central fleet operation;
- NixEdgeOpt for optional future placement optimisation;
- NixOS verified-boot work for a stronger trusted activation chain;
- WireGuard, Cloudflare Tunnel or another adapter for optional remote access.

## Public evidence package

| Claim | Current evidence | Gap |
|---|---|---|
| Public open baseline exists | Repository, licence, CI and governance | No production release |
| Configuration excludes secrets and content | Schemas, policy and synthetic examples | Runtime enforcement not end-to-end |
| Hardware discovery is privacy-minimised | Go service and tests | No validated hardware profile |
| Voice changes are reviewable | Change-plan schema and policy tests | Public intent interpreter not implemented |
| NixOS is reproducible | Pinned flake and module | Clean-runner build and VM activation evidence incomplete |
| Funding boundary is transparent | Grant, budget, milestones and machine-readable status | Final MoU not established |
| Commercial sustainability exists | Open-core support model | Market adoption remains unproven |

## Reviewer questions answered

### Is this just an appliance application?

No. The funded result is the complete public core. The appliance is a separately financed qualification and support channel.

### Is this just a collection of existing tools?

The project intentionally builds on existing tools. Its engineering contribution is the constrained change contract, deterministic risk/approval boundary, hardware-aware activation evidence and recovery model connecting them.

### Why voice?

Voice is an input channel for non-specialists, not deployment authority. It produces an inspectable proposal. The same contract supports text, API and local CLI inputs.

### Why Home Assistant?

It already provides mature local apps, voice pipelines, sensors, actuators and integrations. Box Core avoids rebuilding that interface and focuses on safe infrastructure state.

### Why NixOS?

NixOS provides declarative whole-system configuration, pinned generations and atomic switching. Box Core adds the missing intent, policy, hardware and state-recovery boundaries for the target use case.

### Why will the open core be maintained?

CLARYEL's commercial appliance and support activity uses the same core. Maintaining upstream releases reduces commercial support, recovery and qualification costs.

## Readiness assessment

| Dimension | Current assessment |
|---|---|
| Programme fit | Strong |
| Problem relevance | Strong |
| Differentiation | Credible but must remain precise |
| Public starting evidence | Moderate |
| Feasibility within EUR 50,000 | Moderate; scope discipline required |
| Community and upstream evidence | Early |
| Delivery concentration risk | High |
| Sustainability rationale | Strong |

## Highest-priority improvements

1. Merge a green English-only public baseline with schema and policy tests.
2. Publish the accessible classic grant brief alongside the immersive site.
3. Implement one complete low-risk intent-to-change demo before broadening hardware scope.
4. Produce clean-runner x86_64 build and NixOS VM activation evidence.
5. Obtain an external technical review or contributor commitment.
6. Publish the first failed-deployment rollback report.
7. Keep every ecosystem claim outside the paid deliverables unless the MoU explicitly includes it.
