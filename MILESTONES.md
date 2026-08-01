# Proposed milestones / Предлагаемые milestones

The final milestone structure is subject to NLnet negotiation and the Memorandum of Understanding.

Окончательная структура milestones определяется переговорами с NLnet и Memorandum of Understanding.

## M1 — Public architecture and trust model / Публичная архитектура и модель доверия

**Deliverables / Результаты:** architecture, threat model, public/private boundary, licence policy, desired-state schema and initial CI.  
**Acceptance / Приёмка:** public documents, schema validation and clean-export checks pass.

**Результаты:** архитектура, модель угроз, публичная/приватная граница, политика лицензирования, схема desired state и первоначальный CI.  
**Приёмка:** публичные документы, проверка схем и clean-export checks проходят.

## M2 — Reproducible NixOS baseline / Воспроизводимая основа NixOS

**Deliverables / Результаты:** flake, baseline module, service packaging, x86_64 CPU profile and reproducible build evidence.  
**Acceptance / Приёмка:** a clean machine evaluates and builds the pinned configuration.

**Результаты:** flake, базовый модуль, упаковка сервисов, CPU-профиль x86_64 и evidence воспроизводимой сборки.  
**Приёмка:** чистая машина выполняет evaluation и сборку закреплённой конфигурации.

## M3 — Voice-to-GitOps and policy / Voice-to-GitOps и политики

**Deliverables / Результаты:** local intent contract, explainable change plan, Git-compatible change, risk classification and approval gates.  
**Acceptance / Приёмка:** synthetic low-, medium-, high- and forbidden-risk scenarios produce expected policy outcomes.

**Результаты:** контракт локального intent, понятный план изменений, Git-совместимое изменение, классификация риска и подтверждения.  
**Приёмка:** синтетические сценарии низкого, среднего, высокого и запрещённого риска дают ожидаемые результаты политик.

## M4 — Home Assistant and physical-world integration / Home Assistant и физический мир

**Deliverables / Результаты:** local voice entry, dashboard status, sensor input, safe actuator example and MQTT contract.  
**Acceptance / Приёмка:** a public demo proposes and applies an approved non-destructive configuration change.

**Результаты:** локальный голосовой ввод, dashboard-статус, вход датчиков, безопасный пример исполнительного устройства и MQTT-контракт.  
**Приёмка:** публичное demo предлагает и применяет подтверждённое неразрушающее изменение конфигурации.

## M5 — Atomic deployment, rollback and recovery / Атомарное развёртывание, откат и восстановление

**Deliverables / Результаты:** dry run, activation, health checks, failed-deployment rollback and supported-service recovery contracts.  
**Acceptance / Приёмка:** automated tests demonstrate successful activation and deterministic rollback without overwriting user data.

**Результаты:** dry run, активация, health checks, откат неуспешного deployment и контракты восстановления поддерживаемых сервисов.  
**Приёмка:** автоматические тесты демонстрируют успешную активацию и детерминированный откат без перезаписи пользовательских данных.

## M6 — Hardware profiles and out-of-band recovery / Аппаратные профили и out-of-band recovery

**Deliverables / Результаты:** CPU, iGPU, discrete GPU, NAS/aarch64 experimental profiles and capability-gated Intel vPro/AMT, Redfish and IPMI interfaces.  
**Acceptance / Приёмка:** each profile declares exact capabilities, limitations, safety gates and test evidence.

**Результаты:** профили CPU, iGPU, дискретного GPU, экспериментальные NAS/aarch64 и интерфейсы Intel vPro/AMT, Redfish и IPMI с проверкой возможностей.  
**Приёмка:** каждый профиль описывает точные возможности, ограничения, safety gates и evidence тестирования.

## M7 — Public reference deployment and release / Публичный reference deployment и релиз

**Deliverables / Результаты:** CLARYEL-operated reference deployment, public status, documentation, hardware matrix, website, community onboarding and final release.  
**Acceptance / Приёмка:** public repository, release artifacts, CI evidence, website and known-limitations register are available without a subscription.

**Результаты:** reference deployment под управлением CLARYEL, публичный статус, документация, аппаратная матрица, сайт, подключение сообщества и финальный релиз.  
**Приёмка:** публичный репозиторий, release artifacts, CI evidence, сайт и реестр известных ограничений доступны без подписки.
