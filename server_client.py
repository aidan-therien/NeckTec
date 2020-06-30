import requests
from datetime import datetime

server_name = "http://127.0.0.1:5000"


def add_new_physician():
    str_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    new_physician = {"phys_id": 1,
                     "neck_angles": [1.234, 2.3456, 3.4567, 4],
                     "timestamp": [str_time, str_time, str_time]}
    r = requests.post(server_name+"/api/new_physician", json=new_physician)
    print(r.text)


if __name__ == '__main__':
    add_new_physician()
