from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import plotly
import plotly.express as px
import json
import pandas as pd
#import plotly.graph_objects as go

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lang_base.db'
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    age = db.Column(db.Integer)
    gender = db.Column(db.Text)
    language = db.Column(db.Integer)
    city = db.Column(db.Text)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Text)
    q2 = db.Column(db.Text)
    q3 = db.Column(db.Text)
    q4 = db.Column(db.Text)
    q5 = db.Column(db.Text)
    q6 = db.Column(db.Text)
    q7 = db.Column(db.Text)
    q8 = db.Column(db.Text)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/questions')
def question_page():
    questions = Questions.query.all()
    return render_template('questions.html', questions=questions)


@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    language = request.args.get('flang')
    city = request.args.get('city')
    person = Person(
        name=name,
        age=age,
        gender=gender,
        language=language,
        city=city
    )
    db.session.add(person)
    db.session.commit()
    q1 = request.args.get('sceng')
    q2 = request.args.get('scger')
    q3 = request.args.get('scfr')
    q4 = request.args.get('scesp')
    q5 = request.args.get('uneng')
    q6 = request.args.get('unger')
    q7 = request.args.get('unfr')
    q8 = request.args.get('unesp')
    answer = Answers(q1=q1, q2=q2, q3=q3, q4=q4,
                     q5=q5, q6=q6, q7=q7, q8=q8)
    db.session.add(answer)
    db.session.commit()
    return render_template('thanks.html')


@app.route('/statistics')
def stats():
    con = sqlite3.connect('lang_base.db')
    cur = con.cursor()
    query = '''
    SELECT AVG(age)
    FROM people'''
    cur.execute(query)
    res = cur.fetchone()
    avg_age = res[0]

    city_query = '''
    SELECT city
    FROM people'''
    cur.execute(city_query)
    cities = cur.fetchall()
    lst_city = []
    lst_city_counter = []
    for element in cities:
        lst_city.append(element[0])
        lst_city_counter.append(1)
    df_city = pd.DataFrame(
        {
            'city': lst_city,
            'amount': lst_city_counter
        }
    )
    fig1 = px.histogram(df_city, x='city', y='amount', title='Статистика по городам')
    graph1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    query_q = '''
    SELECT q1, q2, q3, q4, q5, q6, q7, q8
    FROM answers'''
    cur.execute(query_q)
    answers = cur.fetchall()
    lst_q1 = []
    lst_q2 = []
    lst_q3 = []
    lst_q4 = []
    lst_q5 = []
    lst_q6 = []
    lst_q7 = []
    lst_q8 = []
    q_count = []
    print(answers)
    for ans in answers:
        lst_q1.append(ans[0])
        lst_q2.append(ans[1])
        lst_q3.append(ans[2])
        lst_q4.append(ans[3])
        lst_q5.append(ans[4])
        lst_q6.append(ans[5])
        lst_q7.append(ans[6])
        lst_q8.append(ans[7])
        q_count.append(1)
    df_q = pd.DataFrame(
        {
            'q1': lst_q1,
            'q2': lst_q2,
            'q3': lst_q3,
            'q4': lst_q4,
            'q5': lst_q5,
            'q6': lst_q6,
            'q7': lst_q7,
            'q8': lst_q8,
            'amount': q_count,
        }
    )
    fig2 = px.bar(df_q, x=['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8'],
                  y='amount', title='Статистика по вопросам')
    graph2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('statistics.html', avg_age=avg_age,
                           graph_city=graph1, graph_q=graph2)


@app.route('/person/<person_id>')
def person_page(person_id):
    person = Person.query.get(person_id)
    person_id = int(person_id)
    con = sqlite3.connect('lang_base.db')
    cur = con.cursor()
    cur.execute('SELECT MAX(id) FROM people')
    last_id = cur.fetchone()[0]
    print(last_id)
    if person_id + 1 > last_id:
        person_next = ''
    else:
        person_next = '/person/' + str(person_id + 1)
    if person_id == 1:
        person_prev = ''
    else:
        person_prev = '/person/' + str(person_id - 1)
    return render_template('person.html', person=person,
                           person_next=person_next, person_prev=person_prev)


if __name__ == '__main__':
    app.run(debug=True)
