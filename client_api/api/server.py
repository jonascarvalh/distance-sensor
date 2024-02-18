from api.model import db, Sensor, app, sensors_schema, sensor_schema
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow

CORS(app)
api = Api(app)
ma  = Marshmallow(app)

class Measures(Resource):
    def get(self):
        all_measures = Sensor.query.all()
        result = sensors_schema.dump(all_measures)

        return make_response(
            jsonify(result), 200
        )
    
    def post(self):
        measure = Sensor(
            measure=request.json['measure'],
            time=request.json['time'],
            uncertainty=request.json['uncertainty']
        )
        db.session.add(measure)
        db.session.commit()
        result = sensor_schema.dump(measure)

        return make_response(
            jsonify(result), 200
        )

    def delete(self):
        db.session.query(Sensor).delete()
        db.session.commit()
        return make_response(
            jsonify({"status": "all data has been deleted."}), 200
        )
    
class Measure(Resource):
    def get(self):
        measure = Sensor.query.all()
        result = sensors_schema.dump(measure)
        print(result)
        if result != []:
            return make_response(
                jsonify(result[-1]), 200
            )
        else:
            return make_response(
                jsonify({"status": "none measure in database."}), 200
            ) 
    
api.add_resource(Measures, '/measures')
api.add_resource(Measure, '/measure')

def server_run():
    with app.app_context():
        db.create_all()
        # db.drop_all()
    app.run(host="0.0.0.0", port=5000, debug=False)