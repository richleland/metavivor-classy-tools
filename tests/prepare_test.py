from prepare import format_data


def test_all_keys_present(data_all_fields):
    formatted = format_data(data_all_fields)
    expected = [
        {
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
            "member_email_address": "test@test.com",
            "member_phone": "555-123-4567",
            "offline_payment_info": {
                "check_number": "100",
                "description": "Check donation",
                "payment_type": "check",
                "sync_third_party": True,
            },
            "purchased_at": "2021-01-05T12:00:00-0500",
        }
    ]
    assert formatted == expected


def test_page_ids_are_ints_or_null(data_all_fields, data_no_page_ids):
    formatted = format_data(data_all_fields)[0]
    assert type(formatted["fundraising_page_id"]) == int
    assert type(formatted["fundraising_team_id"]) == int

    formatted = format_data(data_no_page_ids)[0]
    assert formatted["fundraising_page_id"] is None
    assert formatted["fundraising_team_id"] is None
