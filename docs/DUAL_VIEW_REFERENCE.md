# Dual-view reference implementation

Status: architectural reference
Date: 2026-08-01

CLARYEL Box Core is the native interaction reference for the CLARYEL website dual-view standard.

## Reference behavior

The public Box Core experience exposes a visible switch between:

- **Immersive 3D** — the primary spatial presentation of the open-core project, architecture and implementation scope.
- **Classic 2D** — the structured grant, architecture, evidence and competitive-landscape presentation.

Both modes preserve the current locale and a visitor can restore the selected view. The switch is accessible by keyboard and remains usable on mobile and RTL documents.

## Managed and native adoption

The visual and interaction pattern is reused by the private managed runtime in `claryel-company/claryel-space`. Box Core itself keeps its native implementation and is excluded from double mounting.

The managed runtime applies the contract to:

- CLARYEL Box;
- CLARYEL Space;
- CLARYEL Solar;
- CLARYEL Funding;
- CLARYEL ID;
- newly generated managed sites.

CLARYEL Web Community is an accepted independent native owner. Its architecture presentation implements an in-page Immersive 3D / Classic 2D switch in all twenty locales, while `/classic/` remains a separate voice-first workspace rather than the Classic presentation route.

Each project owns the information architecture of its Classic 2D presentation. The managed platform owns the shared switch, mode persistence, locale-preserving navigation, accessibility safeguards and conformance checks for managed sites. Accepted native owners validate the same interaction contract in their own repositories.

Functional routes such as identity login, Solar Live, Universe and the Community voice workspace are kept separate from presentation-mode switching.

## Public/private boundary

This repository documents and demonstrates the public open-core reference. It does not contain the private managed-site gateway, private deployment credentials, internal production topology or private product repositories.

Source availability, merge status, Cloudflare deployment and production verification are separate states. This document records the architecture reference only and does not claim that a particular managed-platform pull request has already reached production.
