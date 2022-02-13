from flask import Flask

from classy_tools.api import get_campaigns_from_api
from classy_tools.blueprints.upload import upload_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object("classy_tools.config")

    app.register_blueprint(upload_blueprint)

    @app.route("/campaigns")
    def campaigns_list():
        campaigns = get_campaigns_from_api(app.config["ORG_ID"])
        campaigns = [{k: v for k, v in c.items() if k in ["id", "name", "canonical_url"]} for c in campaigns]
        return {"campaigns": campaigns}

    return app
