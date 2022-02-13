from config import API_URL, CLIENT_ID, CLIENT_SECRET, TOKEN_URL
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


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


def get_fundraising_teams_from_api(campaign_id, url=None):
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
        teams = teams + get_fundraising_teams_from_api(campaign_id, next_page_url)

    # return the teams from all pages
    return teams


def get_fundraising_pages_from_api(campaign_id, url=None):
    if not url:
        url = f"{API_URL}/campaigns/{campaign_id}/fundraising-pages"

    response = session.get(url)
    response.raise_for_status()
    response_json = response.json()

    # append the current page's data
    pages = response_json["data"]

    # see if there's a next page
    next_page_url = response_json["next_page_url"]
    if next_page_url:
        pages = pages + get_fundraising_pages_from_api(campaign_id, next_page_url)

    # return the pages from all pages
    return pages


def create_offline_transaction(campaign_id, payload):
    response = session.post(f"{API_URL}/campaigns/{campaign_id}/transactions", json=payload)
    response.raise_for_status()
    return response.json()


def create_dedication(transaction_id, payload):
    response = session.post(f"{API_URL}/transactions/{transaction_id}/dedications", json=payload)
    response.raise_for_status()
    return response.json()
