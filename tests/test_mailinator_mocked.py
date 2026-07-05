from http import HTTPStatus
from unittest.mock import patch
import warnings

import pytest

from mailinator import (
    Action,
    Attachments,
    Condition,
    CreateDomainRequest,
    CreateRuleRequest,
    DeleteDomainMessagesRequest,
    DeleteDomainRequest,
    DeleteInboxMessagesRequest,
    DeleteMessageRequest,
    DeleteRuleRequest,
    DisableRuleRequest,
    Domain,
    Domains,
    EnableRuleRequest,
    GetAuthenticatorByIdRequest,
    GetAuthenticatorRequest,
    GetAuthenticatorsByIdRequest,
    GetAuthenticatorsRequest,
    GetDomainRequest,
    GetDomainsRequest,
    GetInboxMessageAttachmentRequest,
    GetInboxMessageAttachmentsRequest,
    GetInboxMessageLinksRequest,
    GetInboxMessageRawRequest,
    GetInboxMessageRequest,
    GetInboxMessageSmtpLogRequest,
    GetInboxRequest,
    GetLatestInboxMessagesRequest,
    GetLatestMessagesRequest,
    GetMessageAttachmentRequest,
    GetMessageAttachmentsRequest,
    GetMessageLinksFullRequest,
    GetMessageLinksRequest,
    GetMessageRawRequest,
    GetMessageRequest,
    GetMessageSmtpLogRequest,
    GetRuleRequest,
    GetRulesRequest,
    GetSmsInboxRequest,
    GetTeamInfoRequest,
    GetTeamRequest,
    GetTeamStatsRequest,
    Inbox,
    InstantTOTP2FACodeRequest,
    LatestMessages,
    Links,
    LinksFull,
    Mailinator,
    MailinatorException,
    PostMessage,
    PostMessageRequest,
    PrivateCustomServiceInboxWebhookRequest,
    PrivateCustomServiceWebhookRequest,
    PrivateInboxWebhookRequest,
    PrivateWebhookRequest,
    RawData,
    Rule,
    Rules,
    SmtpLogs,
    Stats,
    Team,
    TeamInfo,
    Webhook,
)
from mailinator.base import RequestData, RequestMethod


BASE_URL = "https://api.mailinator.com/api/v2"
TOKEN = "test-token"
DOMAIN = "example.testinator.com"
INBOX = "sdk-inbox"
MESSAGE_ID = "msg-123"
ATTACHMENT_ID = "att-123"
RULE_ID = "rule-123"
AUTH_ID = "auth-123"
AUTH_SECRET = "totp-secret"
WEBHOOK_TOKEN = "wh-token"
CUSTOM_SERVICE = "sms"
PHONE_NUMBER = "15555550123"


class FakeResponse:
    def __init__(self, status_code=HTTPStatus.OK, headers=None, json_data=None, content=b""):
        self.status_code = status_code
        self.headers = headers or {}
        self._json_data = json_data
        self.content = content

    def json(self):
        return self._json_data

    def iter_content(self, chunk_size=1024):
        yield self.content


def json_response(data, status_code=HTTPStatus.OK):
    return FakeResponse(
        status_code=status_code,
        headers={"Content-Type": "application/json"},
        json_data=data,
        content=str(data).encode("utf-8"),
    )


def binary_response(content=b"attachment bytes"):
    return FakeResponse(
        status_code=HTTPStatus.OK,
        headers={"Content-Type": "application/octet-stream"},
        content=content,
    )


MESSAGE_PAYLOAD = {
    "id": MESSAGE_ID,
    "from": "sender@example.com",
    "fromfull": "Sender <sender@example.com>",
    "to": INBOX,
    "subject": "Mocked message",
    "time": 1710000000000,
    "seconds_ago": 3,
    "domain": DOMAIN,
    "origfrom": "sender@example.com",
    "mrid": "mrid-123",
    "size": 42,
    "stream": "public",
    "msgType": "text/plain",
    "source": "SMTP",
    "text": "Hello from a mocked response.",
    "headers": {"x-test": "true"},
    "parts": [{"headers": {"content-type": "text/plain"}, "body": "Hello"}],
}

