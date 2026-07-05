from http import HTTPStatus
from unittest.mock import patch

import pytest

import mailinator
from mailinator import Mailinator
from mailinator.base import RequestMethod


BASE_URL = "https://api.mailinator.com/api/v2"
TOKEN = "test-token"
DOMAIN = "example.testinator.com"
INBOX = "sdk-inbox"
MESSAGE_ID = "msg-123"


class FakeResponse:
    def __init__(self, status_code=HTTPStatus.OK, headers=None, json_data=None, content=b""):
        self.status_code = status_code
        self.headers = headers or {}
        self._json_data = json_data
        self.content = content

    def json(self):
        return self._json_data


def json_response(data, status_code=HTTPStatus.OK):
    return FakeResponse(
        status_code=status_code,
        headers={"Content-Type": "application/json"},
        json_data=data,
        content=str(data).encode("utf-8"),
    )


MESSAGE_SUMMARY_PAYLOAD = {
    "id": MESSAGE_ID,
    "subject": "Mocked message",
    "domain": DOMAIN,
    "from": "Sender",
    "origfrom": "Sender <sender@example.com>",
    "to": INBOX,
    "time": 1710000000000,
    "seconds_ago": 721029,
    "source": "EMAIL",
}

INBOX_MESSAGES_PAYLOAD = {
    "domain": "private",
    "to": "*",
    "msgs": [MESSAGE_SUMMARY_PAYLOAD],
    "cursor": "cursor-123",
}

MESSAGE_SUMMARY_ONLY_PAYLOAD = {
    "summary": {
        "subject": "Mocked message",
        "domain": "public",
        "from": "sender@example.com",
        "id": MESSAGE_ID,
        "to": INBOX,
        "time": 1710000000000,
    }
}

MESSAGE_TEXT_ONLY_PAYLOAD = {
    "text": "Extracted real text from the mocked message. [link](https://example.com)",
}

MESSAGE_TEXT_PLAIN_ONLY_PAYLOAD = {
    "text/plain": "Plain text body from the mocked message.r\n\r\n[link](https://example.com)",
}

MESSAGE_TEXT_HTML_ONLY_PAYLOAD = {
    "text/html": "<head>\r\n<title>\r\n</title>\r\n<!--[if !mso]><!-->\r\n<meta content=\"IE=edge\" http-equiv=\"X-UA-Compatible\">\r\n<!--<![endif]-->\r\n<meta content=\"text/html; charset=utf-8\" http-equiv=\"Content-Type\">\r\n<meta content=\"width=device-width, initial-scale=1\" name=\"viewport\">\r\n<!--[if mso]>\r\n        <noscript>\r\n        <xml>\r\n        <o:OfficeDocumentSettings>\r\n          <o:AllowPNG/>\r\n          <o:PixelsPerInch>96</o:PixelsPerInch>\r\n        </o:OfficeDocumentSettings>\r\n        </xml>\r\n        </noscript>\r\n        <![endif]-->\r\n<!--[if lte mso 11]>\r\n        <style type=\"text/css\" data-inliner=\"ignore\">\r\n          .mj-outlook-group-fix { width:100% !important; }\r\n        </style>\r\n        <![endif]-->\r\n<!--[if !mso]><!--><!--<![endif]-->\r\n<style>a:not([name]) {color:#15c;text-decoration:underline}\r\na:link {color:#15c;text-decoration:underline}\r\na:visited {color:#15c;text-decoration:underline}\r\na:active {color:#15c;text-decoration:underline}\r\na:hover {color:#15c;text-decoration:underline}</style><style>@import url(https://static-forms.klaviyo.com/fonts/api/v1/N8GZZz/custom_fonts.css);\r\n#outlook a {\r\n    padding: 0\r\n    }\r\nbody {\r\n    margin: 0;\r\n    padding: 0;\r\n    -webkit-text-size-adjust: 100%;\r\n    -ms-text-size-adjust: 100%\r\n    }\r\ntable, td {\r\n    border-collapse: collapse;\r\n    mso-table-lspace: 0;\r\n    mso-table-rspace: 0\r\n    }\r\nimg {\r\n    border: 0;\r\n    line-height: 100%;\r\n    outline: none;\r\n    text-decoration: none;\r\n    -ms-interpolation-mode: bicubic\r\n    }\r\np {\r\n    display: block;\r\n    margin: 13px 0\r\n    }\r\n@media only screen and (min-width: 480px) {\r\n    .mj-column-per-100 {\r\n        width: 100% !important;\r\n        max-width: 100%\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    div.kl-row.colstack div.kl-column {\r\n        display: block !important;\r\n        width: 100% !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    .component-wrapper .mob-no-spc {\r\n        padding-left: 0 !important;\r\n        padding-right: 0 !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    td.kl-img-base-auto-width {\r\n        width: 100% !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    .kl-table-subblock.use-legacy-mobile-padding {\r\n        padding-left: 9px !important;\r\n        padding-right: 9px !important\r\n        }\r\n    }\r\n@media screen and (max-width: 480px) {\r\n    .kl-sl-stk {\r\n        display: block !important;\r\n        width: 100% !important;\r\n        padding: 0 0 9px !important;\r\n        text-align: center !important\r\n        }\r\n    .kl-sl-stk.lbls {\r\n        padding: 0 !important\r\n        }\r\n    .kl-sl-stk.spcblk {\r\n        display: none !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    td.mobile-only {\r\n        display: table-cell !important\r\n        }\r\n    div.mobile-only {\r\n        display: block !important\r\n        }\r\n    table.mobile-only {\r\n        display: table !important\r\n        }\r\n    .desktop-only {\r\n        display: none !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    .table-mobile-only {\r\n        display: table-cell !important;\r\n        max-height: none !important\r\n        }\r\n    .table-mobile-only.block {\r\n        display: block !important\r\n        }\r\n    .table-mobile-only.inline-block {\r\n        display: inline-block !important\r\n        }\r\n    .table-desktop-only {\r\n        max-height: 0 !important;\r\n        display: none !important;\r\n        mso-hide: all !important;\r\n        overflow: hidden !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    body.mce-content-body, /* NOTE: needed for internal tinymce styles */.kl-text > div, .kl-table-subblock > div, .kl-split-subblock > div {\r\n        font-size: 14px !important;\r\n        line-height: 1.3 !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    h1 {\r\n        font-size: 40px !important;\r\n        line-height: 1.1 !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    h2 {\r\n        font-size: 32px !important;\r\n        line-height: 1.1 !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    h3 {\r\n        font-size: 24px !important;\r\n        line-height: 1.1 !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    h4 {\r\n        font-size: 18px !important;\r\n        line-height: 1.1 !important\r\n        }\r\n    }\r\n@media only screen and (max-width: 480px) {\r\n    .root-container {\r\n        width: 100% !important\r\n        }\r\n    .root-container-spacing {\r\n        padding: 0 !important\r\n        }\r\n    .content-padding {\r\n        padding-left: 0 !important;\r\n        padding-right: 0 !important\r\n        }\r\n    .content-padding.kl-first {\r\n        padding-top: 0 !important\r\n        }\r\n    .content-padding.kl-last {\r\n        padding-bottom: 0 !important\r\n        }\r\n    .kl-column > .component-wrapper {\r\n        padding-left: 0 !important;\r\n        padding-right: 0 !important;\r\n        width: unset !important\r\n        }\r\n    .kl-text {\r\n        padding-right: 18px !important;\r\n        padding-left: 18px !important\r\n        }\r\n    }</style></head>",
}

