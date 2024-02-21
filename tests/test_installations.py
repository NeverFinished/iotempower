import json
import os
import subprocess

import pytest

local_dir = os.getenv("IOTEMPOWER_LOCAL", "")
installation_options_file = os.path.join(local_dir, "installation_options.json")
if not os.path.isfile(installation_options_file):
    raise FileNotFoundError(
        f"Could not find {installation_options_file} to load the settings, it should be generated by iot_install"
    )

with open(installation_options_file, "r") as f:
    installation_options = json.load(f)

packages = [
    {"name": "python3.11-venv", "package_manager": "apt", "module": "general"},
    {"name": "git", "package_manager": "apt", "module": "general"},
    {"name": "jq", "package_manager": "apt", "module": "general"},
    {"name": "make", "package_manager": "apt", "module": "general"},
    {"name": "curl", "package_manager": "apt", "module": "general"},
    {"name": "nodejs", "package_manager": "apt", "module": "general"},
    {"name": "haveged", "package_manager": "apt", "module": "general"},
    {"name": "python3-dev", "package_manager": "apt", "module": "general"},
    {"name": "terminal-kit", "package_manager": "npm", "module": "general"},
    {"name": "g++", "package_manager": "apt", "module": "cloud_commander"},
    {"name": "gritty", "package_manager": "npm", "module": "cloud_commander"},
    {"name": "cloudcmd", "package_manager": "npm", "module": "cloud_commander"},
    {"name": "node-red", "package_manager": "npm", "module": "node_red"},
    {"name": "debian-keyring", "package_manager": "apt", "module": "caddy"},
    {"name": "apt-transport-https", "package_manager": "apt", "module": "caddy"},
    {"name": "debian-archive-keyring", "package_manager": "apt", "module": "caddy"},
    {"name": "caddy", "package_manager": "apt", "module": "caddy"},
    {"name": "mosquitto-clients", "package_manager": "apt", "module": "mosquitto"},
    {"name": "mosquitto", "package_manager": "apt", "module": "mosquitto"},
]

packages_to_test = []
for key, value in installation_options.items():
    if value.lower() == "1":
        packages_to_test += [tuple(package.values()) for package in packages if package["module"] == key]


@pytest.mark.parametrize("package_name, package_manager, module", packages_to_test)
def test_eval(package_name, package_manager, module) -> None:
    if package_manager == "apt":
        command = f"dpkg -s {package_name}"
    elif package_manager == "npm":
        command = f"cd {local_dir}/nodejs && npm list {package_name}"
    else:
        raise NotImplementedError("Only apt and npm packages are supported for now")
    result = subprocess.run(command, shell=True)
    assert result.returncode == 0, f"Cannot found {package_name} in your system which is need for {module}"
