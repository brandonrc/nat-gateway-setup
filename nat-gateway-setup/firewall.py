import os
import subprocess
from .utils import CustomException

class FirewallManager:

    def configure_firewall(self):
        """
        Configure the firewall to forward traffic from one network interface to another.

        :raise: CustomException if the firewall configuration fails
        """
        try:
            # Add your firewall configuration commands here
            # Example: subprocess.check_call(['firewall-cmd', '--add-forward-port'])
        except subprocess.CalledProcessError as e:
            raise CustomException(f"Firewall configuration failed with error: {str(e)}") from None
