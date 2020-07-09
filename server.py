from flask import Flask, jsonify, request
import requests
import logging
from pymodm import connect, MongoModel, fields
from pymodm import errors as pymodm_errors
import pymodm


app = Flask(__name__)


class NewPhysician(MongoModel):
    phys_id = fields.IntegerField(primary_key=True)
    neck_angles = fields.ListField()
    timestamp = fields.ListField()


def read_physician(in_dict):
    phys = in_dict["phys_id"]
    data = in_dict["neck_angles"]
    times = in_dict["timestamp"]
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


def add_data(phys_id, data):
    phys_id = int(phys_id)
    try:
        temp = NewPhysician.objects.raw({"_id": phys_id}).first()
        temp.neck_angles.append(data[0])
        temp.timestamp.append(data[1])
        temp.save()
    except pymodm_errors.DoesNotExist:
        return "Physician not found", 400
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


@app.route("/api/add/<phys_id>", methods=["POST"])
def post_new_data(phys_id):
    data = request.get_json()
    return add_data(phys_id, data)


@app.route("/api/delete/<phys_id>", methods=["DELETE"])
def delete_physician(phys_id):
    phys_id = int(phys_id)
    try:
        db_phys = NewPhysician.objects.raw({"_id": phys_id}).first()
    except pymodm_errors.DoesNotExist:
        return "{} is not in the database".format(phys_id), 400
    pymodm.delete(db_phys)
    return "Successfully removed physician from database", 200


if __name__ == '__main__':
    logging.basicConfig(filename="status.log", filemode='w',
                        level=logging.DEBUG)
    init_db()
    app.run()
