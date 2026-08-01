# Threat model / Модель угроз

## Assets / Активы

- customer data and local AI knowledge; / клиентские данные и локальные знания ИИ;
- credentials, keys and recovery material; / учётные данные, ключи и материалы восстановления;
- desired-state integrity and Git history; / целостность desired state и Git-истории;
- deployment authority; / полномочия deployment;
- hardware-control interfaces; / интерфейсы аппаратного управления;
- backups and recovery points; / резервные копии и точки восстановления;
- public release and supply-chain integrity. / целостность публичного релиза и цепочки поставок.

## Trust assumptions / Предпосылки доверия

- The customer-controlled node is the only place that may hold decrypted customer content. / Узел под контролем клиента является единственным местом, где может находиться расшифрованный клиентский контент.
- Git-compatible repositories hold technical desired state only. / Git-совместимые репозитории хранят только техническое desired state.
- Human approval is required for high-risk changes. / Для изменений высокого риска требуется человеческое подтверждение.
- External services may fail or be compromised and therefore are replaceable adapters. / Внешние сервисы могут отказать или быть скомпрометированы и поэтому являются заменяемыми адаптерами.

## Threats and controls / Угрозы и меры

| Threat / Угроза | Primary controls / Основные меры |
|---|---|
| Misheard or ambiguous voice command / Неверно распознанная или неоднозначная голосовая команда | Explainable plan, text confirmation, risk classification and approval. / Понятный план, текстовое подтверждение, классификация риска и approval. |
| Prompt injection through local content / Prompt injection через локальный контент | Separate administrative intent channel, constrained schema, no direct shell execution. / Отдельный административный канал intent, ограниченная схема, отсутствие прямого shell execution. |
| Malicious Git commit / Вредоносный Git commit | Signed or verified revisions, branch protection, policy checks, tests and pinned dependencies. / Подписанные или проверенные revisions, защита веток, политики, тесты и закреплённые зависимости. |
| Secret committed to Git / Секрет добавлен в Git | References-only schema, secret scanning, local secret store and rejection policy. / Схема только со ссылками, secret scanning, локальный secret store и политика отклонения. |
| Customer data copied into configuration / Клиентские данные скопированы в конфигурацию | Schema restrictions, PII checks and separate data mounts. / Ограничения схемы, PII-проверки и отдельные data mounts. |
| Unsafe update / Небезопасное обновление | Build before activation, dry run, health checks and automatic rollback. / Сборка до активации, dry run, health checks и автоматический откат. |
| Rollback corrupts mutable state / Откат повреждает изменяемое состояние | Separate system generation from service data, migration gates and backups. / Разделение системной генерации и данных сервисов, migration gates и backups. |
| Compromised remote-access provider / Компрометация провайдера удалённого доступа | Optional adapter, outbound-only connection, local authentication and rapid revocation. / Опциональный адаптер, исходящее соединение, локальная аутентификация и быстрая отмена. |
| Abuse of Intel AMT, Redfish or IPMI / Злоупотребление Intel AMT, Redfish или IPMI | Disabled by default, capability gate, isolated management network, least privilege and audited actions. / Выключено по умолчанию, capability gate, изолированная management-сеть, минимальные полномочия и аудит действий. |
| Supply-chain compromise / Компрометация цепочки поставок | Pinned inputs, SBOM, dependency review, reproducible builds and signed release metadata. / Закреплённые inputs, SBOM, проверка зависимостей, воспроизводимые сборки и подписанная metadata релизов. |
| Public export leaks private information / Публичный экспорт раскрывает приватную информацию | Clean export, secret/PII/topology/licence review and human approval. / Чистый экспорт, проверка секретов, PII, топологии, лицензий и человеческое подтверждение. |

## Forbidden voice operations / Запрещённые голосовые операции

Voice alone may not authorise deletion of customer data, destruction of backups, key rotation, disk repartitioning, disabling security controls, exposing a service publicly or enabling out-of-band hardware control.

Только голос не может разрешить удаление клиентских данных, уничтожение backups, ротацию ключей, переразметку дисков, отключение security controls, публичное открытие сервиса или включение out-of-band аппаратного управления.

## Future robotics boundary / Граница будущей робототехники

Domestic and industrial robot integration is research outside the current grant scope. Any future adapter must keep sensitive sensor streams local, expose explicit capabilities, require consent and prevent direct unreviewed model-to-actuator control.

Интеграция домашних и промышленных роботов является исследованием вне текущей заявки. Любой будущий адаптер должен сохранять чувствительные sensor streams локально, явно объявлять возможности, требовать согласие и исключать прямое непроверенное управление исполнительными устройствами со стороны модели.
