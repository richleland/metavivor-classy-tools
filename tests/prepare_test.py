import pytest

from config import DEFAULT_CAMPAIGN_ID
from prepare import format_data, format_type


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param("IN MEMORY OF", "memory", id="to lowercase"),
        pytest.param("In Memory Of", "memory", id="to mixed case"),
        pytest.param("   in honor of   ", "honor", id="remove leading and trailing spaces"),
        pytest.param("in memory of", "memory", id="memory proper format"),
        pytest.param("in honor of", "honor", id="honor proper format"),
        pytest.param("nonsense", None, id="unmatched"),
    ],
)
def test_format_type(test_input, expected):
    result = format_type(test_input)
    assert result == expected


def test_all_keys_present(data_all_fields):
    formatted = format_data(data_all_fields)
    expected = [
        {
            "campaign_id": 111111,
            "transaction": {
                "billing_first_name": "Alex",
                "billing_last_name": "Jones",
                "billing_address1": "123 Anywhere Drive",
                "billing_address2": "#13",
                "billing_city": "Somewhere",
                "billing_state": "MD",
                "billing_postal_code": "12345",
                "billing_country": "US",
                "company_name": "Test Company",
                "comment": "testing",
                "fundraising_page_id": 8888888,
                "fundraising_team_id": 4444444,
                "items": [
                    {
                        "overhead_amount": 0,
                        "price": 1.0,
                        "product_id": None,
                        "product_name": "Offline Donation",
                        "quantity": 1,
                        "type": "donation",
                    }
                ],
                "member_name": "Alex Jones",
                "member_email_address": "alex@test.com",
                "member_phone": "555-123-4567",
                "metadata": {"script": True},
                "offline_payment_info": {
                    "check_number": "100",
                    "description": "Check donation",
                    "payment_type": "check",
                    "sync_third_party": True,
                },
                "purchased_at": "2021-01-05T12:00:00-0500",
            },
            "dedication": {
                "address": "444 Another Rd",
                "city": "Small Town",
                "country": "US",
                "ecard_message": "Always here for you",
                "email_address": "pat@test.com",
                "honoree_name": "Sam Jones",
                "name": "Pat Jones",
                "postal_code": "12345",
                "state": "AZ",
                "type": "memory",
            },
        },
    ]
    assert formatted == expected


def test_page_ids_are_ints_or_null(data_all_fields, data_no_page_ids):
    formatted = format_data(data_all_fields)[0]
    assert type(formatted["transaction"]["fundraising_page_id"]) == int
    assert type(formatted["transaction"]["fundraising_team_id"]) == int

    formatted = format_data(data_no_page_ids)[0]
    assert formatted["transaction"]["fundraising_page_id"] is None
    assert formatted["transaction"]["fundraising_team_id"] is None


def test_empty_when_name_and_company_missing(data_all_fields):
    data_all_fields[0]["Donor First Name"] = ""
    data_all_fields[0]["Donor Last Name"] = ""
    data_all_fields[0]["Company Name"] = ""
    formatted = format_data(data_all_fields)
    assert len(formatted) == 0


@pytest.mark.parametrize(
    "first_name, last_name, company_name, expected",
    [
        pytest.param("Erin", "O'Neill", "", "offline+erinoneill@metavivor.org", id="name with apostrophe"),
        pytest.param("Rich", "☘️", "", "offline+rich@metavivor.org", id="name with emoji"),
        pytest.param("", "", "Company+ 123!", "offline+company123@metavivor.org", id="company with symbols"),
    ],
)
def test_only_alphanumeric_values_in_email(first_name, last_name, company_name, expected, data_no_email):
    data_no_email[0]["Donor First Name"] = first_name
    data_no_email[0]["Donor Last Name"] = last_name
    data_no_email[0]["Company Name"] = company_name
    formatted = format_data(data_no_email)[0]
    assert formatted["transaction"]["member_email_address"] == expected


def test_email_falls_back_to_billing_name(data_no_email):
    expected = "offline+alexjones@metavivor.org"
    formatted = format_data(data_no_email)[0]
    assert formatted["transaction"]["member_email_address"] == expected


def test_email_falls_back_to_company_name(data_no_email):
    data_no_email[0]["Donor First Name"] = ""
    data_no_email[0]["Donor Last Name"] = ""
    expected = "offline+testcompany@metavivor.org"
    formatted = format_data(data_no_email)[0]
    assert formatted["transaction"]["member_email_address"] == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param("111111", 111111, id="use campaign ID as-is"),
        pytest.param("", DEFAULT_CAMPAIGN_ID, id="fall back to default campaign ID"),
    ],
)
def test_campaign_id(test_input, expected, data_all_fields):
    data_all_fields[0]["Campaign ID"] = test_input
    formatted = format_data(data_all_fields)[0]
    assert formatted["campaign_id"] == expected