INBOX_PAYLOAD = {
    "domain": DOMAIN,
    "to": INBOX,
    "cursor": "cursor-123",
    "msgs": [MESSAGE_PAYLOAD],
}

ATTACHMENTS_PAYLOAD = {
    "attachments": [
        {
            "filename": "receipt.txt",
            "content-disposition": "attachment",
            "content-transfer-encoding": "base64",
            "content-type": "text/plain",
            "attachment-id": ATTACHMENT_ID,
        }
    ]
}

RULE_PAYLOAD = {
    "_id": RULE_ID,
    "description": "Mocked rule",
    "enabled": True,
    "match_type": "ANY",
    "name": "mocked-rule",
    "priority": 1,
    "conditions": [
        {
            "operation": "PREFIX",
            "condition_data": {"field": "to", "value": "sdk"},
        }
    ],
    "actions": [
        {
            "action": "DROP",
            "action_data": {"url": "https://example.com/webhook"},
        }
    ],
}

WEBHOOK_PAYLOAD = {
    "from": "Webhook Sender",
    "subject": "Webhook subject",
    "text": "Webhook body",
    "to": INBOX,
}


def build_post_message():
    return PostMessage(_from="sender@example.com", subject="Post subject", text="Post body")


def build_rule():
    conditions = [
        Condition(
            operation=Condition.OperationType.PREFIX,
            field="to",
            value="sdk",
        )
    ]
    actions = [
        Action(
            action=Action.ActionType.DROP,
            action_data=Action.ActionData("https://example.com/webhook"),
        )
    ]
    return Rule(
        description="Mocked rule",
        enabled=True,
        name="mocked-rule",
        conditions=conditions,
        actions=actions,
    )


def build_webhook():
    return Webhook(
        _from="Webhook Sender",
        subject="Webhook subject",
        text="Webhook body",
        to=INBOX,
    )


