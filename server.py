from flask import Flask, jsonify, request
import requests
import logging
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
    times = in_dict["timestamp"]
    return [phys, data, times]


def add_physician_to_db(info):
    phys = NewPhysician(phys_id=info[0],
                        neck_angles=info[1],
                        timestamp=info[2])
    phys.save()


def init_db():
    print("connecting to database...")
    connect("mongodb+srv://aidan:Yf3GIDiE8GzUYyZB@cluster0.lmu1g.mongodb.net"
            "/NeckTecDB?retryWrites=true&w=majority")
    print("database connected.")


@app.route("/api/new_physician", methods=["POST"])
def post_new_physician():
    in_dict = request.get_json()
    physician_info = read_physician(in_dict)
    add_physician_to_db(physician_info)
    return "Successfully added physician to database.", 400



if __name__ == '__main__':
    logging.basicConfig(filename="status.log", filemode='w',
                        level=logging.DEBUG)
    init_db()
    app.run()
