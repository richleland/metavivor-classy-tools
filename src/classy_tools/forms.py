from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired


class UploadForm(FlaskForm):
    csv_file = FileField(
        "CSV file",
        validators=[
            FileRequired(),
            FileAllowed(["csv"], "CSV only!"),
        ],
    )
