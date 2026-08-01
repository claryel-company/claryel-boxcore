# CLARYEL Box Core agent rules / Правила агентов CLARYEL Box Core

Before any analysis or change, read `README.md`, `REPOSITORY.yaml`, `ARCHITECTURE.md`, `OPEN_SOURCE_SCOPE.md`, `PUBLICATION_STATUS.md`, `SECURITY.md` and `NEXT_STEPS.md`.

Перед любым анализом или изменением прочитайте `README.md`, `REPOSITORY.yaml`, `ARCHITECTURE.md`, `OPEN_SOURCE_SCOPE.md`, `PUBLICATION_STATUS.md`, `SECURITY.md` и `NEXT_STEPS.md`.

## Mandatory rules / Обязательные правила

1. Treat this repository as public at all times. / Всегда считать этот репозиторий публичным.
2. Never copy private Git history. Export reviewed files into a clean public history. / Никогда не копировать приватную Git-историю. Экспортировать проверенные файлы в чистую публичную историю.
3. Never publish credentials, personal data, customer data, private topology, serial numbers, private repository URLs, support tickets or unpatched security findings. / Никогда не публиковать учётные данные, персональные и клиентские данные, приватную топологию, серийные номера, ссылки на приватные репозитории, тикеты или неисправленные уязвимости.
4. Every exported component must record provenance, source commit, licence review and sanitisation evidence without exposing the private source location to unauthorised readers. / Каждый экспортируемый компонент должен фиксировать происхождение, исходный commit, проверку лицензии и evidence очистки без раскрытия закрытого источника неавторизованным лицам.
5. Distinguish `implemented`, `experimental`, `planned`, `private-testing`, `withheld-security` and `outside-scope`. / Разделять статусы `implemented`, `experimental`, `planned`, `private-testing`, `withheld-security` и `outside-scope`.
6. Do not present the requested EUR 50,000 as awarded funding. / Не представлять запрошенные 50 000 евро как уже присуждённое финансирование.
7. Configuration must not contain secrets or customer content. / Конфигурация не должна содержать секреты или клиентский контент.
8. Voice requests may propose changes but may not bypass policy, review, approval or rollback controls. / Голосовые запросы могут предлагать изменения, но не обходят политики, проверку, подтверждение и откат.
9. Hardware-management adapters must be capability-gated and disabled by default. / Адаптеры аппаратного управления должны включаться только при подтверждённой поддержке и быть выключены по умолчанию.
10. Every material change uses a focused branch, validation and Pull Request. / Каждое существенное изменение проходит через отдельную ветку, проверки и Pull Request.
11. Code and configuration comments are bilingual: English first, Russian immediately after. / Комментарии в коде и конфигурации двуязычные: сначала английский, сразу затем русский.
12. Update `NEXT_STEPS.md` and `PUBLICATION_STATUS.md` with every material release. / При каждом существенном выпуске обновлять `NEXT_STEPS.md` и `PUBLICATION_STATUS.md`.

## Repository boundary / Граница репозитория

This repository owns the public open core, public schemas, public hardware profiles, generic adapters, documentation, grant scope and public status. Commercial support operations, customer configurations, CMDB, logistics, SLA, private topology and customer data remain in private CLARYEL repositories.

Репозиторий владеет публичным открытым ядром, схемами, аппаратными профилями, универсальными адаптерами, документацией, границами заявки и публичным статусом. Коммерческая поддержка, клиентские конфигурации, CMDB, логистика, SLA, приватная топология и клиентские данные остаются в приватных репозиториях CLARYEL.
