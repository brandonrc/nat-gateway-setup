import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
import ipaddress
from utils import get_linux_distribution, CustomException
from dependency_manager import get_required_dependencies, check_dependencies, install_missing_dependencies
from firewall import configure_firewall
from dnsmasq import configure_dnsmasq, check_dnsmasq_configs, restart_dnsmasq
from network_interface import configure_interface

class IPValidator(Validator):
    def validate(self, document):
        try:
            ipaddress.IPv4Address(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a valid IP address", cursor_position=len(document.text))

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='the IP address')
    parser.add_argument('--netmask', help='the netmask')
    parser.add_argument('--wlan', help='the incoming network interface (WLAN)')
    parser.add_argument('--lan', help='the local network interface (LAN)')
    args = parser.parse_args()

    # Check and install dependencies
    linux_distribution = get_linux_distribution()
    required_dependencies = get_required_dependencies(linux_distribution)
    missing_dependencies = check_dependencies(required_dependencies)
    install_missing_dependencies(missing_dependencies)

    # If arguments are not provided via command line, ask for user input
    ip = args.ip if args.ip else prompt("Please enter the IP address: ", validator=IPValidator())
    netmask = args.netmask if args.netmask else prompt("Please enter the netmask: ")  # add validation if desired
    wlan_interface = args.wlan if args.wlan else prompt("Please enter the incoming network interface (WLAN): ")
    lan_interface = args.lan if args.lan else prompt("Please enter the local network interface (LAN): ")

    # Setup network interface
    configure_interface(lan_interface, ip, netmask)

    # Setup dnsmasq
    check_dnsmasq_configs(lan_interface)
    configure_dnsmasq(lan_interface, ip, netmask)
    restart_dnsmasq()

    # Setup firewall
    configure_firewall(wlan_interface, lan_interface)

if __name__ == "__main__":
    main()
