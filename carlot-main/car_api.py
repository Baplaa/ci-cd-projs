from flask import Flask
from flask import request
from flask import Response

from car_manager import CarManager

import json

app = Flask(__name__)

DB_NAME = "sqlite:///carlot.sqlite"


@app.route('/cars/all', methods=['GET'])
def get_all_cars():
    """ Gets all car records """

    car_mgr = CarManager(DB_NAME)
    cars = car_mgr.get_all_cars()

    car_list = []
    for car in cars:
        car_list.append(car.to_dict())

    result = json.dumps(car_list)

    response = app.response_class(
        response=result,
        status=200,
        mimetype='application/json')

    return response

@app.route('/cars', methods=['POST'])
def add_car():
    """ Adds a new car record """

    car_json = request.get_json()

    car_mgr = CarManager(DB_NAME)

    try:
        car_mgr.add_car(car_json['make'], car_json['model'], car_json['year'], car_json['price'])

        response = app.response_class(status=200)
    except ValueError as e:
        response = app.response_class(response=str(e), status=400)

    return response



@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    """ Deletes a car record """

    car_mgr = CarManager(DB_NAME)

    try:
        car_mgr.delete_car(id)

        response = app.response_class(status=200)
    except ValueError as e:
        response = app.response_class(response=str(e), status=404)

    return response


if __name__ == "__main__":
    print("Hello for lab 12")
    app.run(host='0.0.0.0', port=5000)
