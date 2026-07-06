# Roadmap

This roadmap tracks the Python SDK modernization work in strict sequence.

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
