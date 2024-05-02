{ pythonPackages ? (import <nixpkgs> {}).python3Packages }:
pythonPackages.buildPythonApplication {
  pname = "pyproject-dependencies";
  src = ./.;
  version = "0.1.0";
  propagatedBuildInputs = with pythonPackages; [
    setuptools
    toml
    pip
  ];
  pyproject = true;
}
