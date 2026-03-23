# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project aims to follow Semantic Versioning.

## [Unreleased]

### Added

- `GetInboxRequest` supports the `delete` query parameter (added 2025-03-05).

### Changed

- N/A

### Fixed

- N/A

## [1.0.8] - 2026-03-23

### Added

- `.env`-based configuration for integration tests (loader in `tests/dotenv.py` and example file `.env.example`).

### Changed

- Marked all rules endpoint request classes as deprecated in code.
- Marked domain management write requests as deprecated in code (`CreateDomainRequest`, `DeleteDomainRequest`).
- Added runtime `DeprecationWarning` emissions for:
  - `CreateRuleRequest`
  - `EnableRuleRequest`
  - `DisableRuleRequest`
  - `GetRulesRequest`
  - `GetRuleRequest`
  - `DeleteRuleRequest`
  - `CreateDomainRequest`
  - `DeleteDomainRequest`
- Integration tests now load `.env` automatically and skip when required settings are missing (instead of exiting immediately).

### Fixed

- Fixed typos in `tests/test_mailinator.py` that prevented the test module from running.
