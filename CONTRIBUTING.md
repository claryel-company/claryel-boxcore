# Contributing to CLARYEL Box Core / Участие в CLARYEL Box Core

Thank you for contributing to the public open core. This repository is intentionally strict because it combines infrastructure, local AI, hardware control and private-data boundaries.

Спасибо за участие в публичном открытом ядре. Репозиторий намеренно использует строгие правила, поскольку объединяет инфраструктуру, локальный ИИ, аппаратное управление и границы приватных данных.

## Before opening a change / До открытия изменения

1. Read `AGENTS.md`, `ARCHITECTURE.md`, `THREAT_MODEL.md`, `OPEN_SOURCE_SCOPE.md`, `SECURITY.md` and `PUBLICATION_STATUS.md`. / Прочитайте `AGENTS.md`, `ARCHITECTURE.md`, `THREAT_MODEL.md`, `OPEN_SOURCE_SCOPE.md`, `SECURITY.md` и `PUBLICATION_STATUS.md`.
2. Open or reference an issue describing the user outcome, trust boundary and acceptance evidence. / Откройте или укажите issue с пользовательским результатом, границей доверия и evidence приёмки.
3. Keep one functional change per Pull Request. / Сохраняйте одно функциональное изменение на Pull Request.
4. Never paste customer data, real credentials, private topology, production logs or unresolved vulnerability details. / Никогда не добавляйте клиентские данные, реальные credentials, приватную топологию, production logs или сведения о неисправленной уязвимости.

## Required change content / Обязательное содержимое изменения

- implementation status: `experimental`, `validated` or `production-ready`; / статус реализации: `experimental`, `validated` или `production-ready`;
- tests or reproducible validation; / тесты или воспроизводимая проверка;
- security and rollback impact; / влияние на безопасность и rollback;
- documentation and examples; / документация и примеры;
- licence and third-party provenance; / лицензия и происхождение материалов третьих лиц;
- bilingual code and configuration comments: English first, Russian immediately after. / двуязычные комментарии к коду и конфигурации: сначала английский, сразу затем русский.

## Private-to-public exports / Экспорт из приватных репозиториев

Only CLARYEL maintainers may approve an export from a private repository. The export must have an entry in `docs/PROVENANCE.md` and must pass secret, PII, topology, licence and dependency review. Private Git history is never copied.

Только сопровождающие CLARYEL могут подтвердить экспорт из приватного репозитория. Экспорт должен иметь запись в `docs/PROVENANCE.md` и пройти проверку секретов, PII, топологии, лицензий и зависимостей. Приватная Git-история никогда не копируется.

## Validation / Проверка

Run:

Выполните:

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

## Review priorities / Приоритеты review

1. No private or customer information. / Отсутствие приватной или клиентской информации.
2. No unreviewed voice-to-shell or model-to-actuator path. / Отсутствие непроверенного пути voice-to-shell или model-to-actuator.
3. Safe defaults and explicit capability gates. / Безопасные значения по умолчанию и явные capability gates.
4. Reproducibility and rollback. / Воспроизводимость и rollback.
5. Independent usefulness without a CLARYEL subscription. / Самостоятельная полезность без подписки CLARYEL.
