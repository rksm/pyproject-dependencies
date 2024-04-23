{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
      pythonPackages = pkgs.python311Packages;
      python = pkgs.python311;
    in
    with pythonPackages;
    {

      devShells.default = pkgs.mkShell {
        packages = [ python ];
      };

      packages.default = buildPythonApplication {
        pname = "pyproject-dependencies";
        version = "0.1.0";
        pyproject = true;

        build-system = [
          setuptools-scm
        ];
        src = ./.;

        dependencies = [
          setuptools
        ];

        propagatedNativeBuildInputs = [
          pip
          toml
        ];

        meta = with pkgs.lib; {
          description = "Install dependencies from pyproject.toml";
          license = licenses.mit;
          platforms = platforms.unix;
        };
      };

    }
    );
}
