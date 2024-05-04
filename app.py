from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///answers.db'
db = SQLAlchemy(app)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String(80), nullable=False)
    question2 = db.Column(db.String(20), nullable=False)
    question3 = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        question1 = request.form.get('username')
        question2 = request.form.get('question2')
        question3 = request.form.get('question3')

        if not (question1 and question2 and question3):
            return 'Lütfen tüm alanları doldurun.'

        score = 0
        if question2 == 'Numpy':
            score += 50
        if question3 == 'describe':
            score += 50

        new_answer = Answer(question1=question1, question2=question2, question3=question3, score=score)
        try:
            db.session.add(new_answer)
            db.session.commit()
            return redirect(url_for('result', score=score))
        except SQLAlchemyError as e:
            db.session.rollback()
            return f'Bir veritabanı hatası oluştu: {str(e)}'
        except Exception as e:
            return f'Beklenmeyen bir hata oluştu: {str(e)}'

@app.route('/result/<int:score>')
def result(score):
    return f'Your score: {score}%'

if __name__ == '__main__':
    with app.app_context():

        db.create_all()
    app.run(debug=True)