ENDPOINT_CASES = [
    (
        "instant_totp_2fa_code",
        lambda: InstantTOTP2FACodeRequest(AUTH_SECRET),
        RequestMethod.GET,
        f"{BASE_URL}/totp/{AUTH_SECRET}",
        json_response({"code": "123456"}),
        dict,
    ),
    (
        "get_authenticators",
        GetAuthenticatorsRequest,
        RequestMethod.GET,
        f"{BASE_URL}/authenticators/",
        json_response({"authenticators": [{"id": AUTH_ID}]}),
        dict,
    ),
    (
        "get_authenticators_by_id",
        lambda: GetAuthenticatorsByIdRequest(AUTH_ID),
        RequestMethod.GET,
        f"{BASE_URL}/authenticators/{AUTH_ID}",
        json_response({"id": AUTH_ID}),
        dict,
    ),
    (
        "get_authenticator",
        GetAuthenticatorRequest,
        RequestMethod.GET,
        f"{BASE_URL}/authenticator/",
        json_response({"id": AUTH_ID}),
        dict,
    ),
    (
        "get_authenticator_by_id",
        lambda: GetAuthenticatorByIdRequest(AUTH_ID),
        RequestMethod.GET,
        f"{BASE_URL}/authenticator/{AUTH_ID}",
        json_response({"id": AUTH_ID}),
        dict,
    ),
    (
        "get_inbox",
        lambda: GetInboxRequest(DOMAIN, INBOX),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}?skip=0&limit=50&sort=descending&decode_subject=False",
        json_response(INBOX_PAYLOAD),
        Inbox,
    ),
    (
        "get_inbox_with_query_params",
        lambda: GetInboxRequest(
            DOMAIN,
            INBOX,
            skip=5,
            limit=10,
            sort="ascending",
            decode_subject=True,
            cursor="cursor-123",
            full=True,
            delete="10s",
            wait="5s",
        ),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}?skip=5&limit=10&sort=ascending&decode_subject=True&cursor=cursor-123&full=True&delete=10s&wait=5s",
        json_response(INBOX_PAYLOAD),
        Inbox,
    ),
    (
        "get_inbox_message",
        lambda: GetInboxMessageRequest(DOMAIN, INBOX, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}/messages/{MESSAGE_ID}",
        json_response(MESSAGE_PAYLOAD),
        object,
    ),
    (
        "get_message",
        lambda: GetMessageRequest(DOMAIN, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}",
        json_response(MESSAGE_PAYLOAD),
        object,
    ),
    (
        "get_message_with_delete",
        lambda: GetMessageRequest(DOMAIN, MESSAGE_ID, delete="10s"),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}?delete=10s",
        json_response(MESSAGE_PAYLOAD),
        object,
    ),
    (
        "get_sms_inbox",
        lambda: GetSmsInboxRequest(DOMAIN, PHONE_NUMBER),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{PHONE_NUMBER}",
        json_response(INBOX_PAYLOAD),
        Inbox,
    ),
    (
        "get_inbox_message_attachments",
        lambda: GetInboxMessageAttachmentsRequest(DOMAIN, INBOX, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}/messages/{MESSAGE_ID}/attachments",
        json_response(ATTACHMENTS_PAYLOAD),
        Attachments,
    ),
    (
        "get_message_attachments",
        lambda: GetMessageAttachmentsRequest(DOMAIN, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/attachments",
        json_response(ATTACHMENTS_PAYLOAD),
        Attachments,
    ),
    (
        "get_inbox_message_attachment",
        lambda: GetInboxMessageAttachmentRequest(DOMAIN, INBOX, MESSAGE_ID, ATTACHMENT_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}/messages/{MESSAGE_ID}/attachments/{ATTACHMENT_ID}",
        binary_response(),
        FakeResponse,
    ),
    (
        "get_message_attachment",
        lambda: GetMessageAttachmentRequest(DOMAIN, MESSAGE_ID, ATTACHMENT_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/attachments/{ATTACHMENT_ID}",
        binary_response(),
        FakeResponse,
    ),
    (
        "get_message_links",
        lambda: GetMessageLinksRequest(DOMAIN, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/links",
        json_response({"links": ["https://example.com"]}),
        Links,
    ),
    (
        "get_message_links_full",
        lambda: GetMessageLinksFullRequest(DOMAIN, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/linksfull",
        json_response({"links": [{"url": "https://example.com", "text": "Example"}]}),
        LinksFull,
    ),
    (
        "get_inbox_message_links",
        lambda: GetInboxMessageLinksRequest(DOMAIN, INBOX, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}/messages/{MESSAGE_ID}/links",
        json_response({"links": ["https://example.com"]}),
        Links,
    ),
    (
        "delete_domain_messages",
        lambda: DeleteDomainMessagesRequest(DOMAIN),
        RequestMethod.DELETE,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes",
        FakeResponse(status_code=HTTPStatus.NO_CONTENT),
        FakeResponse,
    ),
    (
        "delete_inbox_messages",
        lambda: DeleteInboxMessagesRequest(DOMAIN, INBOX),
        RequestMethod.DELETE,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}",
        FakeResponse(status_code=HTTPStatus.NO_CONTENT),
        FakeResponse,
    ),
    (
        "delete_message",
        lambda: DeleteMessageRequest(DOMAIN, INBOX, MESSAGE_ID),
        RequestMethod.DELETE,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}/messages/{MESSAGE_ID}",
        FakeResponse(status_code=HTTPStatus.NO_CONTENT),
        FakeResponse,
    ),
    (
        "post_message",
        lambda: PostMessageRequest(DOMAIN, INBOX, build_post_message()),
        RequestMethod.POST,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}",
        json_response({"from": "sender@example.com", "subject": "Post subject", "text": "Post body"}),
        PostMessage,
    ),
    (
        "get_message_smtp_log",
        lambda: GetMessageSmtpLogRequest(DOMAIN, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/smtplog",
        json_response({"smtp_logs": [{"log": "accepted", "time": "now", "event": "delivered"}]}),
        SmtpLogs,
    ),
    (
        "get_inbox_message_smtp_log",
        lambda: GetInboxMessageSmtpLogRequest(DOMAIN, INBOX, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}/messages/{MESSAGE_ID}/smtplog",
        json_response({"smtp_logs": [{"log": "accepted", "time": "now", "event": "delivered"}]}),
        SmtpLogs,
    ),
    (
        "get_message_raw",
        lambda: GetMessageRawRequest(DOMAIN, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/raw",
        json_response({"raw_data": "raw message"}),
        RawData,
    ),
    (
        "get_inbox_message_raw",
        lambda: GetInboxMessageRawRequest(DOMAIN, INBOX, MESSAGE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}/messages/{MESSAGE_ID}/raw",
        json_response({"raw_data": "raw message"}),
        RawData,
    ),
    (
        "get_latest_messages",
        lambda: GetLatestMessagesRequest(DOMAIN),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/messages/*",
        json_response({"to": INBOX, "msgs": [MESSAGE_PAYLOAD]}),
        LatestMessages,
    ),
    (
        "get_latest_inbox_messages",
        lambda: GetLatestInboxMessagesRequest(DOMAIN, INBOX),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/inboxes/{INBOX}/messages/*",
        json_response({"to": INBOX, "msgs": [MESSAGE_PAYLOAD]}),
        LatestMessages,
    ),
    (
        "get_domains",
        GetDomainsRequest,
        RequestMethod.GET,
        f"{BASE_URL}/domains",
        json_response({"domains": [{"_id": DOMAIN, "name": DOMAIN, "enabled": True, "rules": []}]}),
        Domains,
    ),
    (
        "get_domain",
        lambda: GetDomainRequest(DOMAIN),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/",
        json_response({"_id": DOMAIN, "name": DOMAIN, "enabled": True, "rules": []}),
        Domain,
    ),
    (
        "create_domain",
        lambda: CreateDomainRequest(DOMAIN),
        RequestMethod.POST,
        f"{BASE_URL}/domains/{DOMAIN}",
        FakeResponse(status_code=HTTPStatus.NO_CONTENT),
        FakeResponse,
    ),
    (
        "delete_domain",
        lambda: DeleteDomainRequest(DOMAIN),
        RequestMethod.DELETE,
        f"{BASE_URL}/domains/{DOMAIN}",
        FakeResponse(status_code=HTTPStatus.NO_CONTENT),
        FakeResponse,
    ),
    (
        "create_rule",
        lambda: CreateRuleRequest(DOMAIN, build_rule()),
        RequestMethod.POST,
        f"{BASE_URL}/domains/{DOMAIN}/rules/",
        json_response(RULE_PAYLOAD),
        Rule,
    ),
    (
        "enable_rule",
        lambda: EnableRuleRequest(DOMAIN, RULE_ID),
        RequestMethod.PUT,
        f"{BASE_URL}/domains/{DOMAIN}/rules/{RULE_ID}?action=enable",
        FakeResponse(status_code=HTTPStatus.NO_CONTENT),
        FakeResponse,
    ),
    (
        "disable_rule",
        lambda: DisableRuleRequest(DOMAIN, RULE_ID),
        RequestMethod.PUT,
        f"{BASE_URL}/domains/{DOMAIN}/rules/{RULE_ID}?action=disable",
        FakeResponse(status_code=HTTPStatus.NO_CONTENT),
        FakeResponse,
    ),
    (
        "get_rules",
        lambda: GetRulesRequest(DOMAIN),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/rules/",
        json_response({"rules": [RULE_PAYLOAD]}),
        Rules,
    ),
    (
        "get_rule",
        lambda: GetRuleRequest(DOMAIN, RULE_ID),
        RequestMethod.GET,
        f"{BASE_URL}/domains/{DOMAIN}/rules/{RULE_ID}/",
        json_response({"rules": [RULE_PAYLOAD]}),
        Rules,
    ),
    (
        "delete_rule",
        lambda: DeleteRuleRequest(DOMAIN, RULE_ID),
        RequestMethod.DELETE,
        f"{BASE_URL}/domains/{DOMAIN}/rules/{RULE_ID}",
        FakeResponse(status_code=HTTPStatus.NO_CONTENT),
        FakeResponse,
    ),
    (
        "private_webhook",
        lambda: PrivateWebhookRequest(WEBHOOK_TOKEN, build_webhook()),
        RequestMethod.POST,
        f"{BASE_URL}/domains/private/webhook?whtoken={WEBHOOK_TOKEN}",
        json_response(WEBHOOK_PAYLOAD),
        Webhook,
    ),
    (
        "private_inbox_webhook",
        lambda: PrivateInboxWebhookRequest(WEBHOOK_TOKEN, INBOX, build_webhook()),
        RequestMethod.POST,
        f"{BASE_URL}/domains/private/webhook/{INBOX}?whtoken={WEBHOOK_TOKEN}",
        json_response(WEBHOOK_PAYLOAD),
        Webhook,
    ),
    (
        "private_custom_service_webhook",
        lambda: PrivateCustomServiceWebhookRequest(WEBHOOK_TOKEN, CUSTOM_SERVICE, build_webhook()),
        RequestMethod.POST,
        f"{BASE_URL}/domains/private/{CUSTOM_SERVICE}?whtoken={WEBHOOK_TOKEN}",
        json_response(WEBHOOK_PAYLOAD),
        Webhook,
    ),
    (
        "private_custom_service_inbox_webhook",
        lambda: PrivateCustomServiceInboxWebhookRequest(
            WEBHOOK_TOKEN,
            CUSTOM_SERVICE,
            INBOX,
            build_webhook(),
        ),
        RequestMethod.POST,
        f"{BASE_URL}/domains/private/{CUSTOM_SERVICE}/{INBOX}?whtoken={WEBHOOK_TOKEN}",
        json_response(WEBHOOK_PAYLOAD),
        Webhook,
    ),
    (
        "get_team",
        GetTeamRequest,
        RequestMethod.GET,
        f"{BASE_URL}/team",
        json_response(
            {
                "_id": "team-123",
                "team_name": "Mocked Team",
                "plan": "starter",
                "token": TOKEN,
                "status": "active",
                "private_domains": [DOMAIN],
                "sms_numbers": [PHONE_NUMBER],
                "members": [{"email": "member@example.com"}],
            }
        ),
        Team,
    ),
    (
        "get_team_stats",
        GetTeamStatsRequest,
        RequestMethod.GET,
        f"{BASE_URL}/team/stats/",
        json_response({"stats": [{"name": "emails", "count": 1}]}),
        Stats,
    ),
    (
        "get_team_info",
        GetTeamInfoRequest,
        RequestMethod.GET,
        f"{BASE_URL}/teaminfo",
        json_response({"server_time": 1710000000000, "domains": [DOMAIN]}),
        TeamInfo,
    ),
]


REQUEST_PATCH_TARGETS = {
    RequestMethod.GET: "mailinator.mailinator.requests.get",
    RequestMethod.POST: "mailinator.mailinator.requests.post",
    RequestMethod.PUT: "mailinator.mailinator.requests.put",
    RequestMethod.DELETE: "mailinator.mailinator.requests.delete",
}


@pytest.mark.parametrize(
    "name,request_factory,expected_method,expected_url,response,expected_type",
    ENDPOINT_CASES,
    ids=[case[0] for case in ENDPOINT_CASES],
)
def test_all_endpoint_requests_are_dispatched_and_deserialized(
    name,
    request_factory,
    expected_method,
    expected_url,
    response,
    expected_type,
):
    client = Mailinator(TOKEN)

    with patch(REQUEST_PATCH_TARGETS[expected_method], return_value=response) as request_mock:
        with pytest.warns(DeprecationWarning) if is_deprecated_case(name) else does_not_warn():
            request_data = request_factory()
        result = client.request(request_data)

    assert request_data.method == expected_method
    assert request_data.url == expected_url
    assert isinstance(result, expected_type)

    if expected_method == RequestMethod.POST:
        request_mock.assert_called_once_with(
            expected_url,
            json=request_data.json,
            headers=client.headers,
            timeout=125,
        )
    else:
        request_mock.assert_called_once_with(
            expected_url,
            headers=client.headers,
            timeout=125,
        )


def is_deprecated_case(name):
    return name in {
        "create_domain",
        "delete_domain",
        "create_rule",
        "enable_rule",
        "disable_rule",
        "get_rules",
        "get_rule",
        "delete_rule",
        "get_latest_messages",
        "get_latest_inbox_messages",
    }


class does_not_warn:
    def __enter__(self):
        self._warnings = warnings.catch_warnings(record=True)
        self._record = self._warnings.__enter__()
        warnings.simplefilter("always")
        return self._record

    def __exit__(self, exc_type, exc_value, traceback):
        self._warnings.__exit__(exc_type, exc_value, traceback)
        assert not self._record


def test_post_message_request_uses_serialized_json_body():
    request_data = PostMessageRequest(DOMAIN, INBOX, build_post_message())

    assert request_data.json == {
        "_from": "sender@example.com",
        "subject": "Post subject",
        "text": "Post body",
        "from": "sender@example.com",
    }


def test_create_rule_request_uses_serialized_json_body():
    with pytest.warns(DeprecationWarning):
        request_data = CreateRuleRequest(DOMAIN, build_rule())

    assert request_data.json["description"] == "Mocked rule"
    assert request_data.json["conditions"] == [
        {
            "operation": "PREFIX",
            "condition_data": {"field": "to", "value": "sdk"},
        }
    ]
    assert request_data.json["actions"] == [
        {
            "action": "DROP",
            "action_data": {"url": "https://example.com/webhook"},
        }
    ]


def test_webhook_request_uses_serialized_json_body():
    request_data = PrivateWebhookRequest(WEBHOOK_TOKEN, build_webhook())

    assert request_data.json == {
        "_from": "Webhook Sender",
        "subject": "Webhook subject",
        "text": "Webhook body",
        "to": INBOX,
        "from": "Webhook Sender",
    }


def test_client_with_token_sends_authorization_and_user_agent_headers():
    client = Mailinator(TOKEN)

    assert client.headers["Authorization"] == TOKEN
    assert client.headers["User-Agent"].startswith("Mailinator SDK - Python V")


def test_client_without_token_sends_only_user_agent_header():
    client = Mailinator()

    assert "Authorization" not in client.headers
    assert client.headers["User-Agent"].startswith("Mailinator SDK - Python V")


def test_json_response_without_model_returns_dict():
    client = Mailinator(TOKEN)
    request_data = RequestData(RequestMethod.GET, f"{BASE_URL}/mocked")

    with patch("mailinator.mailinator.requests.get", return_value=json_response({"ok": True})):
        result = client.request(request_data)

    assert result == {"ok": True}


def test_non_json_response_returns_response_object():
    client = Mailinator(TOKEN)
    request_data = RequestData(RequestMethod.GET, f"{BASE_URL}/mocked")
    response = binary_response(b"downloaded")

    with patch("mailinator.mailinator.requests.get", return_value=response):
        result = client.request(request_data)

    assert result is response
    assert list(result.iter_content()) == [b"downloaded"]


def test_failed_response_raises_mailinator_exception():
    client = Mailinator(TOKEN)
    request_data = RequestData(RequestMethod.GET, f"{BASE_URL}/mocked")
    response = FakeResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        headers={"Content-Type": "application/json"},
        json_data={"error": "unauthorized"},
        content=b'{"error":"unauthorized"}',
    )

    with patch("mailinator.mailinator.requests.get", return_value=response):
        with pytest.raises(MailinatorException) as exc_info:
            client.request(request_data)

    assert "status code 401" in str(exc_info.value)
    assert "unauthorized" in str(exc_info.value)


def test_unknown_request_method_raises_mailinator_exception():
    client = Mailinator(TOKEN)
    request_data = RequestData("PATCH", f"{BASE_URL}/mocked")

    with pytest.raises(MailinatorException) as exc_info:
        client.request(request_data)

    assert "Method not identified PATCH" in str(exc_info.value)


@pytest.mark.parametrize(
    "request_factory",
    [
        lambda: InstantTOTP2FACodeRequest(None),
        lambda: GetAuthenticatorsByIdRequest(None),
        lambda: GetAuthenticatorByIdRequest(None),
        lambda: GetInboxRequest(None, INBOX),
        lambda: GetInboxRequest(DOMAIN, None),
        lambda: GetInboxMessageRequest(None, INBOX, MESSAGE_ID),
        lambda: GetInboxMessageRequest(DOMAIN, None, MESSAGE_ID),
        lambda: GetInboxMessageRequest(DOMAIN, INBOX, None),
        lambda: GetMessageRequest(None, MESSAGE_ID),
        lambda: GetMessageRequest(DOMAIN, None),
        lambda: GetSmsInboxRequest(None, PHONE_NUMBER),
        lambda: GetSmsInboxRequest(DOMAIN, None),
        lambda: GetInboxMessageAttachmentsRequest(None, INBOX, MESSAGE_ID),
        lambda: GetInboxMessageAttachmentsRequest(DOMAIN, None, MESSAGE_ID),
        lambda: GetInboxMessageAttachmentsRequest(DOMAIN, INBOX, None),
        lambda: GetMessageAttachmentsRequest(None, MESSAGE_ID),
        lambda: GetMessageAttachmentsRequest(DOMAIN, None),
        lambda: GetInboxMessageAttachmentRequest(None, INBOX, MESSAGE_ID, ATTACHMENT_ID),
        lambda: GetInboxMessageAttachmentRequest(DOMAIN, None, MESSAGE_ID, ATTACHMENT_ID),
        lambda: GetInboxMessageAttachmentRequest(DOMAIN, INBOX, None, ATTACHMENT_ID),
        lambda: GetInboxMessageAttachmentRequest(DOMAIN, INBOX, MESSAGE_ID, None),
        lambda: GetMessageAttachmentRequest(None, MESSAGE_ID, ATTACHMENT_ID),
        lambda: GetMessageAttachmentRequest(DOMAIN, None, ATTACHMENT_ID),
        lambda: GetMessageAttachmentRequest(DOMAIN, MESSAGE_ID, None),
        lambda: GetMessageLinksRequest(None, MESSAGE_ID),
        lambda: GetMessageLinksRequest(DOMAIN, None),
        lambda: GetMessageLinksFullRequest(None, MESSAGE_ID),
        lambda: GetMessageLinksFullRequest(DOMAIN, None),
        lambda: GetInboxMessageLinksRequest(None, INBOX, MESSAGE_ID),
        lambda: GetInboxMessageLinksRequest(DOMAIN, None, MESSAGE_ID),
        lambda: GetInboxMessageLinksRequest(DOMAIN, INBOX, None),
        lambda: DeleteDomainMessagesRequest(None),
        lambda: DeleteInboxMessagesRequest(None, INBOX),
        lambda: DeleteInboxMessagesRequest(DOMAIN, None),
        lambda: DeleteMessageRequest(None, INBOX, MESSAGE_ID),
        lambda: DeleteMessageRequest(DOMAIN, None, MESSAGE_ID),
        lambda: DeleteMessageRequest(DOMAIN, INBOX, None),
        lambda: PostMessageRequest(None, INBOX, build_post_message()),
        lambda: PostMessageRequest(DOMAIN, None, build_post_message()),
        lambda: GetMessageSmtpLogRequest(None, MESSAGE_ID),
        lambda: GetMessageSmtpLogRequest(DOMAIN, None),
        lambda: GetInboxMessageSmtpLogRequest(None, INBOX, MESSAGE_ID),
        lambda: GetInboxMessageSmtpLogRequest(DOMAIN, None, MESSAGE_ID),
        lambda: GetInboxMessageSmtpLogRequest(DOMAIN, INBOX, None),
        lambda: GetMessageRawRequest(None, MESSAGE_ID),
        lambda: GetMessageRawRequest(DOMAIN, None),
        lambda: GetInboxMessageRawRequest(None, INBOX, MESSAGE_ID),
        lambda: GetInboxMessageRawRequest(DOMAIN, None, MESSAGE_ID),
        lambda: GetInboxMessageRawRequest(DOMAIN, INBOX, None),
        lambda: GetLatestMessagesRequest(None),
        lambda: GetLatestInboxMessagesRequest(None, INBOX),
        lambda: GetLatestInboxMessagesRequest(DOMAIN, None),
        lambda: GetDomainRequest(None),
        lambda: CreateDomainRequest(None),
        lambda: DeleteDomainRequest(None),
        lambda: CreateRuleRequest(None, build_rule()),
        lambda: EnableRuleRequest(None, RULE_ID),
        lambda: EnableRuleRequest(DOMAIN, None),
        lambda: DisableRuleRequest(None, RULE_ID),
        lambda: DisableRuleRequest(DOMAIN, None),
        lambda: GetRulesRequest(None),
        lambda: GetRuleRequest(None, RULE_ID),
        lambda: GetRuleRequest(DOMAIN, None),
        lambda: DeleteRuleRequest(None, RULE_ID),
        lambda: DeleteRuleRequest(DOMAIN, None),
        lambda: PrivateWebhookRequest(None, build_webhook()),
        lambda: PrivateInboxWebhookRequest(None, INBOX, build_webhook()),
        lambda: PrivateInboxWebhookRequest(WEBHOOK_TOKEN, None, build_webhook()),
        lambda: PrivateCustomServiceWebhookRequest(None, CUSTOM_SERVICE, build_webhook()),
        lambda: PrivateCustomServiceWebhookRequest(WEBHOOK_TOKEN, None, build_webhook()),
        lambda: PrivateCustomServiceInboxWebhookRequest(None, CUSTOM_SERVICE, INBOX, build_webhook()),
        lambda: PrivateCustomServiceInboxWebhookRequest(WEBHOOK_TOKEN, None, INBOX, build_webhook()),
        lambda: PrivateCustomServiceInboxWebhookRequest(WEBHOOK_TOKEN, CUSTOM_SERVICE, None, build_webhook()),
    ],
)
def test_required_parameters_reject_none(request_factory):
    with pytest.raises(ValueError):
        with pytest.warns(DeprecationWarning) if warns_before_value_error(request_factory) else does_not_warn():
            request_factory()


def warns_before_value_error(request_factory):
    deprecated_names = (
        "CreateDomainRequest",
        "DeleteDomainRequest",
        "CreateRuleRequest",
        "EnableRuleRequest",
        "DisableRuleRequest",
        "GetRulesRequest",
        "GetRuleRequest",
        "DeleteRuleRequest",
        "GetLatestMessagesRequest",
        "GetLatestInboxMessagesRequest",
    )
    return any(name in request_factory.__code__.co_names for name in deprecated_names)
