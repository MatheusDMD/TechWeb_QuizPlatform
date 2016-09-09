# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True);password = db.Column(db.String(50), unique=False)

	def __init__(self, username, email, password):
    	   self.username = username
    	   self.email = email;
           self.password = password

class Quiz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique=False)
	theme = db.Column(db.String(100), unique=False);user_id = db.Column(db.Integer, db.ForeignKey('user.id'));

	def __init__(self,title, theme, user_id):
    	   self.title = title
    	   self.theme = theme
           self.user_id = user_id

class dquestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), unique=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    def __init__(self, question, quiz_id):
        self.question = question
        self.quiz_id = quiz_id

class mcquestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), unique=False)
    alt1 = db.Column(db.String(100), unique=False)
    alt2 = db.Column(db.String(100), unique=False)
    alt3 = db.Column(db.String(100), unique=False)
    alt4 = db.Column(db.String(100), unique=False)
    correct_alt = db.Column(db.Integer, unique=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    def __init__(self, question,alt1,alt2,alt3,alt4,correct_alt,quiz):
    	   self.question = question
           self.alt1 = alt1
           self.alt2 = alt2
           self.alt3 = alt3
           self.alt4 = alt4
           self.correct_alt = correct_alt
           self.quiz_id = quiz.id

@app.route('/stats')
def stats():
	list_stats = [ 0,1,2,3]
	return render_template('stats.html', lista=lista_stats)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
		mode = request.args.get('mode')
		if mode=='login':
			email = request.form["login_email"]
			password = request.form["login_password"]
			#voltar pra cá e ler como se
			login_user = User.query.filter_by(email=email).first()
			if login_user.password == password:
				return render_template('index.html', id=str(login_user.id))
			else:
				return 'wrong password'
		if mode=='register':
			first_name = request.form["first_name"]
	        last_name = request.form["last_name"]
	        email = request.form["email"]
	     	password = request.form["password"]
	     	user = User(username=first_name+' '+last_name, email=email, password=password)
	     	db.session.add(user)
	     	db.session.commit();next_page2 = make_response(render_template('index.html'));next_page2.set_cookie('user_id', str(user.id))
	        return next_page2
    return render_template('login.html')

@app.route('/main')
def main():
    return render_template('index.html')

@app.route('/create/<user_id>', methods=['GET', 'POST'])
def create_quiz(user_id):
   if request.method == 'POST':
	   title = request.form["title"]
	   theme = request.form["theme"];current_user = User.query.get(int(user_id))
	   quiz = Quiz(title=title, theme=theme, user_id=current_user.id)
	   resp = make_response(render_template('question.html'))
	   resp.set_cookie('quiz_id', str(quiz.id))
	   db.session.add(quiz)
	   db.session.commit()#return User.query.get(quiz.user_id).email
	   return render_template('question.html')
   return render_template('create.html')

@app.route('/question', methods=['GET','POST'])
def create_question():
	if request.method == 'POST':
		print(request.values)
		question = request.form["question"]
 	   	alt1 = request.form["alt1"]
		alt2 = request.form["alt2"]
		alt3 = request.form["alt3"]
		alt4 = request.form["alt4"]
		correct_alt = request.form["check"]
		quiz_id = request.cookies.get('quiz_id')
		m_question = mcquestion(question=question,alt1=alt1,alt2=alt2,alt3=alt3,alt4=alt4,correct_alt=correct_alt,quiz_id=quiz_id)
		db.session.add(m_question)
		db.session.commit()
		return render_template('index.html')
	return render_template('question.html')

@app.route('/quizlist', methods=['GET','POST'])
def list_quiz():
	if request.method == 'POST':
		quiz_id = request.form["select"]
		quiz_questions = mcquestion.query.filter_by(quiz_id=quiz_id).all()
		return render_template('questionlist.html',questions=quiz_questions)
	else:
		user_id = request.cookies.get('user_id')
		quizs = Quiz.query.filter_by(user_id=user_id).all()
	return render_template('quizlist.html',quizs=quizs)

@app.route('/userlist')
def list_user():
	users = User.query.all()
	return render_template('quizlist.html',quizs=users)

db.create_all()

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
