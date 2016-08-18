# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

class Test(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String(1000),  unique=False)
	answer = db.Column(db.String(1000), unique=False)

	def __init__(self, question, answer, number):
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
    	return " dado inserido"
   return '''
    	<form action="" method="post">
			<p>numero: <input type=number name=number style="height: 100px;">
        	<p>pergunta: <input type=text name=question style="height: 100px;">
        	<p>resposta: <input type=text name=answer style="height: 100px;">
        	<p><input type=submit value=Inserir>
    	</form>
	'''

@app.route('/read/<username>')
def read_user(username):
	user = User.query.filter_by(username=username).first()
	if(user):
    	  return user.username + " e-mail: &lt;" + user.email + "&gt;"
	else:
    	  return "Usuário não encontrado",404

db.create_all()

if __name__ == "__main__":
	app.run()
