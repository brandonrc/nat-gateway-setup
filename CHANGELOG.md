# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2023-07-23

### Added
- Implemented a Python-based NAT gateway configuration tool for Linux systems.
- Provided support for Debian-based (including Ubuntu) and Red Hat-based (including CentOS) distributions.
- Implemented command line arguments and interactive user input for configuration parameters such as IP address, netmask, WLAN interface, and LAN interface.
- Developed functions for dependency management including checking for necessary dependencies and automated installation.
- Developed functionality for network interface configuration using NetworkManager.
- Implemented configuration of dnsmasq for providing DHCP and DNS services.
- Implemented firewall configuration to allow traffic forwarding. The implementation includes support for both `firewall-cmd` and `ufw`.
- Added functionality to backup firewall configuration before making changes.
- Provided functionality to calculate and set the IP range for DHCP from a given IP address and a count of desired addresses.
- Developed a utility to fetch and set the DNS server address for dnsmasq based on the existing DNS configuration of the WLAN interface.
- Added comprehensive exception handling and custom exceptions for efficient error management and reporting.

### Changed
- Optimized code for improved structure and readability.
- Enhanced compatibility across various Linux distributions.
- Improved user input validation and error handling mechanisms.

### Fixed
- Fixed the issue with DNS settings propagation to client machines.
- Addressed the problem with IP forwarding settings on Red Hat-based distributions.

### Removed
- None