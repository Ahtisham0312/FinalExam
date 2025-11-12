from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

# Home - show all users
@app.route('/')
def home():
    users = User.query.all()
    return render_template('index.html', users=users)

# Add new user
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']

        new_user = User(name=name, roll_number=roll_number)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('form.html')

# Update existing user
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.roll_number = request.form['roll_number']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('update.html', user=user)

# Delete user
@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
