# CLARYEL Box Core implementation context / Контекст реализации CLARYEL Box Core

This file is a concise machine-readable handoff for coding agents. The authoritative rules are in `AGENTS.md`, `ARCHITECTURE.md`, `OPEN_SOURCE_SCOPE.md`, `SECURITY.md` and `NEXT_STEPS.md`.

Этот файл является краткой передачей контекста для программных агентов. Авторитетные правила находятся в `AGENTS.md`, `ARCHITECTURE.md`, `OPEN_SOURCE_SCOPE.md`, `SECURITY.md` и `NEXT_STEPS.md`.

## Product sentence / Описание продукта

Voice or text intent becomes an explainable Git change, passes policy and approval, builds a pinned NixOS generation, deploys atomically, checks hardware and services, and rolls back on failure.

Голосовое или текстовое намерение превращается в понятное Git-изменение, проходит политики и подтверждение, собирает закреплённую генерацию NixOS, применяется атомарно, проверяет оборудование и сервисы и откатывается при ошибке.

## Hard constraints / Жёсткие ограничения

- Public repository: never introduce secrets or private history. / Публичный репозиторий: никогда не добавлять секреты или приватную историю.
- Customer data and secrets never enter Git. / Клиентские данные и секреты никогда не попадают в Git.
- High-risk changes require explicit approval. / Изменения высокого риска требуют явного подтверждения.
- Hardware actions are capability-gated and disabled by default. / Аппаратные действия включаются только при подтверждённой поддержке и по умолчанию выключены.
- GitHub and Cloudflare are optional adapters, not architectural requirements. / GitHub и Cloudflare являются опциональными адаптерами, а не архитектурными требованиями.
- Home Assistant is the initial user and physical-world interface, not the owner of configuration truth. / Home Assistant является первоначальным пользовательским интерфейсом и интерфейсом физического мира, но не владельцем истины конфигурации.
- Every claim must expose an implementation status. / Каждое утверждение должно иметь статус реализации.
