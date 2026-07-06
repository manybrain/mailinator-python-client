# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project aims to follow Semantic Versioning.

## [1.0.9]

### Added

- Mocked endpoint tests covering SDK request dispatch, response handling, model deserialization, warnings, and required parameter validation without Mailinator credentials.
- Forward-looking mocked tests for newly planned message retrieval and stream endpoints.
- SDK support for domain message listing and message summary/text/header retrieval request classes.

### Changed

- Deprecated singular authenticator request classes and routed them through the canonical `/authenticators/` endpoints. These are duplicate endpoints.
- Raised the minimum supported Python version to 3.9.
- Updated development and release dependency pins in `requirements.txt`.

## [1.0.8]

### Added

- `.env`-based configuration for integration tests (loader in `tests/dotenv.py` and example file `.env.example`).
- `GetInboxRequest` supports the `delete` query parameter (added 2025-03-05).

### Changed

- Marked all rules endpoint request classes as deprecated in code.
- Marked domain management write requests as deprecated in code (`CreateDomainRequest`, `DeleteDomainRequest`).
- Marked `GetLatestMessagesRequest` and `GetLatestInboxMessagesRequest` as deprecated (emits `DeprecationWarning`).
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
- Fixed `DisableRuleRequest` URL to use `action=disable` (was `action=enable`).
