from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gymplan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class gymplan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    days = db.Column(db.String(100), nullable=False)
    workout = db.Column(db.String(200))

    def __init__(self, days, workout):
        self.days = days
        self.workout = workout

@app.route('/')
def home():
    plans = gymplan.query.order_by(gymplan.id).all()
    return render_template('index.html', plans=plans)

@app.route('/exercise', methods =['POST', 'GET'])
def exerc():
    if request.method == 'POST':
        day = request.form['days']
        wrkt = request.form['workout']
        new_plan = gymplan(days=day, workout=wrkt)

        try:
            db.session.add(new_plan)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return 'There was an issue adding your plan'
    else:
        return render_template('exercise.html')


@app.route('/delete/<int:id>')
def delete(id):
    plan_del = gymplan.query.get_or_404(id)

    try:
        db.session.delete(plan_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'A problem occurred when deleting'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    plan = gymplan.query.get_or_404(id)
    if request.method == 'POST':
        plan.days = request.form['days']
        plan.workout = request.form['workout']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'A problem occurred when deleting'
    else:
        return render_template('update.html', plan=plan)
if __name__ == '__main__':
    db.create_all()
    app.run(port = '8080', debug = True)