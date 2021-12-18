from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import collections

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
    db.session.refresh(person)
    q1 = request.args.get('sceng')
    q2 = request.args.get('scger')
    q3 = request.args.get('scfr')
    q4 = request.args.get('scesp')
    q5 = request.args.get('uneng')
    q6 = request.args.get('unger')
    q7 = request.args.get('unfr')
    q8 = request.args.get('unesp')
    answer = Answers(id=person.id, q1=q1, q2=q2, q3=q3, q4=q4,
                     q5=q5, q6=q6, q7=q7, q8=q8)
    db.session.add(answer)
    db.session.commit()
    return 'Ok'

@app.route('/statistics')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(Person.age),
        func.min(Person.age),
        func.max(Person.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = Person.query.count()
    all_info['city_max'] = db.session.query(list(collections.Counter(Person.city).keys())[0])
    all_info['q1_max'] = db.session.query(list(collections.Counter(Answers.q1).keys())[0])
    q1_answers = db.session.query(Answers.q1).all()
    all_info['q2_mean'] = db.session.query(list(collections.Counter(Answers.q2).keys())[0])
    q2_answers = db.session.query(Answers.q2).all()
    all_info['q3_mean'] = db.session.query(list(collections.Counter(Answers.q3).keys())[0])
    q3_answers = db.session.query(Answers.q3).all()
    all_info['q4_mean'] = db.session.query(list(collections.Counter(Answers.q4).keys())[0])
    q4_answers = db.session.query(Answers.q4).all()
    all_info['q5_mean'] = db.session.query(list(collections.Counter(Answers.q5).keys())[0])
    q5_answers = db.session.query(Answers.q5).all()
    all_info['q6_mean'] = db.session.query(list(collections.Counter(Answers.q6).keys())[0])
    q6_answers = db.session.query(Answers.q6).all()
    all_info['q7_mean'] = db.session.query(list(collections.Counter(Answers.q7).keys())[0])
    q7_answers = db.session.query(Answers.q7).all()
    all_info['q8_mean'] = db.session.query(list(collections.Counter(Answers.q8).keys())[0])
    q8_answers = db.session.query(Answers.q8).all()
    return render_template('statistics.html', all_info=all_info)

if __name__ == '__main__':
    app.run(debug=True)