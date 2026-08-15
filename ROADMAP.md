# Roadmap

This roadmap tracks the Python SDK modernization work in strict sequence.

## Python 3.10+ Upgrade

- [x] Raise the minimum supported Python version from 3.9 to 3.10.
  - Updated `python_requires` and the supported-version classifiers in `setup.py`.
  - Verified that the complete pinned dependency set resolves for Python 3.10.
- [x] Upgrade dependencies whose current releases require Python 3.10 or newer.
  Versions adopted as of 2026-08-10:
  - `build`: `1.4.4` to `1.5.0`
  - `importlib-metadata`: `8.7.1` to `9.0.0`
  - `iniconfig`: `2.1.0` to `2.3.0`
  - `jaraco.context`: `6.1.1` to `6.1.2`
  - `jaraco.functools`: `4.4.0` to `4.6.0`
  - `markdown-it-py`: `3.0.0` to `4.2.0`
  - `more-itertools`: `10.8.0` to `11.1.0`
  - `pytest`: `8.4.2` to `9.1.1`
  - `readme-renderer`: `44.0` to `45.0`
  - `requests`: `2.32.5` to `2.34.2`
  - `twine`: `6.2.0` to `7.0.0`
  - `urllib3`: `2.6.3` to `2.7.0`
  - `zipp`: `3.23.1` to `4.1.0`
  - Resolved the complete pinned set together to check transitive compatibility.
- [ ] Add automated testing across every supported Python version (3.10 through 3.13).
  - Run the mocked suite, package build, README rendering, and upload validation in the release workflow.

## OpenAPI Alignment Gap Analysis

Trailing-slash-only differences are intentionally not listed as actionable gaps because the Mailinator API accepts both forms.

### A. In the spec but missing from the SDK

- [ ] `streamDomainMessages`: add `GET /api/v2/domains/{domain}/stream` in `mailinator/message.py` with `full`, `limit`, `throttleInterval`, and `delete`.
- [ ] `streamInboxMessages`: add `GET /api/v2/domains/{domain}/stream/{inbox}` in `mailinator/message.py` with `full`, `limit`, `throttleInterval`, and `delete`.

### B. In the SDK but not in the spec

- [ ] Decide compatibility policy for custom-service webhook endpoints: `PrivateCustomServiceWebhookRequest` and `PrivateCustomServiceInboxWebhookRequest`.

### C. URL path mismatches

- [ ] `PostMessageRequest`: decide how to handle SDK path `POST /api/v2/domains/{domain}/inboxes/{inbox}` vs spec path `POST /api/v2/domains/{domain}/inboxes/{inbox}/messages`.
- [ ] `PrivateWebhookRequest`: decide how to handle SDK path `POST /api/v2/domains/private/webhook?whtoken=...` vs spec path `POST /api/v2/domains/{domain}/webhook?whtoken=...`.
- [ ] `PrivateInboxWebhookRequest`: decide how to handle SDK path `POST /api/v2/domains/private/webhook/{inbox}?whtoken=...` vs spec path `POST /api/v2/domains/{domain}/webhook/{inbox}?whtoken=...`.

### D. Query parameter gaps

- [ ] `GetInboxMessageRequest`: add optional `delete` query parameter without changing default behavior.
- [ ] Stream requests: support `full`, `limit`, `throttleInterval`, and `delete`.

### E. Model and response schema gaps

- [ ] Align TOTP and authenticator responses with spec fields: `passcode`, `time_step`, `futurecodes`, `next_reset_secs`, and `id` where applicable.
- [ ] Align attachment list response with spec fields: `id`, `name`, `contentType`, `size`, and `downloadUrl`.
- [ ] Align `LinksFull` response with spec field `link` instead of mock field `url`.
- [ ] Align SMTP log response with spec key `log` instead of SDK/model key `smtp_logs`.
- [ ] Align raw message response with spec key `data` instead of SDK/model key `raw_data`.
- [ ] Align delete responses with spec `200` JSON `DeleteResponse` containing `status` and optional `count`.
- [ ] Align post message and webhook responses with spec `PostMessageResponse` containing `status` and `id`.
- [ ] Align team response with spec fields including `id`, `webhook_tokens`, `plan_data`, `private_domains`, `sms_numbers`, `members`, `plan`, `team_name`, `status`, and `token`.
- [ ] Align team stats response with spec fields `date`, `retrieved`, and `sent`.
- [ ] Align team info response with spec string `server_time`.
- [ ] Align domain response with spec fields `name`, `description`, `rules`, and `verified`.
- [ ] Align rule payload/model if rules remain supported, reconciling SDK `match_type` and `condition_data` with spec `match`, `operation`, `field`, and `value`.
