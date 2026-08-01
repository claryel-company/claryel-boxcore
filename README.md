# CLARYEL Box Core

> **Public status:** early open baseline. The repository is intentionally incomplete while code is reviewed, sanitised and exported from private CLARYEL repositories. Missing implementation is tracked explicitly; private customer data, credentials, production topology and commercial support internals will not be published.
>
> **Публичный статус:** ранняя открытая основа. Репозиторий намеренно неполон, пока код проверяется, очищается и экспортируется из приватных репозиториев CLARYEL. Отсутствующая реализация фиксируется явно; клиентские данные, учётные данные, production-топология и внутренние механизмы коммерческой поддержки публиковаться не будут.

## Purpose / Назначение

CLARYEL Box Core is the free and open core for reproducible, hardware-aware local infrastructure built around NixOS, private AI, Home Assistant and reviewable Voice-to-GitOps workflows.

CLARYEL Box Core — свободное открытое ядро воспроизводимой аппаратно-ориентированной локальной инфраструктуры на базе NixOS, приватного ИИ, Home Assistant и проверяемых процессов Voice-to-GitOps.

A spoken or written administrative request is converted locally into an explainable configuration change. The change is reviewed, validated by policy and tests, applied atomically and rolled back when health checks fail.

Голосовой или текстовый административный запрос локально преобразуется в понятное изменение конфигурации. Изменение проверяется, проходит политики и тесты, применяется атомарно и откатывается при ошибке health-check.

## Trust boundary / Граница доверия

The public configuration plane never contains customer documents, private datasets, voice recordings, credentials, cryptographic keys or local RAG content. Secrets and encrypted data remain on customer-controlled infrastructure.

Публичный контур конфигурации никогда не содержит клиентские документы, приватные наборы данных, голосовые записи, учётные данные, криптографические ключи или содержимое локального RAG. Секреты и зашифрованные данные остаются в инфраструктуре под контролем клиента.

## Current publication state / Текущее состояние публикации

| Area / Область | Status / Статус | Notes / Примечание |
|---|---|---|
| Architecture and grant scope / Архитектура и границы заявки | In publication / Публикуется | Public documents are being added first. / Сначала добавляются публичные документы. |
| NixOS modules / Модули NixOS | Planned export / Плановый экспорт | New public modules will replace private deployment-specific definitions. / Новые публичные модули заменят приватные определения, привязанные к deployment. |
| Voice-to-GitOps / Voice-to-GitOps | Skeleton pending / Ожидается каркас | Private experiments continue; only reviewed generic contracts will be exported. / Приватные эксперименты продолжаются; экспортируются только проверенные универсальные контракты. |
| Home Assistant integration / Интеграция Home Assistant | Partial private implementation / Частичная приватная реализация | Public adapter and simulation contracts are being separated. / Выделяются публичный адаптер и контракты симуляции. |
| Hardware profiles / Аппаратные профили | Planned / Планируется | CPU, iGPU, GPU, NAS, x86_64, aarch64, Intel vPro/AMT, Redfish and IPMI. / CPU, iGPU, GPU, NAS, x86_64, aarch64, Intel vPro/AMT, Redfish и IPMI. |
| Customer and commercial operations / Клиентские и коммерческие операции | Outside public scope / Вне публичной области | Support tickets, CMDB, logistics, SLA and private topology remain private. / Тикеты, CMDB, логистика, SLA и приватная топология остаются закрытыми. |

## Website / Сайт

The managed public project site is being prepared at `https://boxcore.claryel.space` using the shared CLARYEL twenty-language and immersive web runtime.

Управляемый публичный сайт проекта готовится по адресу `https://boxcore.claryel.space` на общем двадцатиязычном иммерсивном web-runtime CLARYEL.

## NGI Fediversity proposal / Заявка NGI Fediversity

Requested support: **EUR 50,000**. No advance payment is requested. The proposal funds the open core, Voice-to-GitOps, NixOS packaging, hardware profiles, Home Assistant integration, rollback, recovery, tests and public documentation. The commercial CLARYEL Box platform, customer equipment, commercial SLA operations and adjacent CLARYEL products are financed separately.

Запрашиваемая поддержка: **50 000 евро**. Аванс не запрашивается. Заявка финансирует открытое ядро, Voice-to-GitOps, упаковку NixOS, аппаратные профили, интеграцию Home Assistant, откат, восстановление, тесты и публичную документацию. Коммерческая платформа CLARYEL Box, оборудование клиентов, коммерческие SLA-процессы и смежные продукты CLARYEL финансируются отдельно.

## Commercial sustainability / Коммерческая устойчивость

The open stack will remain independently usable. CLARYEL plans to earn from qualified hardware-software appliances, installation, migration, managed stable updates, monitoring, recovery, equipment replacement, integrations and enterprise-grade support for small organisations and households.

Открытый стек останется пригодным для самостоятельного использования. CLARYEL планирует получать доход от квалифицированных аппаратно-программных комплексов, установки, миграции, управляемых стабильных обновлений, мониторинга, восстановления, замены оборудования, интеграций и технической поддержки enterprise-уровня для небольших организаций и домашних хозяйств.

## Repository navigation / Навигация по репозиторию

The complete governance, architecture, threat model, public-export policy, grant scope, budget, milestones, hardware compatibility matrix and implementation status will be added in the first public baseline pull request.

Полное управление, архитектура, модель угроз, политика публичного экспорта, границы заявки, бюджет, milestones, матрица аппаратной совместимости и статус реализации будут добавлены первым Pull Request публичной основы.
