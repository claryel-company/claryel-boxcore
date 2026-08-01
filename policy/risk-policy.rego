package claryel.boxcore.risk

import rego.v1

destructive_actions := {
  "repartition-disk",
  "delete-backup",
  "rotate-root-key",
  "wipe-data",
}

control_plane_actions := {
  "run-shell",
  "modify-policy",
  "disable-approval",
  "disable-audit",
  "disable-rollback",
}

high_risk_actions := {
  "expose-public-service",
  "enable-intel-amt",
  "enable-redfish",
  "enable-ipmi",
}

medium_risk_actions := {
  "install-service",
  "remove-service",
  "change-memory-limit",
  "change-update-channel",
}

low_risk_actions := {
  "enable-metrics",
  "change-dashboard-layout",
  "change-log-retention",
}

known_actions := destructive_actions | control_plane_actions | high_risk_actions | medium_risk_actions | low_risk_actions

deny contains reason if {
  some change in input.changes
  object.get(change, "containsSecretValue", false) == true
  reason := sprintf("secret values are forbidden in Git-managed configuration at %s", [change.path])
}

deny contains reason if {
  some change in input.changes
  object.get(change, "containsCustomerData", false) == true
  reason := sprintf("customer data is forbidden in Git-managed configuration at %s", [change.path])
}

deny contains reason if {
  some change in input.changes
  change.action in destructive_actions
  reason := sprintf("%s requires a separate exceptional workflow and cannot be approved by ordinary Voice-to-GitOps", [change.action])
}

deny contains reason if {
  some change in input.changes
  change.action in control_plane_actions
  reason := sprintf("%s may not be proposed through the ordinary change-plan contract", [change.action])
}

deny contains reason if {
  some change in input.changes
  capability := object.get(change, "requiredCapability", null)
  capability != null
  not capability in input.system.declaredCapabilities
  reason := sprintf("required capability %s is not declared for %s", [capability, input.system.systemId])
}

deny contains reason if {
  object.get(input.approval, "humanApproved", false) == true
  object.get(input.approval, "approvedBy", null) == null
  reason := "human approval is missing an approver identity"
}

deny contains reason if {
  object.get(input.approval, "humanApproved", false) == true
  object.get(input.approval, "approvedAt", null) == null
  reason := "human approval is missing an approval time"
}

has_high_risk if {
  some change in input.changes
  change.action in high_risk_actions
}

has_medium_risk if {
  some change in input.changes
  change.action in medium_risk_actions
}

has_low_risk if {
  some change in input.changes
  change.action in low_risk_actions
}

has_unknown_risk if {
  some change in input.changes
  not change.action in known_actions
}

risk_level := "forbidden" if count(deny) > 0

risk_level := "high" if {
  count(deny) == 0
  has_high_risk
}

risk_level := "medium" if {
  count(deny) == 0
  not has_high_risk
  has_medium_risk
}

risk_level := "unknown" if {
  count(deny) == 0
  not has_high_risk
  not has_medium_risk
  has_unknown_risk
}

risk_level := "low" if {
  count(deny) == 0
  not has_high_risk
  not has_medium_risk
  not has_unknown_risk
  has_low_risk
}

risk_level := "unknown" if {
  count(deny) == 0
  count(input.changes) == 0
}

default requires_human_approval := false

requires_human_approval if risk_level in {"high", "medium", "unknown"}

requires_human_approval if input.system.approvalMode in {"always-human", "offline-manual"}

default automatic_approval_allowed := false

automatic_approval_allowed if {
  risk_level == "low"
  input.system.approvalMode == "automatic-low-risk"
}

human_approval_present if {
  input.approval.humanApproved == true
  input.approval.approvedBy != null
  input.approval.approvedAt != null
}

default allow := false

allow if {
  count(deny) == 0
  automatic_approval_allowed
}

allow if {
  count(deny) == 0
  human_approval_present
}
