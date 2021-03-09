from datetime import datetime


def format_type(dedication_type):
    """
    Formats the dedication type for Classy

    Classy expected the dedication type to be either 'memory' or 'honor'. Here we
    convert the value to lowercase, trim any leading or trailing whitespace, and convert
    the value to what Classy expects. We fall back to a None value for unmatched input.
    """
    dedication_type = dedication_type.lower().strip()
    if dedication_type == "in memory of":
        return "memory"
    elif dedication_type == "in honor of":
        return "honor"
    return None


def format_data(input_data):
    """
    Formats the input data in preparation for Classy API calls

    We take the input data, which is expected to be an instance of csv.DictReader, and
    create a list of dicts, each having two keys - transaction and dedication. These are
    separate keys because we need to first create the transaction, then create the
    dedication via the Classy API.
    """
    formatted = []
    for row in input_data:
        transaction = {
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
            transaction["fundraising_page_id"] = int(row["Individual Page ID"])

        if row["Team Page ID"]:
            transaction["fundraising_team_id"] = int(row["Team Page ID"])

        dedication = {}
        if row["Dedication Type"] and row["Dedication Name"]:
            dedication = {
                "type": format_type(row["Dedication Type"]),
                "honoree_name": row["Dedication Name"],
                "name": row["Dedication Contact Name"] or None,
                "address": row["Dedication Contact Address"] or None,
                "city": row["Dedication Contact City"] or None,
                "state": row["Dedication Contact State"] or None,
                "postal_code": row["Dedication Contact Postal Code"] or None,
                "country": row["Dedication Contact Country"] or None,
                "email_address": row["Dedication Contact Email"] or None,
                "ecard_message": row["Dedication Message"] or None,
            }

        formatted.append(
            {
                "transaction": transaction,
                "dedication": dedication,
            }
        )
    return formatted
