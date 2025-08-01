from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/todoappcode"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    description = db.Column(db.String(500),nullable = False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)
    
    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route('/',methods=['GET','POST'])
def get_data():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get("description")
        todo = Todo(title=title, description = description)
        db.create_all()
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo = alltodo)

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        title = request.form.get('title')
        description = request.form.get("description")
        alltodo=Todo.query.filter_by(sno=sno).first()
        alltodo.title = title
        alltodo.description=description
        db.create_all()
        db.session.add(alltodo)
        db.session.commit()
        return redirect("/")
        
    alltodo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',alltodo=alltodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    alltodo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")


        

