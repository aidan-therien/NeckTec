from flask import Flask, jsonify, request
import requests
import logging
from datetime import datetime
from pymodm import connect, MongoModel, fields
from pymodm import errors as pymodm_errors


app = Flask(__name__)


class NewPhysician(MongoModel):
    phys_id = fields.IntegerField(primary_key=True)
    neck_angles = fields.ListField()
    timestamp = fields.ListField()


def read_physician(in_dict):
    phys = in_dict["phys_id"]
    data = in_dict["neck_angles"]
    times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    return [phys, data, times]


def add_physician_to_db(info):
    phys = NewPhysician(phys_id=info[0],
                        neck_angles=info[1],
                        timestamp=info[2])
    phys.save()


def init_db():
    print("connecting to database...")
    connect("mongodb+srv://aidan:necktec@cluster0.lmu1g.mongodb.net"
            "/NeckTecDB?retryWrites=true&w=majority")
    print("database connected.")


def retrieve_physician_status(phys_id):
    phys_id = int(phys_id)
    try:
        temp = NewPhysician.objects.raw({"_id": phys_id}).first()
        neck_angles = temp.neck_angles
        timestamp = temp.timestamp
        status_phys = {"neck_angles": neck_angles,
                       "timestamp": timestamp}
    except pymodm_errors.DoesNotExist:
        return "Physician not found", 400
    return status_phys


def add_data(data):
    phys_id = int(data["phys_id"])
    try:
        temp = NewPhysician.objects.raw({"_id": phys_id}).first()
    except pymodm_errors.DoesNotExist:
        return "Physician not found", 400
    temp.neck_angles.append(float(data["data"]))
    temp.timestamp.append(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
    temp.save()
    return "Successfully added data", 200


@app.route("/api/new_physician", methods=["POST"])
def post_new_physician():
    in_dict = request.get_json()
    physician_info = read_physician(in_dict)
    add_physician_to_db(physician_info)
    return "Successfully added physician to database.", 400


@app.route("/api/status/<phys_id>", methods=["GET"])
def get_physician_status(phys_id):
    return jsonify(retrieve_physician_status(phys_id))


@app.route("/api/add", methods=["POST"])
def post_new_data():
    data = request.get_json()
    print("data received")
    return add_data(data)


if __name__ == '__main__':
    logging.basicConfig(filename="status.log", filemode='w',
                        level=logging.DEBUG)
    init_db()
    app.run(host="0.0.0.0")
