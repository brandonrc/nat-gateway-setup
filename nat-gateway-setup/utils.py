import os
import subprocess
import platform

def get_linux_distribution():
    """
    Detect the Linux distribution.

    :return: String identifier for the detected Linux distribution
    """
    try:
        return platform.linux_distribution()[0].lower()
    except:
        return "unknown"

class CustomException(Exception):
    pass

DEPENDENCIES = {
    'ubuntu': {'firewall': 'ufw', 'dnsmasq': 'dnsmasq', 'network_manager': 'network-manager', 'systemd': 'systemd'},
    'redhat': {'firewall': 'firewalld', 'dnsmasq': 'dnsmasq', 'network_manager': 'NetworkManager', 'systemd': 'systemd'}
}

def get_required_dependencies(linux_distribution):
    return DEPENDENCIES.get(linux_distribution, {})

def check_dependencies(dependencies):
    return [dep for dep in dependencies if not is_installed(dep)]

def install_missing_dependencies(missing_dependencies):
    for dep in missing_dependencies:
        install_dependency(dep)

def is_installed(dependency):
    try:
        subprocess.check_call(['which', dependency])
        return True
    except subprocess.CalledProcessError:
        return False

def install_dependency(dependency):
    try:
        if os.path.isfile('/usr/bin/yum'):
            subprocess.check_call(['yum', 'install', '-y', dependency])
        elif os.path.isfile('/usr/bin/apt-get'):
            subprocess.check_call(['apt-get', 'install', '-y', dependency])
        else:
            raise CustomException("Unsupported package manager. Cannot install dependencies.")
    except subprocess.CalledProcessError as e:
        raise CustomException(f"Dependency installation failed with error: {str(e)}") from None
