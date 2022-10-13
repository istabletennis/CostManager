from flask import Flask, render_template, request, redirect
from flask_login import login_user, logout_user, login_required, current_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Product %r>' % self.id


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    budget = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return '<User %r>' % self.id


def count_sum(list_of_products):
    sum_of_prices = 0.0
    for element in list_of_products:
        sum_of_prices += element.price
    return "%.2f" % round(sum_of_prices, 2)


def count_budget(budget, sum_of_prices):
    return "%.2f" % round(budget - float(sum_of_prices), 2)


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():

    if request.method == 'POST':
        product = request.form['product']
        price = request.form['price']
        if product != '' and price != '':
            new_product = Products(product=product, price=price, user_id = current_user.get_id())
            try:
                db.session.add(new_product)
                db.session.commit()
            except:
                return 'There was an issue adding your product'
        return redirect('/')

    else:
        list_of_products = Products.query.filter_by(user_id=current_user.get_id()).order_by(Products.date_created).all()
        saved_products = requests.get('http://localhost:5001').json()
        sum_of_prices = count_sum(list_of_products)
        name = current_user.name
        budget = count_budget(current_user.budget, sum_of_prices)
        return render_template('index.html', list=list_of_products, sum=sum_of_prices,
                               saved=saved_products, budget=budget, name=name)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    product_to_delete = Products.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        if not user:
            return redirect('/signup')
        elif not check_password_hash(user.password, password):
            return redirect('/login')
        login_user(user, remember=remember)
        return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            return redirect('/signup')
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/editbudget', methods=['GET', 'POST'])
@login_required
def editbudget():
    user = User.query.get_or_404(current_user.get_id())

    if request.method == 'POST':
        user.budget = request.form['budget']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your budget'

    else:
        return render_template('editbudget.html', budget=user.budget)


@app.route('/save', methods=['POST'])
@login_required
def save():
    product = request.form['product']
    price = request.form['price']
    requests.post('http://localhost:5001', json={'product': product, 'price': price})
    return redirect('/')


@app.route('/deletesaved/<int:id>')
@login_required
def delete_saved(id):
    requests.delete('http://localhost:5001', json={'id': id})
    return redirect('/')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.config['SECRET_KEY'] = 'secret-key-goes-here'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        login_manager = LoginManager()
        login_manager.login_view = 'login'
        login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.run(debug=True, port=5000, host='0.0.0.0')
