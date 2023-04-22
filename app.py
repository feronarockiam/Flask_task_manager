from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['TIMEZONE'] = 'UTC'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

def main():
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        tasks = Task.query.order_by(Task.timestamp).all()
        return render_template('index.html', tasks=tasks)

    @app.route('/add', methods=['POST'])
    def add():
        title = request.form['title']
        description = request.form['description']
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/delete/<int:id>', methods=['POST'])
    def delete(id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/update/<int:id>', methods=['POST', 'GET'])
    def update(id):
        task = Task.query.get_or_404(id)
        if request.method == 'POST':
            task.title = request.form['title']
            task.description = request.form['description']
            task.timestamp = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('update.html', task=task)

    app.run(debug=True)

if __name__ == "__main__":
    main()
