from flask import Flask, redirect, render_template

from .api import get_campaigns_from_api
from .forms import UploadForm


app = Flask(__name__)
app.config.from_object("config")


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
