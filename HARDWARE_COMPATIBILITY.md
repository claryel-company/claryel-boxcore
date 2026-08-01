# Hardware compatibility / Аппаратная совместимость

## Status model / Модель статусов

- `planned`: no public implementation or test evidence yet. / публичной реализации или evidence тестирования ещё нет.
- `experimental`: public implementation exists but support is limited. / публичная реализация существует, но поддержка ограничена.
- `validated`: tested by CLARYEL on declared hardware and release. / протестировано CLARYEL на объявленном оборудовании и релизе.
- `community-validated`: independently reproduced by a community contributor. / независимо воспроизведено участником сообщества.
- `commercially-qualified`: supported by the commercial CLARYEL Box service. / поддерживается коммерческим сервисом CLARYEL Box.

## Initial matrix / Первоначальная матрица

| Profile / Профиль | Architecture / Архитектура | Public status / Публичный статус | Intended use / Назначение |
|---|---|---|---|
| Generic CPU-only server | x86_64 | planned | Local services and small models without GPU acceleration. / Локальные сервисы и небольшие модели без GPU-ускорения. |
| Intel integrated GPU | x86_64 | planned | Low-power local inference and media processing. / Энергоэффективный локальный inference и обработка мультимедиа. |
| AMD integrated GPU | x86_64 | planned | Alternative integrated acceleration profile. / Альтернативный профиль интегрированного ускорения. |
| NVIDIA discrete GPU | x86_64 | planned | Larger local models and accelerated inference. / Более крупные локальные модели и ускоренный inference. |
| Generic ARM node | aarch64 | planned | Low-power edge, Home Assistant and control-plane roles. / Энергоэффективные edge, Home Assistant и control-plane роли. |
| Virtual machine | x86_64/aarch64 | planned | Evaluation, development and migration. / Проверка, разработка и миграция. |
| Compatible NAS | vendor-dependent | planned | Storage, backup or virtualised deployment. / Хранилище, backup или виртуализированное развёртывание. |
| Intel vPro/AMT | x86_64 compatible devices | planned | Optional out-of-band inventory, power, diagnosis and recovery. / Опциональная out-of-band инвентаризация, питание, диагностика и восстановление. |
| Redfish | compatible servers | planned | Vendor-neutral server inventory and recovery control. / Vendor-neutral инвентаризация и управление восстановлением серверов. |
| IPMI | compatible servers | planned | Legacy out-of-band management behind strict local controls. / Legacy out-of-band управление под строгим локальным контролем. |

## Required profile fields / Обязательные поля профиля

Each machine profile declares:

Каждый профиль машины объявляет:

- profile identifier and schema version; / идентификатор профиля и версию схемы;
- CPU architecture and required instruction sets; / архитектуру CPU и необходимые наборы инструкций;
- minimum and recommended RAM; / минимальную и рекомендуемую RAM;
- storage layout and mutable-data boundaries; / схему хранилища и границы изменяемых данных;
- GPU or accelerator type and driver requirements; / тип GPU или ускорителя и требования к драйверам;
- TPM, secure boot and encryption capabilities; / возможности TPM, secure boot и шифрования;
- network and management interfaces; / сетевые и management-интерфейсы;
- Home Assistant sensor and actuator capabilities; / возможности датчиков и исполнительных устройств Home Assistant;
- out-of-band management support; / поддержку out-of-band управления;
- known limitations and destructive-operation gates; / известные ограничения и gates разрушающих операций;
- exact tested commit, release, date and evidence. / точный протестированный commit, релиз, дату и evidence.

## Intel vPro/AMT policy / Политика Intel vPro/AMT

Intel vPro/AMT is an optional capability for compatible equipment, not a dependency of Box Core. Public profiles will describe discovery, inventory, power-state and recovery capabilities without including customer credentials, management-network topology or vendor secrets. Remote actions remain disabled unless local policy explicitly enables them.

Intel vPro/AMT является опциональной возможностью совместимого оборудования, а не зависимостью Box Core. Публичные профили будут описывать обнаружение, инвентаризацию, управление питанием и восстановление без клиентских учётных данных, топологии management-сети или секретов поставщика. Удалённые действия остаются выключенными, пока локальная политика явно не разрешит их.

## Data safety / Безопасность данных

Hardware profile selection never authorises disk repartitioning, data deletion, key rotation or backup destruction. Those operations require separate explicit workflows and cannot be approved by voice alone.

Выбор аппаратного профиля никогда не разрешает переразметку дисков, удаление данных, ротацию ключей или уничтожение backups. Эти операции требуют отдельных явных workflows и не могут быть подтверждены только голосом.
