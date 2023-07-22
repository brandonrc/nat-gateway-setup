import os
import subprocess
import distro
import ipaddress

def enable_ip_forwarding():
    """
    Enable IP forwarding.
    
    :raise: CustomException if the configuration fails
    """
    try:
        if get_linux_distribution() in ['centos', 'redhat']:
            with open('/etc/sysctl.d/99-ipforward.conf', 'w') as f:
                f.write('net.ipv4.ip_forward = 1\n')
            subprocess.check_call(['sysctl', '-p', '/etc/sysctl.d/99-ipforward.conf'])
        elif get_linux_distribution() in ['ubuntu', 'debian']:
            with open('/etc/sysctl.conf', 'a') as f:
                f.write('\nnet.ipv4.ip_forward=1\n')
            subprocess.check_call(['sysctl', '-p'])
        else:
            raise CustomException("Unsupported Linux distribution for IP forwarding configuration.")
    except subprocess.CalledProcessError as e:
        raise CustomException(f"IP forwarding configuration failed with error: {str(e)}") from None

def get_ip_range(start_ip: str, count: int):
    start_ip_int = int(ipaddress.IPv4Address(start_ip))
    end_ip_int = start_ip_int + count - 1
    end_ip = ipaddress.IPv4Address(end_ip_int)
    return f"{start_ip},{end_ip}"

def get_linux_distribution():
    """
    Detect the Linux distribution.

    :return: String identifier for the detected Linux distribution
    """
    try:
        return distro.id()
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
