# Live managed-site evidence / Evidence live managed-сайта

**Audit date / Дата аудита:** 2026-08-01  
**Managed site / Управляемый сайт:** `https://boxcore.claryel.space`  
**Runtime owner / Владелец runtime:** `claryel-company/claryel-space`  
**Public content and open-core owner / Владелец публичного контента и открытого ядра:** `claryel-company/claryel-boxcore`

## Verified live outcomes / Проверенные live-результаты

The production endpoint was checked independently after the managed-site merge and publication workflow.

Production endpoint был независимо проверен после merge управляемого сайта и publication workflow.

- the canonical root returns the native CLARYEL Box Core document; / канонический корень возвращает нативный документ CLARYEL Box Core;
- the live document contains the project title, public-beta statement and `Speak. Review. Deploy. Roll back.` promise; / live-документ содержит название проекта, public-beta statement и обещание `Speak. Review. Deploy. Roll back.`;
- all twenty canonical locale routes return the Box Core document; / все двадцать канонических языковых маршрутов возвращают документ Box Core;
- the document exposes canonical URL, reciprocal `hreflang` records and `x-default`; / документ предоставляет canonical URL, взаимные записи `hreflang` и `x-default`;
- Arabic is served through its canonical locale route and managed RTL metadata; / арабская версия обслуживается через канонический языковой маршрут и managed RTL metadata;
- production security headers include Content Security Policy, Strict Transport Security and `X-Content-Type-Options`; / production security headers включают Content Security Policy, Strict Transport Security и `X-Content-Type-Options`;
- CLARYEL Universe API includes the `boxcore` node, public repository and canonical managed-site URL. / API CLARYEL Universe включает узел `boxcore`, публичный репозиторий и канонический URL управляемого сайта.

## Audited locale routes / Проверенные языковые маршруты

`/`, `/it/`, `/de/`, `/fr/`, `/es/`, `/nl/`, `/pt/`, `/pl/`, `/ro/`, `/cs/`, `/sv/`, `/el/`, `/da/`, `/fi/`, `/zh-cn/`, `/hi/`, `/ar/`, `/id/`, `/uk/`, `/ru/`.

## Status meaning / Значение статуса

This evidence proves that the managed presentation is live. It does not change the implementation status of planned Box Core runtime capabilities. Voice-to-GitOps runtime, generic Home Assistant adapter and validated hardware profiles remain governed by `PUBLICATION_STATUS.md` and must not be inferred from website availability.

Это evidence доказывает, что managed-презентация опубликована. Оно не изменяет статус реализации планируемых runtime-функций Box Core. Runtime Voice-to-GitOps, универсальный адаптер Home Assistant и проверенные аппаратные профили остаются под управлением `PUBLICATION_STATUS.md` и не могут считаться реализованными только из-за доступности сайта.

## Reproduction / Воспроизведение проверки

```bash
# English: Verify the canonical live page.
# Русский: Проверить каноническую live-страницу.
curl --fail --location --silent --show-error https://boxcore.claryel.space/ \
  | grep 'CLARYEL Box Core'

# English: Verify the public Universe registry contains the Box Core node.
# Русский: Проверить наличие узла Box Core в публичном реестре Universe.
curl --fail --location --silent --show-error https://claryel.space/api/universe/sites.json \
  | grep 'claryel-company/claryel-boxcore'
```

## Remaining validation / Оставшаяся проверка

- ongoing visual review across Android-class Chromium, iPhone-class WebKit, tablets and desktop browsers; / продолжающийся визуальный review в Android-class Chromium, iPhone-class WebKit, планшетах и desktop-браузерах;
- accessibility review of every translated long-form document; / accessibility review каждого переведённого длинного документа;
- public release evidence for each runtime milestone. / публичные release evidence для каждого runtime milestone.
