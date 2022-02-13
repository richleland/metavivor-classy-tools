from flask import Blueprint, redirect, render_template

from classy_tools.forms import UploadForm


upload_blueprint = Blueprint("upload", __name__)


@upload_blueprint.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template("upload.html", form=form)
