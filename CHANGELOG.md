## Unreleased - 2023-07-22

### Added
- Prompt-based interactive CLI with the support of 'prompt_toolkit'.
- Time string sanitization function `time_check()`.
- Dependency check and installation functions for Ubuntu and Red Hat.
- Support for NAT configuration in NetworkManager.
- Backup and restore functions for dnsmasq and firewall configurations.
- Unit tests for `time_check()` and other helper functions.

### Changed
- Refactored existing codebase to use more pure functions.
- Reorganized the code structure and separated functions into different Python modules.

### Removed
- Removed dependency on object-oriented design, instead migrated to functional programming approach for simplicity and readability.
