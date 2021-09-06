from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
from secretsecret import POSTGRES_ADD

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_ADD
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

@app.route("/recommend")
def recommend():
    salary = 40
    room_type = "twok"
    list = []
    places = db.session.query(Places).all()
    print(places)
    print("Heloo")
    for place in places:
        if place.twok / salary < .5:
            percent = (place.twok / salary)
            list.append({'City': place.city, 'Rent': place.twok, 'Percent': percent})

        else:
            pass
    mini = min(list, key=lambda x:x['Percent'])
    print(mini)
    return render_template('recommend.html', places=places, df=list, mini=mini)

# @app.route("/recommend")
# def recommend():
#     salary = 40
#     room_type = "twok"
#     col_names =  ['City', 'Rent', 'Percent']
#     df  = pd.DataFrame(columns = col_names)
#     places = db.session.query(Places).all()
#     print(places)
#     print("Heloo")
#     for place in places:
#         if place.twok / salary < .5:
#             percent = (place.twok / salary)
#             # df.append({'City' : f'{place.city}', 'Rent' : 'place.twok', 'Percent' : 'percent' }, ignore_index=True)
#             df.append({'City': 'blah'},ignore_index=True)
#             print(df)
#             print("hey")
#         else:
#             pass
#
#     return render_template('recommend.html', places=places, df=df)


if __name__ == "__main__":
    app.run(debug=True)
