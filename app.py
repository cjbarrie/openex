from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import random

file_path = os.path.abspath(os.getcwd())+"/instance/responses.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/responses.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    ideology = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False)
    group = db.Column(db.String(50), nullable=True)
    social_media_hours = db.Column(db.Float, nullable=True)
    favorite_color = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<SurveyResponse {self.name}>'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        timestamp = datetime.utcnow()

        response = SurveyResponse(name=name, email=email, age=0, gender='', ideology=1, timestamp=timestamp)
        db.session.add(response)
        db.session.commit()

        return redirect(url_for('questions'))
    print('Redirecting to questions page')

    return render_template('index.html')

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        ideology = request.form['ideology']

        response = SurveyResponse.query.order_by(SurveyResponse.id.desc()).first()

        response.age = age
        response.gender = gender
        response.ideology = ideology

        group = random.choice(['treatment', 'control'])
        response.group = group
        db.session.commit()

        if group == 'treatment':
            return redirect(url_for('treatment'))
        else:
            return redirect(url_for('control'))

    return render_template('questions.html')

@app.route('/treatment', methods=['GET', 'POST'])
def treatment():
    if request.method == 'POST':
        hours = request.form['time_on_social_media']
        response = SurveyResponse.query.order_by(SurveyResponse.id.desc()).first()
        response.social_media_hours = hours
        db.session.commit()
        return redirect(url_for('thanks'))

    return render_template('treatment.html')

@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        color = request.form['favourite_color']
        response = SurveyResponse.query.order_by(SurveyResponse.id.desc()).first()
        response.favorite_color = color
        db.session.commit()
        return redirect(url_for('thanks'))

    return render_template('control.html')


@app.route('/thanks', methods=['GET'])
def thanks():
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
