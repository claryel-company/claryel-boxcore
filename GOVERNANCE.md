# Project governance / Управление проектом

## Principles / Принципы

- Open by default, private by necessity. / Открыто по умолчанию, закрыто по необходимости.
- Public claims follow public evidence. / Публичные утверждения следуют за публичными evidence.
- Safety and user control precede automation convenience. / Безопасность и пользовательский контроль важнее удобства автоматизации.
- One capability has one authoritative owner. / У каждой функции один авторитетный владелец.
- External hosted services and hardware vendors are replaceable adapters. / Внешние hosted-сервисы и поставщики оборудования являются заменяемыми адаптерами.

## Roles / Роли

### Maintainers / Сопровождающие

Maintainers approve releases, public exports, security-sensitive changes, contract versions and status transitions.

Сопровождающие подтверждают релизы, публичные экспорты, security-sensitive изменения, версии контрактов и переходы статусов.

### Contributors / Участники

Contributors may propose code, documentation, tests, translations, hardware profiles and validation evidence through reviewed Pull Requests.

Участники могут предлагать код, документацию, тесты, переводы, аппаратные профили и validation evidence через проверяемые Pull Requests.

### Hardware validators / Валидаторы оборудования

A hardware validator reproduces a profile on declared equipment and publishes non-sensitive evidence. A validator never publishes serial numbers, management credentials, private network topology or customer identifiers.

Валидатор оборудования воспроизводит профиль на объявленном оборудовании и публикует нечувствительные evidence. Валидатор никогда не публикует серийные номера, management credentials, приватную сетевую топологию или клиентские идентификаторы.

## Decision process / Процесс принятия решений

- Small compatible changes use a Pull Request and maintainer review. / Небольшие совместимые изменения используют Pull Request и review сопровождающего.
- Public contract changes require versioning, migration notes and architecture review. / Изменения публичных контрактов требуют версионирования, migration notes и архитектурного review.
- Cross-repository ownership changes require a project-platform ADR. / Межрепозиторные изменения владения требуют общепроектного ADR.
- Security embargoes follow `SECURITY.md`. / Security embargo следует `SECURITY.md`.

## Status changes / Изменение статусов

A capability may move from `planned` to `experimental` only when public code and tests exist. It may move to `validated` only with reproducible evidence. `production-ready` requires a documented release, supported upgrade and rollback path, security review and declared hardware/software compatibility.

Функция может перейти из `planned` в `experimental` только при наличии публичного кода и тестов. Переход в `validated` требует воспроизводимых evidence. `production-ready` требует документированного релиза, поддерживаемого пути обновления и rollback, security review и объявленной аппаратно-программной совместимости.

## Grant transparency / Прозрачность гранта

Requested, negotiated, awarded, paid and spent amounts are distinct states. The repository and website must use the exact current state and must not present requested funding as awarded.

Запрошенная, согласованная, присуждённая, выплаченная и израсходованная суммы являются разными состояниями. Репозиторий и сайт обязаны использовать точный текущий статус и не представлять запрошенное финансирование как присуждённое.

## Commercial boundary / Коммерческая граница

Commercial CLARYEL services may provide qualified appliances, installation, migration, managed updates, monitoring, recovery, equipment replacement, integrations and support. They do not receive authority to restrict, revoke or make the open core dependent on a subscription.

Коммерческие сервисы CLARYEL могут предоставлять квалифицированные комплексы, установку, миграцию, управляемые обновления, мониторинг, recovery, замену оборудования, интеграции и поддержку. Они не получают полномочий ограничивать, отзывать или делать открытое ядро зависимым от подписки.
