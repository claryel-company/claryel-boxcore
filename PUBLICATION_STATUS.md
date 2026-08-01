# Public implementation status / Публичный статус реализации

**Snapshot date / Дата snapshot:** 2026-08-01

This repository is an early clean public baseline. Several capabilities exist in private experimental or commercial repositories but are not yet public because testing, sanitisation, licence review or architectural separation is incomplete.

Этот репозиторий является ранней чистой публичной основой. Некоторые функции существуют в приватных экспериментальных или коммерческих репозиториях, но ещё не опубликованы, поскольку тестирование, очистка, проверка лицензий или архитектурное разделение не завершены.

| Capability / Функция | Public status / Публичный статус | Private state / Приватное состояние | Publication condition / Условие публикации |
|---|---|---|---|
| Product architecture / Архитектура продукта | implemented | n/a | Maintained publicly. / Поддерживается публично. |
| Container service catalogue / Каталог контейнерных сервисов | planned | private-testing | Replace environment-specific definitions with generic contracts and tests. / Заменить привязанные к среде определения универсальными контрактами и тестами. |
| Nix flake / Nix flake | experimental | new public work | Complete evaluation and build checks. / Завершить evaluation и build-проверки. |
| NixOS modules / Модули NixOS | planned | private deployment logic exists in another form | Re-engineer rather than copy private deployment code. / Переработать, а не копировать приватный deployment-код. |
| Voice-to-GitOps / Voice-to-GitOps | planned | private-testing | Publish local intent, change-plan and approval contracts after threat-model review. / Опубликовать контракты локального intent, плана изменений и подтверждения после threat-model review. |
| Home Assistant / Home Assistant | experimental contract pending | private-testing | Separate generic adapter and non-destructive simulation from deployment-specific code. / Выделить универсальный адаптер и неразрушающую симуляцию из deployment-специфичного кода. |
| Atomic update and rollback / Атомарное обновление и откат | planned | private installer patterns exist | Implement as public NixOS generation workflow with state safeguards. / Реализовать как публичный workflow генераций NixOS с защитой состояния. |
| Backup and recovery / Backup и recovery | planned | private-testing | Publish service-specific state contracts and synthetic tests. / Опубликовать контракты состояния сервисов и синтетические тесты. |
| Hardware discovery / Обнаружение оборудования | planned | private node-management work exists | Export generic schema and non-sensitive probes. / Экспортировать универсальную схему и нечувствительные probes. |
| Intel vPro/AMT / Intel vPro/AMT | planned | research and commercial integration | Publish capability-gated profile; no credentials or customer topology. / Опубликовать профиль с проверкой возможностей без учётных данных и клиентской топологии. |
| Redfish/IPMI / Redfish/IPMI | planned | research and commercial integration | Publish vendor-neutral interfaces and safe defaults. / Опубликовать vendor-neutral интерфейсы и безопасные значения по умолчанию. |
| Remote support / Удалённая поддержка | outside-scope | commercial private subsystem | Public core exposes only local interfaces and consent contracts. / Публичное ядро предоставляет только локальные интерфейсы и контракты согласия. |
| CMDB, warehouse and logistics / CMDB, склад и логистика | outside-scope | commercial private subsystem | Never copied into the open core. / Никогда не копируются в открытое ядро. |
| Customer data and RAG / Клиентские данные и RAG | outside-scope | local customer data plane | Never stored in this repository. / Никогда не хранятся в этом репозитории. |
| Managed project website / Управляемый сайт проекта | in-progress | shared private web runtime | Publish at `boxcore.claryel.space`; source content remains public here. / Опубликовать на `boxcore.claryel.space`; исходное содержимое остаётся публичным здесь. |

## Honesty rule / Правило честности

A private prototype is not presented as public implementation. A merged change is not presented as deployed. A source marker is not presented as browser evidence. Every status change must cite the public commit, checks and release or deployment evidence.

Приватный прототип не представляется как публичная реализация. Объединённое изменение не представляется как опубликованное. Маркер в исходнике не представляется как браузерное evidence. Каждое изменение статуса должно ссылаться на публичный commit, проверки и evidence релиза или deployment.
