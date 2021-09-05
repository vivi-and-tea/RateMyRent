from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_ADD')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), unique=True, nullable=False)
    oneroom = db.Column(db.Float)
    onek = db.Column(db.Float)
    twok = db.Column(db.Float)
    threek = db.Column(db.Float)
    fourk = db.Column(db.Float)

    def __repr__(self):
        return '<Cities %r>' % self.city


# @app.route("/")
# def home():
#     return render_template('index.html')

@app.route("/")
def home():
    salary = 24
    places = db.session.query(Places).all()

    return render_template('index.html', places=places)

if __name__ == "__main__":
    app.run(debug=True)
