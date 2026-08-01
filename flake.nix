{
  description = "CLARYEL Box Core — reproducible public NixOS foundation";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
  };

  outputs = { self, nixpkgs }:
    let
      # Support remains explicit until each architecture has public evidence.
      supportedSystems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in {
      nixosModules = {
        default = import ./nix/modules;
        boxcore = import ./nix/modules/boxcore.nix;
      };

      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          boxcoreNode = pkgs.buildGoModule {
            pname = "boxcore-node";
            version = "0.1.0";
            src = self;
            vendorHash = null;
            subPackages = [ "cmd/boxcore-node" ];
          };
        in {
          boxcore-node = boxcoreNode;
          default = boxcoreNode;
        });

      apps = forAllSystems (system: {
        boxcore-node = {
          type = "app";
          program = "${self.packages.${system}.boxcore-node}/bin/boxcore-node";
        };
        default = self.apps.${system}.boxcore-node;
      });

      checks = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in {
          public-json = pkgs.runCommand "boxcore-public-json" {
            nativeBuildInputs = [ pkgs.jq ];
          } ''
            find ${self}/schemas ${self}/examples ${self}/site-content -type f -name '*.json' -print0 \
              | xargs -0 -r -n1 jq empty
            touch $out
          '';

          node-package = self.packages.${system}.boxcore-node;
        });

      formatter = forAllSystems (system: (import nixpkgs { inherit system; }).nixpkgs-fmt);
    };
}
