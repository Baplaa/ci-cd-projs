from flask import Flask, request
from point_manager import PointManager
from point import Point
import json

app = Flask(__name__)

POINTS_DB = 'points.sqlite'

point_mgr = PointManager(POINTS_DB)

@app.route('/points', methods=['POST'])
def add_point():
    """ Adds a point to the Grid """
    content = request.json

    try:
        point = Point(content['x'], content['y'])
        point_id = point_mgr.add_point(point)

        response = app.response_class(
            response=str(point_id),
            status=200
        )
    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=400
        )

    return response

@app.route('/points/<int:point_id>', methods=['PUT'])
def update_point(point_id):
    """ Updates an existing point in the Point Manager """
    content = request.json

    if point_id <= 0:
        response = app.response_class(
            status=400
        )
        return response

    try:
        point = Point(content['x'], content['y'])
        point.id = point_id
        point_mgr.update_point(point)

        response = app.response_class(
            status=200
        )
    except ValueError as e:
        status_code = 400
        if str(e) == "Point does not exist":
            status_code = 404

        response = app.response_class(
            response=str(e),
            status=status_code
        )

    return response

@app.route('/points/<int:point_id>', methods=['GET'])
def get_point(point_id):
    """ Gets an existing point from the Point Manager """

    if point_id <= 0:
        response = app.response_class(
            status=400
        )
        return response

    try:
        point = point_mgr.get_point(point_id)

        response = app.response_class(
            status=200,
            response=json.dumps(point.to_dict()),
            mimetype='application/json'
        )

        return response
    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=400
        )

        return response

@app.route('/points/<int:point_id>', methods=['DELETE'])
def delete_point(point_id):
    """ Delete an existing point from the Point Manager """

    if point_id <= 0:
        response = app.response_class(
            status=400
        )
        return response

    try:
        point_mgr.delete_point(point_id)

        response = app.response_class(
            status=200
        )
    except ValueError as e:
        status_code = 400
        if str(e) == "Point does not exist":
            status_code = 404

        response = app.response_class(
            response=str(e),
            status=status_code
        )

    return response

@app.route('/points/all', methods=['GET'])
def get_all_points():
    """ Gets all points in the Point Manager """
    points = point_mgr.get_all_points()

    point_list = []

    for point in points:
        point_list.append(point.to_dict())

    response = app.response_class(
        status=200,
        response=json.dumps(point_list),
        mimetype='application/json'
    )

    return response


if __name__ == "__main__":
    print("anything u want test")
    app.run(host='0.0.0.0', port=3000)
