{ config, lib, pkgs, ... }:

let
  cfg = config.services.claryelBoxCore;
  inherit (lib) mkEnableOption mkIf mkOption types;
  absoluteSafePath = types.strMatching "^/[A-Za-z0-9._@:+-]+(/[A-Za-z0-9._@:+-]+)*$";
in
{
  options.services.claryelBoxCore = {
    enable = mkEnableOption "CLARYEL Box Core public baseline";

    systemId = mkOption {
      type = types.strMatching "^[a-z0-9][a-z0-9-]{1,62}$";
      example = "home-main";
      description = "Technical identifier. Do not use a customer name or personal identifier.";
    };

    desiredStatePath = mkOption {
      type = absoluteSafePath;
      example = "/etc/claryel-boxcore/desired-state";
      description = "Absolute path to a local checkout containing technical desired state only.";
    };

    secretStorePath = mkOption {
      type = absoluteSafePath;
      default = "/var/lib/claryel-boxcore/secrets";
      description = "Absolute local secret-store path. Secret values must never be committed to Git.";
    };

    approvalMode = mkOption {
      type = types.enum [ "automatic-low-risk" "always-human" "offline-manual" ];
      default = "always-human";
      description = "Approval mode used only after schema and policy validation.";
    };

    homeAssistant = {
      enable = mkEnableOption "the public Home Assistant integration boundary";
      url = mkOption {
        type = types.strMatching "^https?://.*$";
        default = "http://127.0.0.1:8123";
        description = "Home Assistant URL. Credentials are resolved through the local secret store.";
      };
    };

    remoteAccess = {
      enable = mkEnableOption "an optional remote-access adapter";
      adapter = mkOption {
        type = types.enum [ "none" "cloudflare-tunnel" "wireguard" "custom" ];
        default = "none";
        description = "Optional adapter. No remote-access provider owns configuration truth.";
      };
    };

    outOfBand = {
      adapter = mkOption {
        type = types.enum [ "none" "intel-amt" "redfish" "ipmi" ];
        default = "none";
        description = "Optional hardware-management adapter; disabled by default.";
      };
      allowPowerControl = mkOption {
        type = types.bool;
        default = false;
        description = "Explicit local gate for power-control actions after separate authentication and policy approval.";
      };
    };
  };

  config = mkIf cfg.enable {
    assertions = [
      {
        assertion = cfg.remoteAccess.enable || cfg.remoteAccess.adapter == "none";
        message = "A remote-access adapter cannot be selected while remote access is disabled.";
      }
      {
        assertion = !cfg.remoteAccess.enable || cfg.remoteAccess.adapter != "none";
        message = "Remote access cannot be enabled without selecting an adapter.";
      }
      {
        assertion = cfg.outOfBand.adapter != "none" || !cfg.outOfBand.allowPowerControl;
        message = "Power control requires an explicit out-of-band adapter.";
      }
      {
        assertion = cfg.desiredStatePath != cfg.secretStorePath;
        message = "Desired state and secret storage must use separate paths.";
      }
    ];

    systemd.tmpfiles.rules = [
      "d /var/lib/claryel-boxcore 0750 root root -"
      "d ${cfg.secretStorePath} 0700 root root -"
      "d /var/lib/claryel-boxcore/state 0750 root root -"
      "d /var/log/claryel-boxcore 0750 root root -"
    ];

    environment.systemPackages = [ pkgs.git pkgs.jq ];

    systemd.services.claryel-boxcore-baseline-check = {
      description = "CLARYEL Box Core public baseline validation";
      wantedBy = [ "multi-user.target" ];
      after = [ "local-fs.target" "systemd-tmpfiles-setup.service" ];
      serviceConfig = {
        Type = "oneshot";
        RemainAfterExit = true;
        User = "root";
        Group = "root";
        NoNewPrivileges = true;
        PrivateTmp = true;
        ProtectSystem = "strict";
        ProtectHome = true;
        ProtectHostname = true;
        ProtectKernelTunables = true;
        ProtectKernelModules = true;
        ProtectControlGroups = true;
        RestrictAddressFamilies = [ "AF_UNIX" ];
        LockPersonality = true;
        MemoryDenyWriteExecute = true;
        UMask = "0077";
        ReadOnlyPaths = [ cfg.desiredStatePath cfg.secretStorePath ];
      };
      script = ''
        set -eu
        test -d ${lib.escapeShellArg cfg.desiredStatePath}
        test -d ${lib.escapeShellArg cfg.secretStorePath}
        test ! -L ${lib.escapeShellArg cfg.secretStorePath}
        printf '%s\n' ${lib.escapeShellArg "Box Core baseline ready for ${cfg.systemId}; no configuration was mutated."}
      '';
    };
  };
}
