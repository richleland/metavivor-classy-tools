import pandas as pd


df = pd.read_csv("input/checks-2021-03-07.csv", dtype=str)

formatted = pd.DataFrame(
    [],
    columns=[
        "purchased_at",
        "fundraising_team_id",
        "fundraising_page_id",
        "comment",
        "billing_first_name",
        "billing_last_name",
        "billing_address1",
        "billing_address2",
        "billing_city",
        "billing_state",
        "billing_postal_code",
        "billing_country",
        "member_email_address",
        "company_name",
        "price",
        "check_number",
    ],
    dtype=str,
)

# transaction metadata
formatted["fundraising_team_id"] = df["Team Page ID"]
formatted["fundraising_page_id"] = df["Individual Page ID"]
formatted["comment"] = df["special handling"]
formatted["purchased_at"] = df["Transaction Date"]
formatted["purchased_at"] = pd.to_datetime(formatted["purchased_at"])
formatted["purchased_at"] = formatted["purchased_at"].dt.strftime("%Y-%m-%dT12:00:00-0500")

# contact information
formatted["billing_first_name"] = df["Donor First Name"]
formatted["billing_last_name"] = df["Donor Last Name"]
formatted["billing_address1"] = df["Billing Address 1"]
formatted["billing_address2"] = df["Billing Address 2"]
formatted["billing_city"] = df["Billing City"]
formatted["billing_state"] = df["Billing State"]
formatted["billing_postal_code"] = df["Billing Postal Code"]
formatted["billing_country"] = df["Billing Country"]
formatted["member_email_address"] = df["Billing Email Address"]
formatted["member_phone"] = df["donor phone"]
formatted["company_name"] = df["Company Name"]

# payment info
formatted["price"] = df["Gross Transaction Amount"]
formatted["price"] = formatted["price"].astype(float)
formatted["check_number"] = df["check number"]

formatted.to_json("output/checks-2021-03-07.json", orient="records", indent=2)
