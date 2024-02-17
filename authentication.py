from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)

with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/b29'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'osudhciuh'

    db = SQLAlchemy(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login_view'


    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), nullable=False)
        password = db.Column(db.String(20), nullable=False)


    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        unm = request.form.get('unm')
        pwd = request.form.get('pwd')
        user = User(username=unm, password=pwd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_view'))
    return render_template('register_user.html')


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        unm = request.form.get('unm')
        pwd = request.form.get('pwd')
        user = User.query.filter_by(username=unm, password=pwd).first()
        if user:
            login_user(user)
            return redirect(url_for('success_view'))
    return render_template('login_user.html')


@app.route('/success')
@login_required
def success_view():
    return render_template('success.html')


@app.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('login_view'))


if __name__ == '__main__':
    app.run(debug=True)
