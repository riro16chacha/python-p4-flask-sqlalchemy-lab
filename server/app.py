#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    if animal is None:
        return make_response('<h1>Animal not found</h1>', 404)

    attributes = {
        'Name': animal.name,
        'Species': animal.species,
        'Zookeeper': animal.zookeeper.name if animal.zookeeper else 'No assigned zookeeper',
        'Enclosure': animal.enclosure.environment if animal.enclosure else 'No assigned enclosure'
        # Add more attributes as needed
    }

    response_body = '<ul>' + ''.join([f'<li>{key}: {value}</li>' for key, value in attributes.items()]) + '</ul>'
    return make_response(response_body, 200)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if zookeeper is None:
        return make_response('<h1>Zookeeper not found</h1>', 404)

    attributes = {
        'Name': zookeeper.name,
        'Birthday': zookeeper.birthday,
        'Animals': '<ul>' + ''.join([f'<li>{animal.name}</li>' for animal in zookeeper.animals]) + '</ul>' if zookeeper.animals else 'No assigned animals'
        # Add more attributes as needed
    }

    response_body = '<ul>' + ''.join([f'<li>{key}: {value}</li>' for key, value in attributes.items()]) + '</ul>'
    return make_response(response_body, 200)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if enclosure is None:
        return make_response('<h1>Enclosure not found</h1>', 404)

    attributes = {
        'Environment': enclosure.environment,
        'Open to Visitors': 'Yes' if enclosure.open_to_visitors else 'No',
        'Animals': '<ul>' + ''.join([f'<li>{animal.name}</li>' for animal in enclosure.animals]) + '</ul>' if enclosure.animals else 'No assigned animals'
        # Add more attributes as needed
    }

    response_body = '<ul>' + ''.join([f'<li>{key}: {value}</li>' for key, value in attributes.items()]) + '</ul>'
    return make_response(response_body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
