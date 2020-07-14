import requests
from datetime import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

local_server_name = config['connections']['local_server']
vm_server_name = config['connections']['vm_server']


def add_new_physician():
    str_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    new_physician = {"phys_id": 10,
                     "neck_angles": [2.234, 3.3456, 4.4567, 5],
                     "timestamp": [str_time, str_time, str_time]}
    r = requests.post(server_name+"/api/new_physician", json=new_physician)
    print(r.text)


def get_physician_status():
    r = requests.get(server_name+"/api/status/1")
    print(r.text)


def add_physician_data():
    data = {"phys_id": "1",
            "data": 101.9}
    r = requests.post(server_name+"/api/add", json=data)
    print(r.text)


def physician_ids():
    r = requests.get(server_name+"/api/available_physician_ids")
    print(r.text)


def dates():
    r = requests.get(server_name+"/api/retrieve_phys_dates/1")
    print(r.text)


if __name__ == '__main__':
    # dates()
    physician_ids()
    # add_physician_data()
    # get_physician_status()
    # add_physician_data()
