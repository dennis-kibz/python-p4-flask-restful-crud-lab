#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        return make_response(jsonify(plant.to_dict()), 200)
    
    def patch(self, id):
        print(f"Patch request for plant ID: {id}")
        plant = Plant.query.filter_by(id=id).first()

        if not plant:
            print("Plant not found")
            return make_response(jsonify({"error": "Plant not found"}), 404)
        
        data = request.get_json()
        print(f"Request data: {data}")

        try:
            # Update only the fields that are provided in the request
            for key in data:
                if hasattr(plant, key):
                    print(f"Updating {key} to {data[key]}")
                    setattr(plant, key, data[key])
            

            db.session.commit()

            plant_dict = plant.to_dict()
            print(f"Plant dict from to_dict(): {plant_dict}")
            print(f"Plant dict keys: {plant_dict.keys()}")
            
            # Temporary: Manual dict creation to test
            manual_dict = {
                'id': plant.id,
                'name': plant.name,
                'image': plant.image,
                'price': plant.price,
                'is_in_stock': plant.is_in_stock
            }
            print(f"Manual dict: {manual_dict}")

            return make_response(jsonify(plant.to_dict()), 200)
        except Exception as e:
            print(f"Error during patch: {e}")
            db.session.rollback()

            return make_response(jsonify({"error": str(e)}), 400)
        
    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()

        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)
        
        try:
            db.session.delete(plant)
            db.session.commit()

            return make_response('', 204)
    
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 400)
    


api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
