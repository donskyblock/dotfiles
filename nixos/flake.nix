{
  description = "Don's NixOS config";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    helium = {
      url = "github:FKouhai/helium2nix/main";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, helium, ... }:
    let
      system = "x86_64-linux";
    in {
      nixosConfigurations.don = nixpkgs.lib.nixosSystem {
        inherit system;

        modules = [
          ./configuration.nix

          ({ pkgs, ... }: {
            environment.systemPackages = with pkgs; [
                # helium
                helium.defaultPackage.${system}

                # Node.js (includes npm + npx)
                nodejs

                # package managers
                pnpm
                yarn

                # modern replacements
                typescript
            ];
          })
        ];
      };
    };
}