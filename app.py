from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- Model ----------------
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# --------------- CLI Command to Create DB -----------------
@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables."""
    db.create_all()
    print('Initialized the database.')

# --------------- Routes -----------------
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # get data from form
        title = request.form['title']
        desc = request.form['description']
        print(f"Received title: {title}, description: {desc}")  # Debugging
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        print("Todo added to database.")  # Debugging
        return redirect('/')
    
    # show all todos
    all_todos = Todo.query.all()
    print(f"Fetched todos: {all_todos}")  # Debugging
    return render_template('index.html', all_todos=all_todos)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['description']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)




if __name__ == "__main__":
    app.run(debug=True, port=8000)

    # app.run(debug=True, port=8080)