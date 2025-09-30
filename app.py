from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os 
from flask_scss import Scss
from datetime import datetime, timezone

app= Flask(__name__)
Scss(app)


db_url = os.environ.get("DATABASE_URL", "sqlite:///instance/site.db")

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, server_default=func.now())


    def __repr__(self) -> str:
        return f"Task('{self.id}', '{self.content}', '{self.date_created}')"



@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = MyTask(content=current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except Exception as e:
            return f'There was an issue adding your task: {e}'

    else:
        tasks = MyTask.query.order_by(MyTask.date_created).all()
        return render_template('index.html', tasks=tasks)



@app.route('/delete/<int:id>')
def delete(id:int):
    delete_row=MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_row)
        db.session.commit()
        return redirect('/')
    
    except Exception as e:
        return f'Error {e}'
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id:int):
    task = MyTask.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'Error {e}'
    else:
        return "edit test"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)