MESSAGE_HEADERS_ONLY_PAYLOAD = {
    "headers": {
        "mime-version": "1.0",
        "date": "Mon, 01 Jan 2024 00:00:00 +0000",
        "message-id": "<mocked-message@example.com>",
        "from": "sender@example.com",
        "to": f"{INBOX}@{DOMAIN}",
        "subject": "Mocked message",
        "content-type": "text/plain; charset=utf-8",
        "received": ["from mail.example.com by mailinator.com"],
        "dkim-signature": "v=1; a=rsa-sha256; c=relaxed/relaxed; d=mailinator.com; s=mailinator; h=from:to:subject:date:message-id; bh=abc123; b=def456",
    }
}


def request_class(name):
    try:
        return getattr(mailinator, name)
    except AttributeError:
        pytest.fail(f"Expected SDK request class {name} to be implemented")


def model_class(name):
    try:
        return getattr(mailinator, name)
    except AttributeError:
        pytest.fail(f"Expected SDK response model {name} to be implemented")


NEW_ENDPOINT_CASES = [
    (
        "list_domain_messages_default_params",
        lambda: request_class("ListDomainMessagesRequest")(DOMAIN),
        f"{BASE_URL}/domains/{DOMAIN}/inboxes?inbox=*&skip=0&limit=50&sort=descending&decode_subject=False",
        json_response(INBOX_MESSAGES_PAYLOAD),
        lambda: model_class("Inbox"),
    ),
    (
        "list_domain_messages_all_query_params",
        lambda: request_class("ListDomainMessagesRequest")(
            DOMAIN,
            inbox=INBOX,
            skip=5,
            limit=10,
            sort="ascending",
            decode_subject=True,
            cursor="cursor-123",
            full=True,
            wait="5s",
            delete="10s",
        ),
        f"{BASE_URL}/domains/{DOMAIN}/inboxes?inbox={INBOX}&skip=5&limit=10&sort=ascending&decode_subject=True&cursor=cursor-123&full=True&wait=5s&delete=10s",
        json_response(INBOX_MESSAGES_PAYLOAD),
        lambda: model_class("Inbox"),
    ),
    (
        "get_message_summary",
        lambda: request_class("GetMessageSummaryRequest")(DOMAIN, MESSAGE_ID),
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/summary",
        json_response(MESSAGE_SUMMARY_ONLY_PAYLOAD),
        lambda: model_class("MessageSummary"),
    ),
    (
        "get_message_text",
        lambda: request_class("GetMessageTextRequest")(DOMAIN, MESSAGE_ID),
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/text",
        json_response(MESSAGE_TEXT_ONLY_PAYLOAD),
        lambda: model_class("MessageText"),
    ),
    (
        "get_message_text_plain",
        lambda: request_class("GetMessageTextPlainRequest")(DOMAIN, MESSAGE_ID),
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/textplain",
        json_response(MESSAGE_TEXT_PLAIN_ONLY_PAYLOAD),
        lambda: model_class("MessageTextPlain"),
    ),
    (
        "get_message_text_html",
        lambda: request_class("GetMessageTextHtmlRequest")(DOMAIN, MESSAGE_ID),
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/texthtml",
        json_response(MESSAGE_TEXT_HTML_ONLY_PAYLOAD),
        lambda: model_class("MessageTextHtml"),
    ),
    (
        "get_message_headers",
        lambda: request_class("GetMessageHeadersRequest")(DOMAIN, MESSAGE_ID),
        f"{BASE_URL}/domains/{DOMAIN}/messages/{MESSAGE_ID}/headers",
        json_response(MESSAGE_HEADERS_ONLY_PAYLOAD),
        lambda: model_class("MessageHeaders"),
    ),
    (
        "stream_domain_messages_default_params",
        lambda: request_class("StreamDomainMessagesRequest")(DOMAIN),
        f"{BASE_URL}/domains/{DOMAIN}/stream?limit=50",
        json_response(MESSAGE_SUMMARY_PAYLOAD),
        lambda: model_class("Message"),
    ),
    (
        "stream_domain_messages_all_query_params",
        lambda: request_class("StreamDomainMessagesRequest")(
            DOMAIN,
            full=True,
            limit=10,
            throttleInterval="5s",
            delete="10s",
        ),
        f"{BASE_URL}/domains/{DOMAIN}/stream?full=True&limit=10&throttleInterval=5s&delete=10s",
        json_response(MESSAGE_SUMMARY_PAYLOAD),
        lambda: model_class("Message"),
    ),
    (
        "stream_inbox_messages_default_params",
        lambda: request_class("StreamInboxMessagesRequest")(DOMAIN, INBOX),
        f"{BASE_URL}/domains/{DOMAIN}/stream/{INBOX}?limit=50",
        json_response(MESSAGE_SUMMARY_PAYLOAD),
        lambda: model_class("Message"),
    ),
    (
        "stream_inbox_messages_all_query_params",
        lambda: request_class("StreamInboxMessagesRequest")(
            DOMAIN,
            INBOX,
            full=True,
            limit=10,
            throttleInterval="5s",
            delete="10s",
        ),
        f"{BASE_URL}/domains/{DOMAIN}/stream/{INBOX}?full=True&limit=10&throttleInterval=5s&delete=10s",
        json_response(MESSAGE_SUMMARY_PAYLOAD),
        lambda: model_class("Message"),
    ),
]


