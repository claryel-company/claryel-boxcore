# Public export provenance / Происхождение публичного экспорта

This register records reviewed private-to-public exports without copying private Git history.

Этот реестр фиксирует проверенные экспорты из приватной области в публичную без копирования приватной Git-истории.

## Export 2026-08-01-001 — node capability service

| Field / Поле | Value / Значение |
|---|---|
| Source owner / Владелец источника | `claryel-company/claryel-node-agent` |
| Reviewed source commit / Проверенный исходный commit | `bfd46ea40e6aebe48931c160dfb9361d2450cadd` |
| Reviewed files / Проверенные файлы | `cmd/claryel-node-agent/main.go`, `internal/discovery/discovery.go`, `internal/discovery/discovery_test.go` |
| Public destination / Публичное назначение | `cmd/boxcore-node/main.go`, `internal/discovery/discovery.go`, `internal/discovery/discovery_test.go` |
| Export type / Тип экспорта | Clean re-engineering, not history copy / Чистая переработка, не копирование истории |
| Security changes / Изменения безопасности | Raw hostname removed from public capability output; loopback-only default retained; no privileged mutation. / Raw hostname удалён из публичного вывода возможностей; сохранён loopback по умолчанию; привилегированные изменения отсутствуют. |
| Licence decision / Решение по лицензии | Public re-engineered code released under Apache-2.0. / Публично переработанный код выпущен под Apache-2.0. |
| Private material excluded / Исключённый приватный материал | Internal service names, private topology, fleet identifiers, credentials, telemetry and future private worker adapters. / Внутренние имена сервисов, приватная topology, идентификаторы парка, credentials, telemetry и будущие приватные worker adapters. |

## Future records / Будущие записи

Every later export must add a separate record containing source owner, exact private commit, reviewed files, public destination, sanitisation, licence decision, excluded material and public validation evidence.

Каждый последующий экспорт должен добавлять отдельную запись с владельцем источника, точным приватным commit, проверенными файлами, публичным назначением, очисткой, решением по лицензии, исключёнными материалами и публичным evidence проверки.
