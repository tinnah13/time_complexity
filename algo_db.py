from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(100))
    step = db.Column(db.Integer)
    n_max = db.Column(db.Integer)
