import os
import shutil
import subprocess
import glob
from .utils import CustomException
import tarfile
import time
import re

def backup_dnsmasq_configuration(backup_folder="/var/cache/nat-linux-gateway"):
    """
    Backup existing dnsmasq configuration.

    :param backup_folder: The directory to store the backup.
    :raise: CustomException if the backup fails
    """
    timestamp = time.strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(backup_folder, f'dnsmasq_backup_{timestamp}.tar.gz')

    with tarfile.open(backup_file, 'w:gz') as tar:
        try:
            tar.add('/etc/dnsmasq.conf')
            tar.add('/etc/dnsmasq.d/')
        except Exception as e:
            raise CustomException(f"Backup of existing dnsmasq configuration failed with error: {str(e)}") from None


def restore_dnsmasq_configuration(backup_folder="/var/cache/nat-linux-gateway", backup_file=None):
    """
    Restore dnsmasq configuration from a backup.

    :param backup_folder: The directory where the backup is stored.
    :param backup_file: The tar.gz file to restore from. If None, uses the latest backup.
    :raise: CustomException if the restore fails
    """
    if backup_file is None:
        backup_files = sorted(os.listdir(backup_folder))
        if not backup_files:
            raise CustomException("No backup files found.")
        backup_file = os.path.join(backup_folder, backup_files[-1])

    with tarfile.open(backup_file, 'r:gz') as tar:
        try:
            tar.extractall(path='/etc/')
        except Exception as e:
            raise CustomException(f"Restoring dnsmasq configuration failed with error: {str(e)}") from None

def check_dnsmasq_configs(dns_interface):
    """
    Check if there are conflicting configurations in dnsmasq settings.

    :param dns_interface: The network interface that dnsmasq should bind to.
    :raise: CustomException if a conflicting configuration is found
    """
    # Check if there are conflicting configurations in /etc/dnsmasq.conf
    with open('/etc/dnsmasq.conf', 'r') as f:
        contents = f.read()
        if re.search(rf'interface={dns_interface}', contents):
            raise CustomException(f"Conflict found in /etc/dnsmasq.conf for interface {dns_interface}")

    # Check if there are conflicting configurations in /etc/dnsmasq.d/
    for filename in glob.glob('/etc/dnsmasq.d/*.conf'):
        with open(filename, 'r') as f:
            contents = f.read()
            if re.search(rf'interface={dns_interface}', contents):
                raise CustomException(f"Conflict found in {filename} for interface {dns_interface}")


def restart_dnsmasq():
    """
    Restart the dnsmasq service.

    :raise: CustomException if the service fails to restart
    """
    try:
        subprocess.check_call(['systemctl', 'restart', 'dnsmasq'])
    except subprocess.CalledProcessError as e:
        raise CustomException(f"Failed to restart dnsmasq service: {str(e)}") from None


def configure_dnsmasq(dns_interface, ip_range, dns_server, lease_time):
    """
    Configure dnsmasq with the given parameters.

    :param dns_interface: The network interface that dnsmasq should bind to.
    :param ip_range: The IP range for DHCP.
    :param dns_server: The upstream DNS server.
    :param lease_time: The DHCP lease time.
    :raise: CustomException if the configuration fails
    """
    try:
        # First, check for conflicts
        check_dnsmasq_configs(dns_interface)

        # Write our new configuration
        with open(f'/etc/dnsmasq.d/nat_{dns_interface}.conf', 'w') as f:
            f.write(f"interface={dns_interface}\n")
            f.write(f"dhcp-range={ip_range},{lease_time}\n")
            f.write(f"dhcp-option=6,{dns_server}\n")
            f.write("no-resolv\n")
            f.write("no-poll\n")
            f.write("bind-interfaces\n")

        # Restart the dnsmasq service to apply changes
        restart_dnsmasq()

    except Exception as e:
        raise CustomException(f"DNSMasq configuration failed with error: {str(e)}") from None
