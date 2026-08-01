# Managed website architecture / Архитектура управляемого сайта

## Source ownership / Владение исходниками

The open-source implementation, governance, NixOS modules, schemas and public technical documentation live in this repository: `claryel-company/claryel-boxcore`.

Открытая реализация, управление проектом, модули NixOS, схемы и публичная техническая документация находятся в этом репозитории: `claryel-company/claryel-boxcore`.

The production website `https://boxcore.claryel.space/` is assembled, tested and deployed by the managed CLARYEL web platform in `claryel-company/claryel-space`, under:

- `public/sites/boxcore/index.html`
- `public/sites/boxcore/assets/boxcore-experience.js`
- `public/sites/boxcore/assets/boxcore-experience.css`
- `public/sites/boxcore/i18n/`
- shared language runtime: `public/sites/box/assets/language-switch-bridge.js`

Production-сайт `https://boxcore.claryel.space/` собирается, тестируется и публикуется управляемой веб-платформой CLARYEL в репозитории `claryel-company/claryel-space`, в каталогах:

- `public/sites/boxcore/index.html`
- `public/sites/boxcore/assets/boxcore-experience.js`
- `public/sites/boxcore/assets/boxcore-experience.css`
- `public/sites/boxcore/i18n/`
- общий языковой runtime: `public/sites/box/assets/language-switch-bridge.js`

## Language interaction contract / Контракт переключения языков

Box Core exposes the shared twenty-language circular selector. The native Box Core controller renders the orbit and preserves the current scene and layer. The shared delegated language bridge provides resilient flag selection after pointer-capture loss or DOM replacement and supplies gesture-unlocked ratchet audio for drag, wheel and flag selection.

Box Core использует общий круговой переключатель из двадцати языков. Собственный контроллер Box Core строит орбиту и сохраняет текущую сцену и слой. Общий делегированный языковой мост страхует выбор флага при потере pointer capture или перестройке DOM и воспроизводит разблокируемую жестом трещотку при вращении, колесе и выборе флага.

The managed website source is authoritative for visual and deployment behaviour. This public repository remains authoritative for the open Box Core product and technical implementation boundary.

Исходники управляемого сайта являются источником истины для визуального поведения и публикации. Этот публичный репозиторий остаётся источником истины для открытого продукта Box Core и границ технической реализации.
