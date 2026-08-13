# Mailinator Python SDK

The official Mailinator Python SDK. This REST API client is implemented as a thin wrapper around the [Mailinator API](https://www.mailinator.com/documentation/docs/api/index.html). The OpenAPI specification is the source of truth.

## API Reference

See [Mailinator's API Reference](https://www.mailinator.com/documentation/docs/api/index.html) for all of the currently available API endpoints.

## Documentation

- OpenAPI spec: <https://github.com/manybrain/mailinatordocs/blob/main/openapi/mailinator-api.yaml>
- SDK examples: [`EXAMPLE.md`](EXAMPLE.md)
- SDK architecture and OpenAPI alignment workflow: [`OPENAPI_ALIGNMENT.md`](OPENAPI_ALIGNMENT.md)
- Current modernization and alignment work: [`ROADMAP.md`](ROADMAP.md)

## Installation

```bash
pip install mailinator-python-client-2
```

## Quick Start

```python
from mailinator import Mailinator

client = Mailinator("YOUR_API_TOKEN")
```

For request examples (inbox, messages, domains, rules, webhooks, and stats), see [`EXAMPLE.md`](EXAMPLE.md).

## Tests

Run the mocked tests with:

```bash
python -m pytest tests/test_mailinator_mocked.py
```

These tests do not make network requests and do not require Mailinator credentials.

Run the integration tests with:

```bash
python -m pytest tests/test_mailinator.py -s
```

Integration tests require valid environment values and will skip when required settings are missing.

Use either:

- `.env` (recommended): copy `.env.example` to `.env` and fill in values.
- `tests/localsettings.py`: copy `tests/localsettings.py.template` to `tests/localsettings.py` (it also loads `.env` if present).

Run the full suite with:

```bash
python -m pytest
```
