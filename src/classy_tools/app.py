from flask import Flask, redirect, render_template

from classy_tools.api import get_campaigns_from_api
from classy_tools.forms import UploadForm


def create_app():
    app = Flask(__name__)
    app.config.from_object("classy_tools.config")

    @app.route("/upload")
    def upload():
        form = UploadForm()
        if form.validate_on_submit():
            return redirect("/")
        return render_template("upload.html", form=form)

    @app.route("/campaigns")
    def campaigns_list():
        campaigns = get_campaigns_from_api(app.config["ORG_ID"])
        campaigns = [{k: v for k, v in c.items() if k in ["id", "name", "canonical_url"]} for c in campaigns]
        return {"campaigns": campaigns}

    return app
