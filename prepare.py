import csv
import json
from datetime import datetime


def format_data(input_data):
    formatted = []
    for row in input_data:
        converted = {
            "billing_first_name": row["Donor First Name"] or None,
            "billing_last_name": row["Donor Last Name"] or None,
            "billing_address1": row["Billing Address 1"] or None,
            "billing_address2": row["Billing Address 2"] or None,
            "billing_city": row["Billing City"] or None,
            "billing_state": row["Billing State"] or None,
            "billing_postal_code": row["Billing Postal Code"] or None,
            "billing_country": row["Billing Country"] or None,
            "company_name": row["Company Name"] or None,
            "comment": row["special handling"] or None,
            "fundraising_page_id": None,
            "fundraising_team_id": None,
            "items": [
                {
                    "overhead_amount": 0,
                    "price": float(row["Gross Transaction Amount"]),
                    "product_id": None,
                    "product_name": "Offline Donation",
                    "quantity": 1,
                    "type": "donation",
                }
            ],
            "member_email_address": row["Billing Email Address"] or None,
            "member_phone": row["donor phone"] or None,
            "offline_payment_info": {
                "check_number": row["check number"],
                "description": "Check donation",
                "payment_type": "check",
                "sync_third_party": True,
            },
            "purchased_at": datetime.strptime(row["Transaction Date"], "%m/%d/%y").strftime("%Y-%m-%dT12:00:00-0500"),
        }

        if row["Individual Page ID"]:
            converted["fundraising_page_id"] = int(row["Individual Page ID"])

        if row["Team Page ID"]:
            converted["fundraising_team_id"] = int(row["Team Page ID"])

        formatted.append(converted)
    return formatted


if __name__ == "__main__":
    with open("input/checks-2021-03-07.csv") as csvfile:
        csv_data = csv.DictReader(csvfile)
        formatted = format_data(csv_data)

    with open("output/checks-2021-03-07.json", "w") as f:
        json.dump(formatted, f, indent=2)
