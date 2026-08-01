# CLARYEL Box Core architecture / Архитектура CLARYEL Box Core

## 1. Goal / Цель

CLARYEL Box Core provides a reproducible open infrastructure core for private AI and hardware-integrated edge systems. The authoritative desired state is declarative; user data and secrets remain local.

CLARYEL Box Core предоставляет воспроизводимое открытое инфраструктурное ядро для приватного ИИ и аппаратно-интегрированных edge-систем. Авторитетное желаемое состояние является декларативным; пользовательские данные и секреты остаются локально.

## 2. Main flow / Основной поток

`Voice or text intent → local interpretation → explainable change plan → Git branch or commit → schema and policy validation → approval gate → pinned NixOS build → dry run → atomic activation → service and hardware health checks → success or rollback`

`Голосовое или текстовое намерение → локальная интерпретация → понятный план изменений → Git-ветка или commit → проверка схемы и политик → подтверждение → закреплённая сборка NixOS → dry run → атомарная активация → проверка сервисов и оборудования → успех или откат`

## 3. Trust planes / Контуры доверия

### 3.1. Public source plane / Публичный контур исходного кода

Contains open code, schemas, generic hardware profiles, public examples, documentation, tests and release metadata.

Содержит открытый код, схемы, универсальные аппаратные профили, публичные примеры, документацию, тесты и metadata релизов.

### 3.2. User-owned desired-state plane / Контур желаемого состояния пользователя

A Git-compatible repository may describe multiple systems such as home, office and community nodes. It contains technical configuration only.

Git-совместимый репозиторий может описывать несколько систем: домашние, офисные и общественные узлы. Он содержит только техническую конфигурацию.

### 3.3. Local secret plane / Локальный контур секретов

Credentials, cryptographic keys and recovery material remain in a local secret store or hardware-backed facility. Git stores references, never values.

Учётные данные, криптографические ключи и материалы восстановления остаются в локальном secret store или аппаратно защищённом хранилище. Git хранит ссылки, но не значения.

### 3.4. Local data plane / Локальный контур данных

Customer documents, databases, object storage, vector indexes, model prompts, voice recordings and RAG content remain on customer-controlled infrastructure.

Клиентские документы, базы данных, объектное хранилище, векторные индексы, prompts моделей, голосовые записи и содержимое RAG остаются в инфраструктуре под контролем клиента.

### 3.5. Optional access plane / Опциональный контур доступа

Remote access adapters may include Cloudflare Tunnel, WireGuard or other compatible backends. They are optional and do not own configuration truth or customer data.

Адаптеры удалённого доступа могут включать Cloudflare Tunnel, WireGuard и другие совместимые backends. Они опциональны и не владеют истиной конфигурации или клиентскими данными.

## 4. Component boundaries / Границы компонентов

| Component / Компонент | Responsibility / Ответственность |
|---|---|
| NixOS modules | Reproducible services, users, networking, storage integration and generation management. / Воспроизводимые сервисы, пользователи, сеть, интеграция хранилища и управление генерациями. |
| Voice-to-GitOps | Convert local administrative intent into an explainable proposed change. / Преобразовывать локальное административное намерение в понятное предлагаемое изменение. |
| Policy engine | Classify risk, reject forbidden changes and require approval. / Классифицировать риск, отклонять запрещённые изменения и требовать подтверждение. |
| Deployment controller | Build, dry-run, activate, verify and roll back. / Собирать, выполнять dry run, активировать, проверять и откатывать. |
| Home Assistant adapter | User interface, voice entry, sensor and actuator integration. / Пользовательский интерфейс, голосовой ввод, интеграция датчиков и исполнительных устройств. |
| Hardware profiler | Discover capabilities and select validated profiles. / Обнаруживать возможности и выбирать проверенные профили. |
| Out-of-band adapters | Optional Intel vPro/AMT, Redfish and IPMI recovery actions. / Опциональные действия восстановления Intel vPro/AMT, Redfish и IPMI. |
| Observability | Local metrics, logs, health evidence and privacy-preserving status summaries. / Локальные метрики, логи, evidence состояния и приватные сводки статуса. |

## 5. Hardware integration / Аппаратная интеграция

Hardware profiles are explicit and capability-gated. A profile declares architecture, CPU, memory, storage, accelerators, TPM, secure boot, network, sensors and out-of-band management. Destructive or remote-control capabilities are disabled unless the profile and local policy permit them.

Аппаратные профили являются явными и включаются только при подтверждённой поддержке. Профиль описывает архитектуру, CPU, память, хранилище, ускорители, TPM, secure boot, сеть, датчики и out-of-band управление. Разрушающие или удалённые действия выключены, пока профиль и локальная политика не разрешат их.

## 6. Public and private boundary / Публичная и приватная граница

The public repository contains reusable implementation and evidence. Private repositories retain deployment-specific commercial runtime, customer configuration, support operations, CMDB, logistics, SLA, private topology and confidential security work.

Публичный репозиторий содержит повторно используемую реализацию и evidence. Приватные репозитории сохраняют deployment-специфичный коммерческий runtime, клиентские конфигурации, поддержку, CMDB, логистику, SLA, приватную топологию и конфиденциальные security-работы.

## 7. Website boundary / Граница сайта

The public website runtime belongs to `claryel-space`. This repository owns versioned public content and status data consumed by the managed site at `boxcore.claryel.space`.

Публичный web-runtime принадлежит `claryel-space`. Этот репозиторий владеет версионированным публичным содержимым и данными статуса, используемыми управляемым сайтом `boxcore.claryel.space`.
