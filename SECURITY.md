# Security policy / Политика безопасности

## Reporting / Сообщение об уязвимости

Do not open a public issue for a vulnerability that may expose credentials, customer data, private topology, destructive hardware operations or an exploitable deployment path. Use the private security-reporting channel configured for the repository. Until that channel is enabled, contact the CLARYEL organisation administrators without publishing technical details.

Не открывайте публичный issue для уязвимости, которая может раскрыть учётные данные, клиентские данные, приватную топологию, разрушающие аппаратные операции или эксплуатируемый deployment-путь. Используйте приватный security-канал репозитория. До его включения свяжитесь с администраторами организации CLARYEL без публикации технических деталей.

## Supported status / Поддерживаемый статус

The repository is an early public baseline and is not production-ready. Files and releases must state whether they are `experimental`, `validated` or `production-ready`.

Репозиторий является ранней публичной основой и не готов к production. Файлы и релизы обязаны указывать статус `experimental`, `validated` или `production-ready`.

## Security invariants / Инварианты безопасности

- Git contains no secret values or customer content. / Git не содержит значений секретов или клиентского контента.
- Voice input never bypasses review, policy or approval. / Голосовой ввод никогда не обходит проверку, политики или подтверждение.
- High-risk and destructive operations are denied by default. / Операции высокого риска и разрушающие операции по умолчанию запрещены.
- Hardware-management actions require declared capability and local authorisation. / Аппаратные действия требуют объявленной возможности и локального разрешения.
- Remote access is optional, outbound-first and separately authenticated. / Удалённый доступ является опциональным, исходящим и отдельно аутентифицируемым.
- Rollback of system configuration does not replace backup of mutable user data. / Откат системной конфигурации не заменяет резервирование изменяемых пользовательских данных.
- Public examples use synthetic identifiers and networks. / Публичные примеры используют синтетические идентификаторы и сети.

## Public-export checks / Проверки публичного экспорта

Every export from a private repository requires secret scanning, PII review, private-topology review, licence review, dependency review and human approval.

Каждый экспорт из приватного репозитория требует проверки секретов, PII, приватной топологии, лицензий, зависимостей и человеческого подтверждения.

## Disclosure lifecycle / Жизненный цикл раскрытия

1. Private receipt and acknowledgement. / Приватное получение и подтверждение.
2. Reproduction and severity classification. / Воспроизведение и классификация серьёзности.
3. Private remediation and tests. / Приватное исправление и тесты.
4. Coordinated release and secret rotation where applicable. / Согласованный выпуск и ротация секретов при необходимости.
5. Public advisory after users have a safe upgrade path. / Публичное уведомление после появления безопасного пути обновления.