@pytest.mark.parametrize(
    "name,request_factory,expected_url,response,expected_model_factory",
    NEW_ENDPOINT_CASES,
    ids=[case[0] for case in NEW_ENDPOINT_CASES],
)
def test_new_message_endpoint_requests_are_dispatched_and_deserialized(
    name,
    request_factory,
    expected_url,
    response,
    expected_model_factory,
):
    client = Mailinator(TOKEN)

    with patch("mailinator.mailinator.requests.get", return_value=response) as request_mock:
        request_data = request_factory()
        result = client.request(request_data)

    assert request_data.method == RequestMethod.GET
    assert request_data.url == expected_url
    assert isinstance(result, expected_model_factory())
    request_mock.assert_called_once_with(
        expected_url,
        headers=client.headers,
        timeout=125,
    )


@pytest.mark.parametrize(
    "request_factory",
    [
        lambda: request_class("ListDomainMessagesRequest")(None),
        lambda: request_class("GetMessageSummaryRequest")(None, MESSAGE_ID),
        lambda: request_class("GetMessageSummaryRequest")(DOMAIN, None),
        lambda: request_class("GetMessageTextRequest")(None, MESSAGE_ID),
        lambda: request_class("GetMessageTextRequest")(DOMAIN, None),
        lambda: request_class("GetMessageTextPlainRequest")(None, MESSAGE_ID),
        lambda: request_class("GetMessageTextPlainRequest")(DOMAIN, None),
        lambda: request_class("GetMessageTextHtmlRequest")(None, MESSAGE_ID),
        lambda: request_class("GetMessageTextHtmlRequest")(DOMAIN, None),
        lambda: request_class("GetMessageHeadersRequest")(None, MESSAGE_ID),
        lambda: request_class("GetMessageHeadersRequest")(DOMAIN, None),
        lambda: request_class("StreamDomainMessagesRequest")(None),
        lambda: request_class("StreamInboxMessagesRequest")(None, INBOX),
        lambda: request_class("StreamInboxMessagesRequest")(DOMAIN, None),
    ],
)
def test_new_message_endpoint_requests_reject_required_none_parameters(request_factory):
    with pytest.raises(ValueError):
        request_factory()
