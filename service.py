from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

service = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
service.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'service.db')
db = SQLAlchemy(service)


class SavedProducts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<SavedProduct %r>' % self.id


@service.route('/', methods=['POST', 'GET', 'DELETE'])
def index():

    if request.method == 'POST':
        product = request.json['product']
        price = request.json['price']
        product_to_save = SavedProducts(product=product, price=price)
        try:
            db.session.add(product_to_save)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem adding that product'

    if request.method == 'GET':
        response = []
        saved_products = SavedProducts.query.order_by(SavedProducts.date_created).all()
        for element in saved_products:
            response.append({'id': element.id, 'product': element.product, 'price': element.price})
        return jsonify(response)

    if request.method == 'DELETE':
        id = request.json['id']
        product_to_delete = SavedProducts.query.get_or_404(id)
        try:
            db.session.delete(product_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem deleting that product'


if __name__ == "__main__":
    with service.app_context():
        db.create_all()
    service.run(debug=True, port=5001, host='0.0.0.0')