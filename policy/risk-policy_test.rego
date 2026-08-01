package claryel.boxcore.risk

import rego.v1

test_low_risk_automatic_approval if {
  risk_level == "low" with input as low_risk_input
  automatic_approval_allowed with input as low_risk_input
  allow with input as low_risk_input
}

test_high_risk_requires_human_approval if {
  risk_level == "high" with input as high_risk_unapproved_input
  requires_human_approval with input as high_risk_unapproved_input
  not allow with input as high_risk_unapproved_input
}

test_high_risk_human_approval_allows_plan if {
  risk_level == "high" with input as high_risk_approved_input
  allow with input as high_risk_approved_input
}

test_destructive_action_is_forbidden if {
  risk_level == "forbidden" with input as destructive_input
  not allow with input as destructive_input
}

test_missing_capability_is_forbidden if {
  risk_level == "forbidden" with input as missing_capability_input
  not allow with input as missing_capability_input
}

test_control_plane_self_modification_is_forbidden if {
  risk_level == "forbidden" with input as policy_modification_input
  not allow with input as policy_modification_input
}

test_unknown_action_fails_closed if {
  risk_level == "unknown" with input as unknown_action_input
  requires_human_approval with input as unknown_action_input
  not allow with input as unknown_action_input
}

low_risk_input := {
  "request": {"channel": "voice"},
  "system": {
    "systemId": "home-main",
    "approvalMode": "automatic-low-risk",
    "declaredCapabilities": ["system.metrics.local"],
  },
  "changes": [{
    "path": "/services/metrics/enabled",
    "action": "enable-metrics",
    "containsSecretValue": false,
    "containsCustomerData": false,
    "requiredCapability": "system.metrics.local",
  }],
  "approval": {
    "humanApproved": false,
    "approvedBy": null,
    "approvedAt": null,
  },
}

high_risk_unapproved_input := {
  "request": {"channel": "text"},
  "system": {
    "systemId": "office-edge",
    "approvalMode": "always-human",
    "declaredCapabilities": ["hardware.redfish"],
  },
  "changes": [{
    "path": "/profile/capabilities/outOfBand",
    "action": "enable-redfish",
    "containsSecretValue": false,
    "containsCustomerData": false,
    "requiredCapability": "hardware.redfish",
  }],
  "approval": {
    "humanApproved": false,
    "approvedBy": null,
    "approvedAt": null,
  },
}

high_risk_approved_input := object.union(high_risk_unapproved_input, {
  "approval": {
    "humanApproved": true,
    "approvedBy": "synthetic-maintainer",
    "approvedAt": "2026-08-01T10:06:00Z",
  },
})

destructive_input := {
  "request": {"channel": "voice"},
  "system": {
    "systemId": "home-main",
    "approvalMode": "always-human",
    "declaredCapabilities": [],
  },
  "changes": [{
    "path": "/profile/storage",
    "action": "repartition-disk",
    "containsSecretValue": false,
    "containsCustomerData": false,
    "requiredCapability": null,
  }],
  "approval": {
    "humanApproved": true,
    "approvedBy": "synthetic-maintainer",
    "approvedAt": "2026-08-01T10:06:00Z",
  },
}

missing_capability_input := {
  "request": {"channel": "text"},
  "system": {
    "systemId": "office-edge",
    "approvalMode": "always-human",
    "declaredCapabilities": [],
  },
  "changes": [{
    "path": "/profile/capabilities/outOfBand",
    "action": "enable-redfish",
    "containsSecretValue": false,
    "containsCustomerData": false,
    "requiredCapability": "hardware.redfish",
  }],
  "approval": {
    "humanApproved": true,
    "approvedBy": "synthetic-maintainer",
    "approvedAt": "2026-08-01T10:06:00Z",
  },
}

policy_modification_input := {
  "request": {"channel": "text"},
  "system": {
    "systemId": "home-main",
    "approvalMode": "always-human",
    "declaredCapabilities": [],
  },
  "changes": [{
    "path": "/deployment/approvalMode",
    "action": "disable-approval",
    "containsSecretValue": false,
    "containsCustomerData": false,
    "requiredCapability": null,
  }],
  "approval": {
    "humanApproved": true,
    "approvedBy": "synthetic-maintainer",
    "approvedAt": "2026-08-01T10:06:00Z",
  },
}

unknown_action_input := {
  "request": {"channel": "api"},
  "system": {
    "systemId": "home-main",
    "approvalMode": "automatic-low-risk",
    "declaredCapabilities": [],
  },
  "changes": [{
    "path": "/metadata/purpose",
    "action": "future-undefined-action",
    "containsSecretValue": false,
    "containsCustomerData": false,
    "requiredCapability": null,
  }],
  "approval": {
    "humanApproved": false,
    "approvedBy": null,
    "approvedAt": null,
  },
}
