# AI Instructions

This document explains the relationship between this Python client and the Mailinator OpenAPI specification.

**OpenAPI Specification:** [https://github.com/manybrain/mailinatordocs/blob/main/openapi/mailinator-api.yaml](https://github.com/manybrain/mailinatordocs/blob/main/openapi/mailinator-api.yaml)

## Codebase Structure

The codebase structure is module-oriented under `mailinator/` and reflects Mailinator API domains.

-   **Request modules:** API request classes live in module files such as:
    -   `mailinator/message.py` for inbox/message operations
    -   `mailinator/domain.py` for domain operations
    -   `mailinator/rules.py` for rules operations
    -   `mailinator/stats.py` for team/stats operations
    -   `mailinator/authenticators.py` for authenticator operations
    -   `mailinator/webhooks.py` for private webhook operations
-   **Request base types:** Shared request primitives are in `mailinator/base.py` (`RequestMethod`, `RequestData`).
-   **Client transport:** HTTP execution logic is in `mailinator/mailinator.py` (`Mailinator.request`).
-   **Entities/models:** Response and payload models are centralized in `mailinator/models.py`.

## Request Patterns

This client uses a **Request Object** pattern implemented with Python classes that inherit from `RequestData`.

-   **Naming convention:** Request classes are named `{Operation}Request` (for example, `GetInboxRequest`, `DeleteDomainRequest`, `CreateRuleRequest`).
-   **Definition style:** Each class constructor validates required params (`check_parameter`) and builds the URL from `RequestData._base_url` (`https://api.mailinator.com/api/v2`).
-   **HTTP mapping:** Each class calls `super().__init__(RequestMethod.<METHOD>, url, model=<ModelClass>, json=<payload>)` to define the HTTP method, endpoint, response model, and optional request body.
-   **Location:** Multiple request classes are grouped by API area in a single module file (not one file per request class).

## Execution

Requests are executed through `Mailinator`.

```python
from mailinator import Mailinator, GetInboxRequest

client = Mailinator("api_token")
request = GetInboxRequest("domain.com", "inbox_name")
response = client.request(request)
```

`Mailinator.request()` dispatches on `RequestMethod` and uses `requests` to execute HTTP calls. If `request_data.model` is provided and the response is JSON, the client instantiates that model with the response body.

## Entities

Entities are Python model classes in `mailinator/models.py`.

-   Examples include `Inbox`, `Message`, `Domain`, `Rule`, `Stats`, and `Webhook`.
-   Request classes reference these via the `model=` argument in `RequestData`.
-   Payload-style entities expose `to_json()` for outgoing request bodies (for example `PostMessage`, `Rule`, `Condition`, `Action`).

---

## Gap Analysis Workflow

Use this workflow whenever you want to audit the SDK against the OpenAPI spec, identify missing or extra coverage, and bring the two into alignment.

### Step 1 — Fetch the OpenAPI Specification

Retrieve the raw YAML from:

```
https://raw.githubusercontent.com/manybrain/mailinatordocs/main/openapi/mailinator-api.yaml
```

> The rendered GitHub page is at https://github.com/manybrain/mailinatordocs/blob/main/openapi/mailinator-api.yaml
> but always read the **raw** URL for machine parsing.

Extract every `paths` entry. For each path, record:
- The HTTP method (`get`, `post`, `put`, `delete`, etc.)
- The full path string (e.g. `/api/v2/domains/{domain}/inboxes/{inbox}`)
- The `operationId`
- The tag (maps to the SDK module directory)
- All query parameters defined under `parameters`

### Step 2 — Catalogue the SDK

For each request class under `mailinator/*.py`:
1. Identify classes ending in `Request` that inherit from `RequestData`.
2. Capture method, URL, model, and JSON body from the `super().__init__(RequestMethod.<METHOD>, url, model=..., json=...)` call.
3. Record query parameters passed in the URL (both dynamically built query strings and inline `?key=value` values).
4. Note whether the endpoint is currently documented as deprecated in class docstring/comments.

Also enumerate request modules (`message.py`, `domain.py`, `rules.py`, `stats.py`, `authenticators.py`, `webhooks.py`) and cross-reference with OpenAPI tags.

### Step 3 — Identify Gaps

Produce a gap report with four sections:

#### A. In the spec but missing from the SDK
List every `operationId` that has no corresponding Python request class. This is what needs to be **added**.

#### B. In the SDK but not in the spec
List every request class whose URL has no matching path+method in the spec.
- If it is marked deprecated, note that separately.
- If it is not deprecated but still absent from the spec, flag it for clarification (it may be an undocumented endpoint).

#### C. URL path mismatches
Compare the base path used by each SDK class against the spec.
- The spec base URL is `https://api.mailinator.com` and all paths start with `/api/v2/`.
- The SDK **must** use `/api/v2/` not `/v2/`. Flag any class using the wrong prefix.

#### D. Query parameter gaps
For each existing SDK class, compare the query parameters it sends against the spec's declared parameters for that operation. List any parameters the spec defines that the SDK does not implement.

### Step 4 — Build a Plan

Before making any changes, write out a plan that includes:

1. **New request classes to add** — one class per missing `operationId`, grouped by module directory.
2. **URL fixes** — list every file where the prefix needs to change from `/v2/` to `/api/v2/`.
3. **Query parameter additions** — list every file and which parameters to add.
4. **Deprecated classes** — decide whether to remove them or keep with explicit deprecation warnings/messages. Do not remove without confirmation.
5. **Model/schema updates** — if new endpoints return new schemas, list the Python model classes to create/update in `mailinator/models.py`.

Present the plan to the user and wait for approval before proceeding.

### Step 5 — Implement

Follow the existing patterns in the codebase:

#### Adding a new request class

Use an existing class as a template (for example in `mailinator/message.py`).

```python
from .base import RequestData, RequestMethod
from .models import *

class GetSomethingRequest(RequestData):
    def __init__(self, domain, item_id, optional_flag=None):
        self.check_parameter(domain, "domain")
        self.check_parameter(item_id, "item_id")

        base_url = f"{self._base_url}/domains/{domain}/something/{item_id}"

        params = {"optional_flag": optional_flag}
        query_string = "&".join(
            f"{key}={value}" for key, value in params.items() if value is not None
        )
        url = f"{base_url}?{query_string}" if query_string else base_url

        super().__init__(RequestMethod.GET, url, model=SomeModel)
```

Key rules:
- **Always** use `/api/v2/` as the path prefix — never `/v2/`.
- Place the class in the module file that matches the operation's OpenAPI tag.
- Ensure the class is exported via `mailinator/__init__.py` (directly or through module wildcard exports).
- Add/update corresponding models in `mailinator/models.py` if response schemas are new.

#### Fixing a URL prefix

Change `/v2/` → `/api/v2/` in URL construction.

#### Adding a missing query parameter

Add the parameter in the request constructor and include it in the query string builder:
```python
params = {"delete": delete}
query_string = "&".join(f"{key}={value}" for key, value in params.items() if value is not None)
url = f"{base_url}?{query_string}" if query_string else base_url
```

### Step 6 — Verify

After implementing:
1. Run `python -m pytest` — existing tests should pass.
2. Manually instantiate at least one updated/new request class and verify URL generation matches spec path exactly.
3. Verify model hydration works for JSON responses (`request_data.model(**response.json())` path).

### Notes on SDK Conventions

| Convention | Detail |
|---|---|
| Version source | Avoid duplicate hardcoded versions. Keep one authoritative package version and derive runtime user-agent version from it. |
| Auth header | Authenticated requests send `Authorization` header via `Mailinator` client initialization. |
| No-token requests | No-token access exists for private webhook request classes that rely on `whtoken` query parameter. |
| Deprecated marker | Mark deprecated request classes clearly in docstring/comments and use runtime warnings where possible. |
| Exports | Public request/model classes must remain importable from `mailinator` package root via `mailinator/__init__.py`. |
