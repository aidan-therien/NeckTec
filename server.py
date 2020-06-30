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


def init_db():
    print("connecting to databse...")
    connect("mongodb+srv://aidan:<password>@cluster0.lmu1g.mongodb.net"
            "/<dbname>?retryWrites=true&w=majority")
    print("database connected.")


if __name__ == '__main__':
    logging.basicConfig(filename="status.log", filemode='w',
                        level=logging.DEBUG)
    init_db()
    app.run()
