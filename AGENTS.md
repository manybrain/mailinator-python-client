# Repository Instructions for Coding Agents

## Project Overview

This is the Mailinator Python SDK. It is a thin request-object wrapper around the Mailinator API. The OpenAPI specification is the source of truth for endpoint behavior.

## Documentation Ownership

- `README.md` documents installation and public usage.
- `OPENAPI_ALIGNMENT.md` is the canonical guide to the SDK architecture, request conventions, and OpenAPI alignment workflow.
- `ROADMAP.md` records current alignment gaps and modernization work. Keep it current when work is completed, deferred, or newly discovered.
- This file contains only agent-specific repository policy, commands, and safety constraints. Do not duplicate the detailed alignment workflow here.

## Development Commands

- Run the primary mocked tests: `python -m pytest tests/test_mailinator_mocked.py`
- Run the newer mocked tests: `python -m pytest tests/test_mailinator_mocked_new.py`
- Run the full suite: `python -m pytest`
- Run integration tests: `python -m pytest tests/test_mailinator.py -s`

Integration tests require valid environment values and skip when required settings are missing. Prefer mocked tests for normal SDK changes unless live API behavior is explicitly under review.

## Repository Conventions

- Follow `OPENAPI_ALIGNMENT.md` for request, model, URL, export, and endpoint-audit conventions.
- Keep `mailinator/__init__.py` as the package version source; `setup.py` reads `__version__` from there.
- Do not bump `__version__` unless explicitly asked.
- Do not build, publish, or upload packages unless explicitly asked.
- Do not remove deprecated request classes without explicit maintainer approval.

## API Alignment

Read and follow `OPENAPI_ALIGNMENT.md` before performing OpenAPI gap analysis, endpoint reconciliation, or broad SDK alignment work. Check `ROADMAP.md` for known gaps before starting, and update it when the status or scope of an alignment item changes.

## Safety

- Do not commit secrets or real `.env` values.
- Do not run integration tests against live Mailinator credentials unless explicitly asked.
- Avoid changing live API behavior without mocked test coverage for URL generation, request method, payload, and model hydration.
