# Open-source scope and export policy / Область открытого кода и политика экспорта

## Public by default / Открыто по умолчанию

The following categories are intended for publication after review:

Следующие категории предназначены для публикации после проверки:

- Nix flakes and generic NixOS modules; / Nix flakes и универсальные модули NixOS;
- desired-state and hardware-profile schemas; / схемы desired state и аппаратных профилей;
- Voice-to-GitOps contracts and generic implementation; / контракты Voice-to-GitOps и универсальная реализация;
- policy rules and approval model; / правила политик и модель подтверждения;
- generic Home Assistant and MQTT adapters; / универсальные адаптеры Home Assistant и MQTT;
- capability-gated Intel vPro/AMT, Redfish and IPMI profiles; / профили Intel vPro/AMT, Redfish и IPMI с проверкой возможностей;
- bootstrap examples and synthetic fixtures; / bootstrap-примеры и синтетические fixtures;
- tests, CI, documentation, threat model and public evidence; / тесты, CI, документация, модель угроз и публичные evidence;
- grant scope, budget, milestones and status. / границы заявки, бюджет, milestones и статус.

## Private by necessity / Закрыто по необходимости

The following categories remain private:

Следующие категории остаются закрытыми:

- customer documents, databases, vector stores and voice recordings; / клиентские документы, базы данных, vector stores и голосовые записи;
- credentials, keys, recovery material and secret values; / учётные данные, ключи, материалы восстановления и значения секретов;
- customer-specific desired state and private repository metadata; / клиентское desired state и metadata приватных репозиториев;
- production topology, IP addressing, VPN configuration and account identifiers; / production-топология, IP-адресация, VPN-конфигурация и идентификаторы аккаунтов;
- support tickets, conversations, CMDB, warehouse and logistics data; / тикеты, переписка, CMDB, складские и логистические данные;
- commercial SLA workflows and equipment-replacement operations; / коммерческие SLA-процессы и операции замены оборудования;
- unresolved vulnerabilities and confidential audit findings; / неисправленные уязвимости и конфиденциальные результаты аудита;
- third-party material without compatible publication rights. / материалы третьих лиц без совместимых прав публикации.

## Clean-export rule / Правило чистого экспорта

Private Git history is never copied. A candidate file is exported into a clean public branch only after:

Приватная Git-история никогда не копируется. Файл-кандидат экспортируется в чистую публичную ветку только после:

1. functional-owner approval; / подтверждения владельца функции;
2. secret and credential scan; / проверки секретов и учётных данных;
3. personal-data and private-topology review; / проверки персональных данных и приватной топологии;
4. licence and third-party rights review; / проверки лицензий и прав третьих лиц;
5. dependency and SBOM review; / проверки зависимостей и SBOM;
6. removal of internal names and environment-specific paths; / удаления внутренних имён и environment-специфичных путей;
7. public tests and documentation; / публичных тестов и документации;
8. provenance record containing the private source commit without publishing inaccessible source content. / записи происхождения с исходным приватным commit без публикации закрытого содержимого.

## Publication status vocabulary / Словарь статусов публикации

- `implemented`: public code and tests exist. / публичный код и тесты существуют.
- `experimental`: public implementation exists but is not production-ready. / публичная реализация существует, но не готова к production.
- `planned`: public implementation does not yet exist. / публичная реализация ещё не существует.
- `private-testing`: implementation exists privately and is still being reviewed or tested. / реализация существует приватно и ещё проверяется или тестируется.
- `withheld-security`: publication is delayed for a concrete security reason. / публикация отложена по конкретной причине безопасности.
- `outside-scope`: the capability is commercial, customer-specific or owned elsewhere. / функция является коммерческой, клиентской или принадлежит другому компоненту.

## Licence model / Модель лицензирования

Public code is initially released under Apache-2.0. Public documentation is released under CC BY-SA 4.0 unless a file states another compatible licence. The licence model may be refined during grant negotiations without reducing the freedom of already published grant-funded results.

Публичный код первоначально выпускается под Apache-2.0. Публичная документация выпускается под CC BY-SA 4.0, если файл не указывает другую совместимую лицензию. Модель лицензирования может быть уточнена во время переговоров по гранту без ограничения свободы уже опубликованных результатов, профинансированных грантом.
