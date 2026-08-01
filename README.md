# CLARYEL Box Core

[![Validate public baseline](https://github.com/claryel-company/claryel-boxcore/actions/workflows/validate.yml/badge.svg)](https://github.com/claryel-company/claryel-boxcore/actions/workflows/validate.yml)

> **Public status:** early open baseline. This repository is intentionally incomplete while code is reviewed, sanitised and clean-exported or re-engineered from private CLARYEL repositories. A private prototype is never presented as public implementation. Customer data, credentials, production topology, support operations and commercial service internals will not be published.
>
> **Публичный статус:** ранняя открытая основа. Репозиторий намеренно неполон, пока код проверяется, очищается, чисто экспортируется или перерабатывается из приватных репозиториев CLARYEL. Приватный прототип никогда не представляется публичной реализацией. Клиентские данные, учётные данные, production-топология, процессы поддержки и внутренние механизмы коммерческого сервиса публиковаться не будут.

## Speak. Review. Deploy. Roll back. / Скажите. Проверьте. Разверните. Откатите.

CLARYEL Box Core is the free and open NixOS core for reproducible, hardware-aware local infrastructure, private AI, Home Assistant and reviewable Voice-to-GitOps workflows.

CLARYEL Box Core — свободное открытое ядро NixOS для воспроизводимой аппаратно-ориентированной локальной инфраструктуры, приватного ИИ, Home Assistant и проверяемых процессов Voice-to-GitOps.

`voice or text intent → explainable Git change → schema and policy validation → approval according to risk → pinned NixOS build → dry run → atomic activation → service and hardware health checks → success or rollback`

`голосовое или текстовое намерение → понятное Git-изменение → проверка схемы и политик → подтверждение по уровню риска → закреплённая сборка NixOS → dry run → атомарная активация → проверка сервисов и оборудования → успех или откат`

## Public baseline already present / Уже опубликованная основа

- project governance, architecture and threat model; / управление проектом, архитектура и модель угроз;
- exact public/private and grant boundaries; / точные публичные, приватные и грантовые границы;
- desired-state and hardware-profile JSON Schemas; / JSON Schemas desired state и аппаратных профилей;
- initial OPA-style risk policy; / первоначальная risk policy в стиле OPA;
- initial Nix flake and non-destructive NixOS module; / первоначальный Nix flake и неразрушающий модуль NixOS;
- privacy-minimised node capability service clean-exported from the private Node Agent; / минимизированный с точки зрения приватности сервис возможностей узла, чисто экспортированный из приватного Node Agent;
- synthetic home-system example; / синтетический пример домашней системы;
- public CI, deterministic validation and secret scanning; / публичный CI, детерминированная проверка и secret scanning;
- grant budget, milestones and machine-readable website content; / грантовый бюджет, milestones и машиночитаемый контент сайта;
- explicit implementation and private-testing gap register. / явный реестр реализации и приватно тестируемых пробелов.

## Trust boundary / Граница доверия

Git-managed configuration contains technical desired state only. It never contains customer documents, private datasets, voice recordings, credentials, cryptographic keys, secret values or local RAG content. Secrets and encrypted data remain on customer-controlled infrastructure.

Git-managed конфигурация содержит только техническое желаемое состояние. Она никогда не содержит клиентские документы, приватные наборы данных, голосовые записи, учётные данные, криптографические ключи, значения секретов или содержимое локального RAG. Секреты и зашифрованные данные остаются в инфраструктуре под контролем клиента.

## Current publication state / Текущее состояние публикации

| Area / Область | Public status / Публичный статус | Notes / Примечание |
|---|---|---|
| Architecture, governance and grant scope / Архитектура, управление и границы заявки | `implemented` | Public documents and machine-readable status exist. / Публичные документы и машиночитаемый статус существуют. |
| Nix flake and baseline module / Nix flake и базовый модуль | `experimental` | Creates safe local boundaries and performs no destructive deployment action. / Создаёт безопасные локальные границы и не выполняет разрушающие deployment-действия. |
| Node capability service / Сервис возможностей узла | `experimental` | First clean export with exact provenance; raw hostname is not exposed. / Первый чистый экспорт с точным provenance; raw hostname не раскрывается. |
| Voice-to-GitOps runtime / Runtime Voice-to-GitOps | `planned` | Policy and schemas are public; runtime implementation is not yet public. / Политика и схемы опубликованы; runtime-реализация ещё не публична. |
| Home Assistant adapter / Адаптер Home Assistant | `private-testing` | Generic adapter and non-destructive simulation are being separated. / Выделяются универсальный адаптер и неразрушающая симуляция. |
| Hardware profiles / Аппаратные профили | `planned` | CPU, iGPU, GPU, NAS, x86_64, aarch64, Intel vPro/AMT, Redfish and IPMI. / CPU, iGPU, GPU, NAS, x86_64, aarch64, Intel vPro/AMT, Redfish и IPMI. |
| Commercial support, CMDB, logistics and SLA / Коммерческая поддержка, CMDB, логистика и SLA | `outside-scope` | Remain in private commercial repositories. / Остаются в приватных коммерческих репозиториях. |

See [`PUBLICATION_STATUS.md`](PUBLICATION_STATUS.md). / См. [`PUBLICATION_STATUS.md`](PUBLICATION_STATUS.md).

## Website and ecosystem / Сайт и экосистема

- Managed Box Core site, prepared for publication: **https://boxcore.claryel.space**
- CLARYEL Universe: **https://claryel.space/universe/**
- CLARYEL Web Community: **https://github.com/claryel-company/claryel-web-community**
- Commercial CLARYEL Box: **https://claryel.com**

The managed website uses the shared CLARYEL twenty-language and twelve-view immersive runtime. Repository source, merged Pull Request, deployed site and live browser validation remain separate status states.

Управляемый сайт использует общий двадцатиязычный иммерсивный runtime CLARYEL из двенадцати видов. Исходник репозитория, слитый Pull Request, опубликованный сайт и live browser validation остаются отдельными статусами.

## NGI Fediversity proposal / Заявка NGI Fediversity

Requested support: **EUR 50,000**. No advance payment is requested. This is a requested amount, not an award. The proposal funds the public NixOS core, Voice-to-GitOps, hardware profiles, Home Assistant integration, rollback, recovery, tests and documentation. The commercial platform and adjacent products are financed separately.

Запрашиваемая поддержка: **50 000 евро**. Аванс не запрашивается. Это запрошенная, а не присуждённая сумма. Заявка финансирует публичное ядро NixOS, Voice-to-GitOps, аппаратные профили, интеграцию Home Assistant, rollback, recovery, тесты и документацию. Коммерческая платформа и смежные продукты финансируются отдельно.

- [`GRANT_SCOPE.md`](GRANT_SCOPE.md)
- [`BUDGET.md`](BUDGET.md)
- [`MILESTONES.md`](MILESTONES.md)

## Commercial sustainability / Коммерческая устойчивость

The open stack remains independently usable without a subscription. CLARYEL plans to earn from qualified hardware-software appliances, installation, migration, managed stable updates, monitoring, recovery, equipment replacement, integrations and enterprise-grade support for small organisations and households.

Открытый стек остаётся пригодным для самостоятельного использования без подписки. CLARYEL планирует получать доход от квалифицированных аппаратно-программных комплексов, установки, миграции, управляемых стабильных обновлений, мониторинга, recovery, замены оборудования, интеграций и enterprise-поддержки для небольших организаций и домашних хозяйств.

## Documentation / Документация

- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`THREAT_MODEL.md`](THREAT_MODEL.md)
- [`OPEN_SOURCE_SCOPE.md`](OPEN_SOURCE_SCOPE.md)
- [`HARDWARE_COMPATIBILITY.md`](HARDWARE_COMPATIBILITY.md)
- [`SECURITY.md`](SECURITY.md)
- [`GOVERNANCE.md`](GOVERNANCE.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`docs/PRIVATE_EXPORT_INVENTORY.md`](docs/PRIVATE_EXPORT_INVENTORY.md)
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md)
- [`NEXT_STEPS.md`](NEXT_STEPS.md)

## Validation / Проверка

```bash
# English: Validate public files and obvious disclosure risks.
# Русский: Проверить публичные файлы и очевидные риски раскрытия.
python3 scripts/validate_public_baseline.py

# English: Test the public node-capability service.
# Русский: Протестировать публичный сервис возможностей узла.
go test ./...

# English: Evaluate the public Nix flake.
# Русский: Выполнить evaluation публичного Nix flake.
nix flake check --no-build
```

## Licence / Лицензия

Public code is currently released under Apache-2.0. Public documentation is intended for CC BY-SA 4.0 unless a file states another compatible licence. Grant negotiations may refine the licence structure without reducing the freedom of published grant-funded results.

Публичный код в настоящее время выпускается под Apache-2.0. Публичная документация предназначена для CC BY-SA 4.0, если файл не указывает другую совместимую лицензию. Переговоры по гранту могут уточнить структуру лицензирования без ограничения свободы опубликованных результатов, профинансированных грантом.
