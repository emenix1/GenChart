from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///KKGenChart.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.secret_key = 'kl_as_As-#@$d-aSDADs#@@#$%$^%&^'
db = SQLAlchemy(app)


from carcass import config, handlers, forms

with app.app_context():
    db.create_all()
