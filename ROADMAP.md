# Roadmap

This roadmap tracks the Python SDK modernization work in strict sequence.

### Prioritization



### A. In the spec but missing from the SDK

Add request classes for OpenAPI operations that do not currently have SDK equivalents:

- [ ] `listDomainMessages`: `GET /api/v2/domains/{domain}/inboxes`
  - Module: `mailinator/message.py`
  - Query params: `inbox`, `skip`, `limit`, `sort`, `decode_subject`, `cursor`, `full`, `wait`, `delete`
  - Response schema: `InboxMessagesResponse`
- [ ] `getMessageSummary`: `GET /api/v2/domains/{domain}/messages/{messageId}/summary`
  - Module: `mailinator/message.py`
  - Response schema: `MessageSummaryOnly`
- [ ] `getMessageText`: `GET /api/v2/domains/{domain}/messages/{messageId}/text`
  - Module: `mailinator/message.py`
  - Response schema: `MessageTextOnly`
- [ ] `getMessageTextPlain`: `GET /api/v2/domains/{domain}/messages/{messageId}/textplain`
  - Module: `mailinator/message.py`
  - Response schema: `MessageTextPlainOnly`
- [ ] `getMessageTextHtml`: `GET /api/v2/domains/{domain}/messages/{messageId}/texthtml`
  - Module: `mailinator/message.py`
  - Response schema: `MessageTextHtmlOnly`
- [ ] `getMessageHeaders`: `GET /api/v2/domains/{domain}/messages/{messageId}/headers`
  - Module: `mailinator/message.py`
  - Response schema: `MessageHeadersOnly`
- [ ] `streamDomainMessages`: `GET /api/v2/domains/{domain}/stream`
  - Module: `mailinator/message.py`
  - Query params: `full`, `limit`, `throttleInterval`, `delete`
  - Response schema: `MessageSummary`
- [ ] `streamInboxMessages`: `GET /api/v2/domains/{domain}/stream/{inbox}`
  - Module: `mailinator/message.py`
  - Query params: `full`, `limit`, `throttleInterval`, `delete`
  - Response schema: `MessageSummary`

### B. In the SDK but not in the spec

Keep these for now, but mark compatibility/deprecation decisions before changing public API:

- [ ] Authenticator endpoints absent from the spec:
  - `GetAuthenticatorsRequest`: `GET /api/v2/authenticators/`
  - `GetAuthenticatorRequest`: `GET /api/v2/authenticator/`
  - `GetAuthenticatorByIdRequest`: `GET /api/v2/authenticator/{id}`
- [ ] Webhook custom-service endpoints absent from the spec:
  - `PrivateCustomServiceWebhookRequest`: `POST /api/v2/domains/private/{customService}?whtoken=...`
  - `PrivateCustomServiceInboxWebhookRequest`: `POST /api/v2/domains/private/{customService}/{inbox}?whtoken=...`

### C. URL path mismatches

Fix SDK paths where an implemented operation maps to a spec operation but the path differs:

- [ ] `PostMessageRequest`
  - Current SDK: `POST /api/v2/domains/{domain}/inboxes/{inbox}`
  - Spec: `POST /api/v2/domains/{domain}/inboxes/{inbox}/messages`
- [ ] `PrivateWebhookRequest`
  - Current SDK: `POST /api/v2/domains/private/webhook?whtoken=...`
  - Spec: `POST /api/v2/domains/{domain}/webhook?whtoken=...`
  - Needs design decision because SDK currently takes `whToken` but no `domain`.
- [ ] `PrivateInboxWebhookRequest`
  - Current SDK: `POST /api/v2/domains/private/webhook/{inbox}?whtoken=...`
  - Spec: `POST /api/v2/domains/{domain}/webhook/{inbox}?whtoken=...`
  - Needs design decision because SDK currently takes `whToken` and `inbox` but no `domain`.
- [ ] `GetTeamStatsRequest`
  - Current SDK: `GET /api/v2/team/stats/`
  - Spec: `GET /api/v2/team/stats`
- [ ] `GetDomainRequest`
  - Current SDK: `GET /api/v2/domains/{domain}/`
  - Spec: `GET /api/v2/domains/{domain_name}`


### D. Query parameter gaps

Add query parameters for implemented operations where the spec defines more than the SDK exposes:

- [ ] `GetInboxMessageRequest`
  - Missing spec query param: `delete`
- [ ] `GetMessageRequest`
  - Already supports `delete`
