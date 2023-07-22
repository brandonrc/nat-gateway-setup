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

class DependencyManager:

    linux_distribution = get_linux_distribution()

    DEPENDENCIES = {
        'ubuntu': {'firewall': 'ufw', 'dnsmasq': 'dnsmasq', 'network_manager': 'network-manager', 'systemd': 'systemd'},
        'redhat': {'firewall': 'firewalld', 'dnsmasq': 'dnsmasq', 'network_manager': 'NetworkManager', 'systemd': 'systemd'}
    }

    REQUIRED_DEPENDENCIES = DEPENDENCIES.get(linux_distribution, {})

    if not REQUIRED_DEPENDENCIES:
        print(f"Unsupported Linux distribution: {linux_distribution}")
        return

    def check_dependencies(self):
        self.missing_dependencies = [dep for dep in self.REQUIRED_DEPENDENCIES if not self.is_installed(dep)]

    def install_missing_dependencies(self):
        for dep in self.missing_dependencies:
            self.install_dependency(dep)

    def is_installed(self, dependency):
        try:
            subprocess.check_call(['which', dependency])
            return True
        except subprocess.CalledProcessError:
            return False

    def install_dependency(self, dependency):
        try:
            if os.path.isfile('/usr/bin/yum'):
                subprocess.check_call(['yum', 'install', '-y', dependency])
            elif os.path.isfile('/usr/bin/apt-get'):
                subprocess.check_call(['apt-get', 'install', '-y', dependency])
            else:
                raise CustomException("Unsupported package manager. Cannot install dependencies.")
        except subprocess.CalledProcessError as e:
            raise CustomException(f"Dependency installation failed with error: {str(e)}") from None
