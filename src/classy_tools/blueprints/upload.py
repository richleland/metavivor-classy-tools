import pandas as pd
from flask import Blueprint, render_template
from werkzeug.utils import secure_filename

from classy_tools.forms import UploadForm


upload_blueprint = Blueprint("upload", __name__)


@upload_blueprint.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.csv_file.data
        file_name = secure_filename(f.filename)
        # import ipdb; ipdb.set_trace()
        df = pd.read_csv(f)
        table = df.to_html()
        return render_template("preview.html", data=table, file_name=file_name)
    return render_template("upload.html", form=form)
