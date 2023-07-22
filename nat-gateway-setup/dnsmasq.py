import os
import subprocess
from .utils import CustomException

class DNSMasqManager:

    def install_dnsmasq(self):
        """
        Install DNSMasq using the appropriate package manager.

        :raise: CustomException if the installation fails
        """
        try:
            if os.path.isfile('/usr/bin/yum'):
                subprocess.check_call(['yum', 'install', '-y', 'dnsmasq'])
            elif os.path.isfile('/usr/bin/apt-get'):
                subprocess.check_call(['apt-get', 'install', '-y', 'dnsmasq'])
            else:
                raise CustomException("Unsupported package manager. Please manually install dnsmasq.")
        except subprocess.CalledProcessError as e:
            raise CustomException(f"DNSMasq installation failed with error: {str(e)}") from None

    def configure_dnsmasq(self):
        """
        Configure DNSMasq.

        :raise: CustomException if the configuration fails
        """
        try:
            # Add your dnsmasq configuration commands here
            # Example: subprocess.check_call(['systemctl', 'restart', 'dnsmasq'])
        except subprocess.CalledProcessError as e:
            raise CustomException(f"DNSMasq configuration failed with error: {str(e)}") from None
