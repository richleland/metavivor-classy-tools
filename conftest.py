import pytest


@pytest.fixture
def data_all_fields():
    return [
        {
            "Transaction Date": "01/05/21",
            "Payment Type": "check",
            "check number": "100",
            "Gross Transaction Amount": "1",
            "Company Name": "Test Company",
            "Donor First Name": "Alex",
            "Donor Last Name": "Jones",
            "Billing Address 1": "123 Anywhere Drive",
            "Billing Address 2": "#13",
            "Billing City": "Somewhere",
            "Billing State": "MD",
            "Billing Postal Code": "12345",
            "Billing Country": "US",
            "Billing Email Address": "alex@test.com",
            "Dedication Type": "in memory of",
            "Dedication Name": "Sam Jones",
            "Dedication Contact Name": "Pat Jones",
            "Dedication Contact Address": "444 Another Rd",
            "Dedication Contact City": "Small Town",
            "Dedication Contact State": "AZ",
            "Dedication Contact Postal Code": "12345",
            "Dedication Contact Country": "US",
            "Dedication Contact Email": "pat@test.com",
            "Dedication Message": "Always here for you",
            "donor phone": "555-123-4567",
            "special handling": "internal note",
            "QBO account or fundraiser": "donation",
            "Campaign ID": "111111",
            "Team Page ID": "4444444",
            "Individual Page ID": "8888888",
        }
    ]


@pytest.fixture
def data_no_page_ids():
    return [
        {
            "Transaction Date": "01/05/21",
            "Payment Type": "check",
            "check number": "100",
            "Gross Transaction Amount": "1",
            "Company Name": "Test Company",
            "Donor First Name": "Alex",
            "Donor Last Name": "Jones",
            "Billing Address 1": "123 Anywhere Drive",
            "Billing Address 2": "#13",
            "Billing City": "Somewhere",
            "Billing State": "MD",
            "Billing Postal Code": "12345",
            "Billing Country": "US",
            "Billing Email Address": "alex@test.com",
            "Dedication Type": "in memory of",
            "Dedication Name": "Sam Jones",
            "Dedication Contact Name": "Pat Jones",
            "Dedication Contact Address": "444 Another Rd",
            "Dedication Contact City": "Small Town",
            "Dedication Contact State": "AZ",
            "Dedication Contact Postal Code": "12345",
            "Dedication Contact Country": "US",
            "Dedication Contact Email": "pat@test.com",
            "Dedication Message": "Always here for you",
            "donor phone": "555-123-4567",
            "special handling": "testing",
            "QBO account or fundraiser": "donation",
            "Campaign ID": "111111",
            "Team Page ID": "",
            "Individual Page ID": "",
        }
    ]


@pytest.fixture
def data_no_email():
    return [
        {
            "Transaction Date": "01/05/21",
            "Payment Type": "check",
            "check number": "100",
            "Gross Transaction Amount": "1",
            "Company Name": "Test Company",
            "Donor First Name": "Alex",
            "Donor Last Name": "Jones",
            "Billing Address 1": "123 Anywhere Drive",
            "Billing Address 2": "#13",
            "Billing City": "Somewhere",
            "Billing State": "MD",
            "Billing Postal Code": "12345",
            "Billing Country": "US",
            "Billing Email Address": "",
            "Dedication Type": "",
            "Dedication Name": "",
            "Dedication Contact Name": "",
            "Dedication Contact Address": "",
            "Dedication Contact City": "",
            "Dedication Contact State": "",
            "Dedication Contact Postal Code": "",
            "Dedication Contact Country": "",
            "Dedication Contact Email": "",
            "Dedication Message": "",
            "donor phone": "",
            "special handling": "testing",
            "QBO account or fundraiser": "donation",
            "Campaign ID": "111111",
            "Team Page ID": "",
            "Individual Page ID": "",
        }
    ]
