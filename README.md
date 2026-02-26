# Mailinator Python SDK

The official Mailinator Python SDK. This REST API client is implemented as a thin wrapper around the [Mailinator API](https://www.mailinator.com/documentation/docs/api/index.html). The OpenAPI specification is the source of truth.


## API Reference

See [Mailinator's API Reference](https://www.mailinator.com/documentation/docs/api/index.html) for all of the currently available API endpoints.

## Documentation

- OpenAPI spec: <https://github.com/manybrain/mailinatordocs/blob/main/openapi/mailinator-api.yaml>
- SDK examples: [`EXAMPLEs.md`](EXAMPLEs.md)

## Installation

```bash
pip install mailinator-python-client-2
```

## Quick Start

```python
from mailinator import Mailinator

client = Mailinator("YOUR_API_TOKEN")
```

For request examples (inbox, messages, domains, rules, webhooks, and stats), see [`EXAMPLEs.md`](EXAMPLEs.md).

## Tests

Run tests with:

```bash
python -m pytest -s
```

Most tests require valid environment values. Use `tests/localsettings.py.template` as the source for local test configuration.
