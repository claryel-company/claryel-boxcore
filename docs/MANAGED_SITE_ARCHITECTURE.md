# Managed website architecture

## Source ownership

The open-source implementation, governance, NixOS modules, schemas and canonical public technical documentation live in this repository: `claryel-company/claryel-boxcore`.

The production website `https://boxcore.claryel.space/` is assembled, tested and deployed by the managed CLARYEL web platform in `claryel-company/claryel-space`, under:

- `public/sites/boxcore/index.html`;
- `public/sites/boxcore/assets/boxcore-experience.js`;
- `public/sites/boxcore/assets/boxcore-experience.css`;
- `public/sites/boxcore/i18n/`;
- the shared language runtime under `public/sites/box/assets/`.

The managed website source is authoritative for visual behaviour, user-facing localisation, routing and deployment. This public repository remains authoritative for canonical English project facts, open-core implementation, technical scope, implementation status and public evidence.

## Language interaction contract

Box Core uses the shared twenty-language website contract, including Russian, because user-facing localisation is separate from public-source governance. Public source, issues and canonical documentation remain English-only under `docs/LANGUAGE_POLICY.md`.

The native Box Core controller renders the language orbit and preserves the active scene or classic view. The shared delegated language bridge provides resilient flag selection after pointer-capture loss or DOM replacement and gesture-unlocked ratchet audio for drag, wheel and direct flag selection.

A translated website string must not change technical scope, funding state, implementation status, security boundaries or legal meaning. When presentation text differs, the versioned English facts in this repository are authoritative.

## Presentation modes

The managed site provides two complementary presentations:

- **Immersive view:** the twelve-state 3D experience used across managed CLARYEL sites.
- **Classic view:** an accessible two-dimensional grant brief that does not depend on WebGL, animation or spatial navigation.

The selected mode is part of restorable URL state. Pointer, touch and keyboard input must all work. Essential grant information, honest implementation status, competitor differentiation, scope, budget and evidence links must remain available in the classic view.

## Delivery evidence

Source, merged Pull Request, deployed site and browser validation are separate delivery states. A complete website release record identifies:

1. the exact `claryel-space` commit;
2. required checks and Pull Request;
3. Cloudflare Worker dry run and production deployment;
4. exact-domain HTTP validation;
5. desktop Chromium, Android-class Chromium, desktop WebKit and iPhone-class WebKit evidence;
6. keyboard, reduced-motion, language and classic-view checks;
7. rollback reference and remaining limitations.