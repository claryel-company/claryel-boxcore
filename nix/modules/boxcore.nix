{ config, lib, pkgs, ... }:

let
  cfg = config.services.claryelBoxCore;
  inherit (lib) mkEnableOption mkIf mkOption types;
in
{
  options.services.claryelBoxCore = {
    enable = mkEnableOption "CLARYEL Box Core public baseline";

    systemId = mkOption {
      type = types.strMatching "^[a-z0-9][a-z0-9-]{1,62}$";
      example = "home-main";
      description = "Public technical identifier. Do not use a customer name or personal identifier.";
    };

    desiredStatePath = mkOption {
      type = types.path;
      description = "Path to a local checkout containing technical desired state only.";
    };

    secretStorePath = mkOption {
      type = types.path;
      default = "/var/lib/claryel-boxcore/secrets";
      description = "Local secret-store path. Secret values must never be committed to Git.";
    };

    approvalMode = mkOption {
      type = types.enum [ "automatic-low-risk" "always-human" "offline-manual" ];
      default = "always-human";
      description = "Approval mode used after schema and policy validation.";
    };

    homeAssistant = {
      enable = mkEnableOption "the public Home Assistant integration boundary";
      url = mkOption {
        type = types.str;
        default = "http://127.0.0.1:8123";
        description = "Local Home Assistant URL. Credentials are referenced through the local secret store.";
      };
    };

    remoteAccess = {
      enable = mkEnableOption "an optional remote-access adapter";
      adapter = mkOption {
        type = types.enum [ "none" "cloudflare-tunnel" "wireguard" "custom" ];
        default = "none";
        description = "Optional adapter. Box Core does not depend on a single remote-access provider.";
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
        description = "Explicit local gate for power-control actions.";
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
        assertion = cfg.outOfBand.adapter != "none" || !cfg.outOfBand.allowPowerControl;
        message = "Power control requires an explicit out-of-band adapter.";
      }
    ];

    # English: The public baseline creates local boundaries but performs no destructive deployment actions.
    # Русский: Публичная основа создаёт локальные границы, но не выполняет разрушающие deployment-действия.
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
      after = [ "local-fs.target" ];
      serviceConfig = {
        Type = "oneshot";
        RemainAfterExit = true;
      };
      script = ''
        set -eu
        # English: Refuse to start when the desired-state path is unavailable.
        # Русский: Отказываться от запуска, если путь desired state недоступен.
        test -d ${lib.escapeShellArg (toString cfg.desiredStatePath)}

        # English: Secret values belong only to the local protected directory.
        # Русский: Значения секретов принадлежат только локальному защищённому каталогу.
        test -d ${lib.escapeShellArg (toString cfg.secretStorePath)}

        printf '%s\n' ${lib.escapeShellArg "Box Core baseline ready for ${cfg.systemId}; no configuration was mutated."}
      '';
    };
  };
}
