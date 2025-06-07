# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquakes_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    
    if earthquake:
        body = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }      
        status_code = 200
    else:
        body = {
            "message": f"Earthquake {id} not found."
        }
        status_code = 404
    
    return make_response(jsonify(body), status_code)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    matching_quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    quakes_data = [
        {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        for quake in matching_quakes
    ]

    body = {
        "count": len(quakes_data),
        "quakes": quakes_data
    }

    return make_response(jsonify(body), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