- [ ] `GetInboxRequest`
  - Already supports spec query params for `listInboxMessages`: `skip`, `limit`, `sort`, `decode_subject`, `cursor`, `full`, `wait`, `delete`
- [ ] New `listDomainMessages` request should support: `inbox`, `skip`, `limit`, `sort`, `decode_subject`, `cursor`, `full`, `wait`, `delete`
- [ ] New stream requests should support: `full`, `limit`, `throttleInterval`, `delete`

### E. Model and response schema gaps

Update or add model classes so mocked tests and SDK hydration match OpenAPI schemas:

- [ ] Add response models for message partial endpoints:
  - `MessageSummaryOnly`
  - `MessageTextOnly`
  - `MessageTextPlainOnly`
  - `MessageTextHtmlOnly`
  - `MessageHeadersOnly`
- [ ] Align TOTP/authenticator responses:
  - Current mock uses `code`; spec uses `passcode`, `time_step`, `futurecodes`, `next_reset_secs`.
  - Current authenticator mock uses mostly `id`; spec uses `passcode`, `time_step`, `id`, `futurecodes`, `next_reset_secs`.
- [ ] Align attachment list response:
  - Current SDK/mock fields include `filename`, `content-type`, `attachment-id`.
  - Spec fields are `id`, `name`, `contentType`, `size`, `downloadUrl`.
- [ ] Align `LinksFull` response:
  - Current mock uses `url`.
  - Spec requires `link` and optional `text`.
- [ ] Align SMTP log response:
  - Current SDK/model expects `smtp_logs`.
  - Spec response key is `log`.
- [ ] Align raw message response:
  - Current SDK/model expects `raw_data`.
  - Spec response key is `data`.
- [ ] Align delete responses:
  - Current mocked tests use `204 No Content`.
  - Spec defines `200` JSON `DeleteResponse` with `status` and optional `count`.
- [ ] Align post message and webhook responses:
  - Current SDK models responses as `PostMessage` or `Webhook`.
  - Spec response schema is `PostMessageResponse` with `status` and `id`.
- [ ] Align team response:
  - Current SDK/model uses `_id`.
  - Spec uses `id`, plus `webhook_tokens`, `plan_data`, `private_domains`, `sms_numbers`, `members`, `plan`, `team_name`, `status`, `token`.
- [ ] Align team stats response:
  - Current mock uses `name` and `count`.
  - Spec uses `date`, `retrieved`, and `sent`.
- [ ] Align team info response:
  - Current mock uses numeric `server_time`.
  - Spec defines `server_time` as a string.
- [ ] Align domain response:
  - Current mock/model includes `_id`, `enabled`, `ownerid`.
  - Spec defines `name`, `description`, `rules`, and `verified`.
- [ ] Align rule payload/model if rules remain supported:
  - Current SDK uses `match_type` and nested `condition_data`.
  - Spec schemas use `match` and flat rule condition fields `operation`, `field`, `value`.


## Sequence

- [ ] Define Python support policy (supported Python versions and test matrix).
- [ ] Add CI quality gates (lint, tests, build, install smoke test).
- [ ] Document Python release mechanics (build, twine, TestPyPI/PyPI workflow, credentials).
- [ ] Add mocked SDK-compatibility tests for the existing public request classes.
- [ ] Add mocked OpenAPI-conformance tests for missing spec operations before implementing them.
- [ ] Add missing message read operations listed in section A:
  - `listDomainMessages`
  - `getMessageSummary`
  - `getMessageText`
  - `getMessageTextPlain`
  - `getMessageTextHtml`
  - `getMessageHeaders`
- [ ] Add missing stream operations listed in section A:
  - `streamDomainMessages`
  - `streamInboxMessages`
- [ ] Add new response models needed only by newly added endpoints.
- [ ] Add non-breaking optional query parameters listed in section D, starting with `delete` on `GetInboxMessageRequest`.
- [ ] Update mocked responses for new endpoints to match OpenAPI schemas.
- [ ] Document newly added request classes and examples in README/EXAMPLE docs.
- [ ] Publish additive OpenAPI functionality as a minor release.
- [ ] Decide compatibility policy for SDK-only endpoints listed in section B.
- [ ] Decide whether to add spec-aligned alternatives for mismatched existing endpoints before changing current classes.
- [ ] Fix URL path inconsistencies listed in section C only after compatibility policy is agreed.
- [ ] Update existing models and mocked responses listed in section E only where changes can remain backward compatible.
- [ ] Document compatibility/migration notes in `CHANGELOG.md` and README for endpoint/deprecation changes.
