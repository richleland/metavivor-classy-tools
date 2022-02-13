from flask import Flask

from api import get_campaigns_from_api
from config import ORG_ID

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world!"


@app.route("/campaigns")
def campaigns_list():
    campaigns = get_campaigns_from_api(ORG_ID)
    campaigns = [{k: v for k, v in c.items() if k in ["id", "name", "canonical_url"]} for c in campaigns]
    return {"campaigns": campaigns}
