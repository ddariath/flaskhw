from flask import Flask, render_template, request
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template("index.html")


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    age = db.Column(db.Integer)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    def __init__(self, id, text):
        self.id = id
        self.text = text


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q0 = db.Column(db.Integer)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.Integer)
    q9 = db.Column(db.Integer)

    def __init__(self, id, q0, q1, q2, q3, q4, q5, q6, q7, q8, q9):
        self.id = id
        self.q0 = q0
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6
        self.q7 = q7
        self.q8 = q8
        self.q9 = q9


@app.route('/questions')
def question_page():
    questions = Questions.query.all()
    return render_template(
        'questions.html',
        questions=questions
    )


@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    gender = request.args.get('gender')
    education = request.args.get('education')
    age = request.args.get('age')
    user = User(
        age=age,
        gender=gender,
        education=education
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    q0 = request.args.get('q0')
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')
    q6 = request.args.get('q6')
    q7 = request.args.get('q7')
    q8 = request.args.get('q8')
    q9 = request.args.get('q9')
    answer = Answers(user.id, q0, q1, q2, q3, q4, q5, q6, q7, q8, q9)
    db.session.add(answer)
    db.session.commit()
    db.session.refresh(answer)
    return render_template('final.html')


@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = User.query.count()
    all_info['q0_mean'] = db.session.query(func.avg(Answers.q0)).one()[0]
    all_info['q5_mean'] = db.session.query(func.avg(Answers.q5)).one()[0]
    all_info['q1_mean'] = db.session.query(func.avg(Answers.q1)).one()[0]
    return render_template('stats.html', all_info=all_info)


with app.app_context():

    db.create_all()
    questions = Questions.query.all()
    if len(questions) == 0:
        db.session.add(Questions(0, 'Ирония судьбы'))
        db.session.add(Questions(1, 'Один дома'))
        db.session.add(Questions(2, 'Клаус'))
        db.session.add(Questions(3, 'Гринч'))
        db.session.add(Questions(4, 'Иван Васильевич меняет профессию'))
        db.session.add(Questions(5, 'Елки'))
        db.session.add(Questions(6, 'Джентельмены удачи'))
        db.session.add(Questions(7, 'Карнавальная ночь'))
        db.session.add(Questions(8, 'Бриллиантовая рука'))
        db.session.add(Questions(9, 'Реальная любовь'))
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
