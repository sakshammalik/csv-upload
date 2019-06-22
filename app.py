from flask import Flask, render_template, request, redirect, jsonify
from flask_bootstrap import Bootstrap
import os
import csv
import io
import tasks
import json
from db import db
import models

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Bootstrap(app)


def upload(file):
    if not file:
        return 'Please attach a file'

    stream = io.StringIO(file.stream.read().decode('UTF8'), newline=None)
    csv_dict = csv.DictReader(stream, delimiter=",")
    products = list(csv_dict)
    # Celery task
    tasks.upload_file.delay(products)
    return {'result': 'uploading'}


@app.route('/products')
def get_products():
    return render_template('products.html')


@app.route('/search', methods=['POST'])
def search():
    data = json.loads(request.data.decode('utf8'))
    search_term = data['text']
    status = data['status']
    if search_term and status:
        all_products = db.session.query(models.Product)\
            .filter(models.Product.name.ilike('%'+search_term+'%'),
                    models.Product.status == status).all()
        return jsonify({'result': 'success',
                        'is_search': True,
                        'data': render_template('list.html', products=all_products)})
    else:
        all_products = db.session.query(models.Product)\
            .filter(models.Product.status == status).all()
        return jsonify({'result': 'success',
                        'is_search': False,
                        'data': render_template('list.html', products=all_products)})


@app.route('/get_all_products', methods=['GET', 'POST'])
def get_all_products():
    data = json.loads(request.data.decode('utf8'))
    status = data['status']
    all_products = db.session.query(models.Product) \
        .filter(models.Product.status == status).all()
    return jsonify({'result': 'success',
                    'data': render_template('list.html', products=all_products)})


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['inputFile']
        upload(file)
        return redirect('/products')
    return render_template('index.html')


@app.errorhandler(404)
def error_handler(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
