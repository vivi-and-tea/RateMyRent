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

places = db.session.query(Places).all()
room_type = ""

def rent_finder(place, room_type):
    if room_type == "oneroom":
        return place.oneroom
    elif room_type == "onek":
        return place.onek
    elif room_type == "twok":
        return place.twok
    elif room_type == "threek":
        return place.threek
    elif room_type == "fourk":
        return place.fourk

def rate_rent(percent):
    if percent <= 25:
        return "A+"
    elif percent <= 30:
        return "A"
    elif percent <= 33:
        return "B+"
    elif percent <= 35:
        return "B"
    elif percent <= 40:
        return "B-"
    elif percent <= 45:
        return "C"
    elif percent <= 45:
        return "C-"




@app.route("/")
def home():
    return render_template('index.html')

@app.route('/rate')
def rate():

    salary = 24
    room_type = "twok"
    user_city = 3
    place = Places.query.get(user_city)
    rent = rent_finder(place, room_type)
    percent = int((rent / salary) * 100)
    grade = rate_rent(percent)

    return render_template('rate.html', place=place, rent=rent, percent=percent, grade=grade)

@app.route("/recommend")
def recommend():
    salary = 20
    room_type = "onek"
    list = []

    for place in places:

        rent = rent_finder(place, room_type)
        percent = int((rent / salary) * 100)


        if percent < 50 and percent > 20:
            list.append({'City': place.city, 'Rent': rent, 'Percent': percent})
        else:
            pass

    message = ""
    mini = ""
    if len(list):
        mini = min(list, key=lambda x:x['Percent'])
    else:
        message="Sorry, we couldn't find a good fit. Try changing your preferred room size for different options."

    context = {}
    context['places'] = places
    context['room_type'] = room_type
    context['salary'] = salary

    if mini:
        context['mini'] = mini
    if message:
        context['message'] = message

    return render_template('recommend.html', **context)




if __name__ == "__main__":
    app.run(debug=True)
