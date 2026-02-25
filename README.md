# Official Mailinator Python Client

Python SDK for the [Mailinator](https://www.mailinator.com/) REST API.

## Documentation

- Mailinator API docs: <https://manybrain.github.io/mailinatordocs/#operation>
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
