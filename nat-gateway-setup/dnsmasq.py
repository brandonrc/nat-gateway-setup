import os
import shutil
import subprocess
import glob
from .utils import CustomException
import tarfile
import time

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

def configure_dnsmasq(dns_interface, dns_range):
    """
    Configure DNSMasq.

    :param dns_interface: The network interface for DNSMasq to bind.
    :param dns_range: The IP range for DNSMasq to assign IPs from.
    :raise: CustomException if the configuration fails
    """
    try:
        backup_dnsmasq_configuration()
        
        with open(f'/etc/dnsmasq.d/nat_{dns_interface}.conf', 'w') as f:
            f.write(f"""
                bind-interfaces
                interface={dns_interface}
                except-interface=lo
                dhcp-range={dns_range}
            """)

        subprocess.check_call(['systemctl', 'restart', 'dnsmasq'])

    except subprocess.CalledProcessError as e:
        raise CustomException(f"DNSMasq configuration failed with error: {str(e)}") from None
