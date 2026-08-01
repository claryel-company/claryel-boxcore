package claryel.boxcore.risk

# English: Deny changes that attempt to place secret values or customer content in configuration.
# Русский: Запрещать изменения, которые пытаются поместить значения секретов или клиентский контент в конфигурацию.
deny contains reason if {
  input.change.containsSecretValue == true
  reason := "secret values are forbidden in Git-managed configuration"
}

deny contains reason if {
  input.change.containsCustomerData == true
  reason := "customer data is forbidden in Git-managed configuration"
}

# English: Voice alone may never authorise destructive storage, backup or key-management actions.
# Русский: Только голос никогда не может разрешить разрушающие операции с хранилищем, backups или ключами.
deny contains reason if {
  input.request.channel == "voice"
  input.change.action in {"repartition-disk", "delete-backup", "rotate-root-key", "wipe-data"}
  reason := "destructive operations require a separate explicit workflow"
}

# English: Public exposure and hardware out-of-band control are always high risk.
# Русский: Публичное открытие сервиса и out-of-band аппаратное управление всегда относятся к высокому риску.
high_risk if input.change.action in {"expose-public-service", "enable-intel-amt", "enable-redfish", "enable-ipmi"}

# English: Medium-risk actions change installed services or resource allocation.
# Русский: Действия среднего риска изменяют установленные сервисы или распределение ресурсов.
medium_risk if input.change.action in {"install-service", "remove-service", "change-memory-limit", "change-update-channel"}

# English: Low-risk actions affect observability or non-destructive presentation settings.
# Русский: Действия низкого риска затрагивают наблюдаемость или неразрушающие настройки представления.
low_risk if input.change.action in {"enable-metrics", "change-dashboard-layout", "change-log-retention"}

risk_level := "forbidden" if count(deny) > 0
risk_level := "high" if {
  count(deny) == 0
  high_risk
}
risk_level := "medium" if {
  count(deny) == 0
  not high_risk
  medium_risk
}
risk_level := "low" if {
  count(deny) == 0
  not high_risk
  not medium_risk
  low_risk
}
risk_level := "unknown" if {
  count(deny) == 0
  not high_risk
  not medium_risk
  not low_risk
}

# English: High, medium and unknown actions require explicit human approval.
# Русский: Действия высокого, среднего и неизвестного риска требуют явного человеческого подтверждения.
requires_human_approval if risk_level in {"high", "medium", "unknown"}

# English: Only known low-risk actions may use automatic approval when local policy allows it.
# Русский: Только известные действия низкого риска могут подтверждаться автоматически, если это разрешает локальная политика.
automatic_approval_allowed if {
  risk_level == "low"
  input.system.deployment.approvalMode == "automatic-low-risk"
}
