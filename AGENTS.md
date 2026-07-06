# Agent Instructions

## Project Overview

This is the Mailinator Python SDK. It is a thin request-object wrapper around the Mailinator API. The OpenAPI specification is the source of truth for endpoint behavior.

## Important Files

- `mailinator/base.py`: `RequestData`, `RequestMethod`, and the shared API base URL.
- `mailinator/mailinator.py`: HTTP transport, headers, error handling, and response hydration.
- `mailinator/message.py`, `domain.py`, `rules.py`, `stats.py`, `authenticators.py`, `webhooks.py`: request classes grouped by API area.
- `mailinator/models.py`: response and payload models.
- `mailinator/__init__.py`: package-root exports and the authoritative `__version__`.
- `tests/test_mailinator_mocked.py`: primary fast mocked test suite.
- `tests/test_mailinator_mocked_new.py`: newer mocked endpoint coverage.
- `tests/test_mailinator.py`: integration tests that require Mailinator credentials.
- `ROADMAP.md`: current OpenAPI alignment gaps and modernization work.
- `OPENAPI_ALIGNMENT.md`: detailed workflow for auditing the SDK against the OpenAPI spec.

## Development Commands

- Run the primary mocked tests: `python -m pytest tests/test_mailinator_mocked.py`
- Run the newer mocked tests: `python -m pytest tests/test_mailinator_mocked_new.py`
- Run the full suite: `python -m pytest`
- Run integration tests: `python -m pytest tests/test_mailinator.py -s`

Integration tests require valid environment values and skip when required settings are missing. Prefer mocked tests for normal SDK changes unless live API behavior is explicitly under review.

## Coding Conventions

- Add one `{Operation}Request` class per API operation.
- Request classes inherit from `RequestData`.
- Build URLs from `RequestData._base_url`, currently `https://api.mailinator.com/api/v2`.
- Validate required constructor arguments with `check_parameter`.
- Group request classes in the module that matches their API area; do not create one file per request class.
- Add or update response and payload models in `mailinator/models.py` when schemas change.
- Keep public request and model classes importable from the package root through `mailinator/__init__.py`.
- Keep `mailinator/__init__.py` as the package version source; `setup.py` reads `__version__` from there.
- Do not bump `__version__` unless explicitly asked.
- Do not build, publish, or upload packages unless explicitly asked.
- Do not remove deprecated request classes without explicit maintainer approval.

## API Alignment

For OpenAPI gap analysis, endpoint reconciliation, or broad SDK alignment work, follow `OPENAPI_ALIGNMENT.md` before changing code. `ROADMAP.md` tracks the known outstanding gaps. Update `ROADMAP.md` when an alignment item is completed, deferred, or newly discovered.

## Safety

- Do not commit secrets or real `.env` values.
- Do not run integration tests against live Mailinator credentials unless explicitly asked.
- Avoid changing live API behavior without mocked test coverage for URL generation, request method, payload, and model hydration.
