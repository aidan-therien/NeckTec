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
    connect("mongodb+srv://james:nbzKGQnRbS8nXh5E@cluster0.lmu1g.mongodb.net"
            "/NeckTecDB?retryWrites=true&w=majority")
    print("database connected.")

def get_physician_status(phys_id):
    phys_id = int(phys_id)
    for phys in phys_db:
        if phys["phys_id"] == phys_id:
            neck_angles = phys['neck_angles']
            if len(neck_angles) == 1:
                neck_angles = neck_angles[0]
            else:
                neck_angles = neck_angles[-1]
            status = phys['status']
            timestamp = phys['timestamp']
            if len(timestamp) == 1:
                timestamp = timestamp[0]
            else:
                timestamp = timestamp[-1]
            status_phys = {"neck_angles": neck_angles,
                             "timestamp": timestamp}
            return status_phys
    return "Physician not found"
    
    


@app.route("/api/new_physician", methods=["POST"])
def post_new_physician():
    in_dict = request.get_json()
    physician_info = read_physician(in_dict)
    add_physician_to_db(physician_info)
    return "Successfully added physician to database.", 400
    
@app.route("/api/status/<phys_id>", methods=["GET"])
def get_physician_status(phys_id):
    return jsonify(get_physician_status(phys_id))



if __name__ == '__main__':
    logging.basicConfig(filename="../../Desktop/NeckTek/status.log", filemode='w',
                        level=logging.DEBUG)
    init_db()
    app.run()
