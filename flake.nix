{
  description = "CLARYEL Box Core — reproducible public NixOS foundation";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };

  outputs = { self, nixpkgs }:
    let
      # English: Keep supported systems explicit until each one has public test evidence.
      # Русский: Явно перечислять поддерживаемые системы, пока для каждой не появится публичное evidence тестирования.
      supportedSystems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in {
      nixosModules = {
        default = import ./nix/modules;
        boxcore = import ./nix/modules/boxcore.nix;
      };

      checks = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in {
          # English: Validate public JSON files without requiring private infrastructure.
          # Русский: Проверять публичные JSON-файлы без зависимости от приватной инфраструктуры.
          public-json = pkgs.runCommand "boxcore-public-json" {
            nativeBuildInputs = [ pkgs.jq ];
          } ''
            find ${self}/schemas ${self}/examples ${self}/site-content -type f -name '*.json' -print0 \
              | xargs -0 -r -n1 jq empty
            touch $out
          '';
        });
    };
}
