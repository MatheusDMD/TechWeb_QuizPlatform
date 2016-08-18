# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

class Test(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String(100),  unique=False)
	answer = db.Column(db.String(100), unique=False)

	def __init__(self, question, answer):
    	   self.question = question
    	   self.answer = answer

@app.route('/create', methods=['GET', 'POST'])
def add_user():
   if request.method == 'POST':
    	question = request.form["question"]
    	answer = request.form["answer"]
    	test = Test(question=question, answer=answer)
    	db.session.add(test)
    	db.session.commit()
        tests = Test.query.all()
    	return render_template('quizlist.html',tests=tests)
   return render_template('create.html')

@app.route('/quizlist')
def list_user():
	tests = Test.query.all()
	return render_template('quizlist.html',tests=tests)

db.create_all()

if __name__ == "__main__":
	app.run()
