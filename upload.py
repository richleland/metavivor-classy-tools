# import json
import os

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

CLIENT_ID = os.environ["CLASSY_CLIENT_ID"]
CLIENT_SECRET = os.environ["CLASSY_CLIENT_SECRET"]
ORG_ID = os.environ["CLASSY_ORG_ID"]
TOKEN_URL = "https://api.classy.org/oauth2/auth"
API_URL = "https://api.classy.org/2.0"

client = BackendApplicationClient(client_id=CLIENT_ID)
session = OAuth2Session(client=client)
token = session.fetch_token(
    token_url=TOKEN_URL,
    client_secret=CLIENT_SECRET,
    client_id=CLIENT_ID,
    include_client_id=True,
)


def get_campaigns_from_api(org_id, url=None):
    if not url:
        url = f"{API_URL}/organizations/{org_id}/campaigns"

    response = session.get(url)
    response.raise_for_status()
    response_json = response.json()

    # append the current page's data
    campaigns = response_json["data"]

    # see if there's a next page
    next_page_url = response_json["next_page_url"]
    if next_page_url:
        campaigns = campaigns + get_campaigns_from_api(org_id, next_page_url)

    # return the campaigns from all pages
    return campaigns


def get_teams_from_api(campaign_id, url=None):
    if not url:
        url = f"{API_URL}/campaigns/{campaign_id}/fundraising-teams"

    response = session.get(url)
    response.raise_for_status()
    response_json = response.json()

    # append the current page's data
    teams = response_json["data"]

    # see if there's a next page
    next_page_url = response_json["next_page_url"]
    if next_page_url:
        teams = teams + get_teams_from_api(campaign_id, next_page_url)

    # return the teams from all pages
    return teams


# # get a transaction
# response = session.get(f"{API_URL}/transactions/42112117/items")
# response.raise_for_status()
# with open("output/response-get-transaction.json", "w") as f:
#     json.dump(response.json(), f, indent=2)

# # get fundraising pages
# response = session.get(f"{API_URL}/campaigns/319115/fundraising-pages")
# response.raise_for_status()
# with open("output/response-fundraising-pages.json", "w") as f:
#     json.dump(response.json(), f, indent=2)

# # create an offline transaction
# with open("input/test-transaction.json") as f:
#     payload = json.load(f)
# response = session.post(f"{API_URL}/campaigns/319115/transactions", json=payload)
# with open("output/response-create-transaction.json", "w") as f:
#     json.dump(response.json(), f, indent=2)
# print(f"Done. Response status: {response.status_code}")
