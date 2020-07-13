import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import base64
import io
import matplotlib.image as mpimg
import requests
from tkinter.filedialog import asksaveasfile
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

server_name = config['connections']['local_server']
vm_server_name = config['connections']['vm_server']


def get_available_patient_ids():
    """
    This function makes a GET request and returns a list of patient ids

    This function makes a GET request to the cloud server that stores
    patient data. This GET request will return a list of patient ids
    that are present in the database. This list is returned.
    :return: a list of patient ids in the database
    """
    # This will make a request
    r = requests.get(server_name + "/patient_id_list")
    return r.json()


def load_patient_data(patient_id):
    """
    This function returns recent patient data for a specific id

    This function makes a GET request for a specific patient id that
    returns the patient's name, id, most recent heart rate, most
    recent ecg image, and time of the most recent ecg upload.
    :param patient_id: the id number of the patient of interest
    :return: a list containing recent patient information
    """
    # This will make a request
    r = requests.get(server_name + "/" + patient_id + "/load_recent_data")
    return r.json()


def design_window():
    root = tk.Tk()
    root.title("Monitoring Station User Interface")

    patient_id_text = ttk.Label(root, text="Select Patient ID")
    patient_id_text.grid(column=0, row=0)

    patient_choice = tk.StringVar()
    patient_id_box = ttk.Combobox(root, textvariable=patient_choice)
    patient_id_box['values'] = get_available_patient_ids()
    patient_id_box.state(["readonly"])
    patient_id_box.grid(column=1, row=0)

    load_patient_button = ttk.Button(root, text="Load Patient Data")
    # command=new_patient)
    load_patient_button.grid(column=2, row=0)

    patient_session_text = ttk.Label(root, text="Select Date")
    patient_session_text.grid(column=0, row=1)

    session_choice = tk.StringVar()
    patient_session_box = ttk.Combobox(root, textvariable=patient_choice)
    patient_session_box['values'] = get_available_patient_ids()
    patient_session_box.state(["readonly"])
    patient_session_box.grid(column=1, row=1)

    load_patient_button = ttk.Button(root, text="Load Session Data")
    # command=new_patient)
    load_patient_button.grid(column=2, row=1)

    display_patient_id_text = ttk.Label(root, text="Patient ID:")
    display_patient_id_text.grid(column=0, row=2, sticky="E")

    display_patient_name_text = ttk.Label(root, text="Patient Name:")
    display_patient_name_text.grid(column=0, row=3, sticky="E")

    display_timestamp_text = ttk.Label(root,
                                       text="Time range of data collected:")
    display_timestamp_text.grid(column=0, row=4)

    display_patient_id_value = ttk.Label(root)
    display_patient_id_value.grid(column=1, row=2)

    display_patient_name_value = ttk.Label(root)
    display_patient_name_value.grid(column=1, row=3)

    display_timestamp_value = ttk.Label(root)
    display_timestamp_value.grid(column=1, row=6)

    exit_button = ttk.Button(root, text="Exit")
    # command=cancel)
    exit_button.grid(column=2, row=9)

    reset_button = ttk.Button(root, text="Reset Data")
    # command=reset)
    reset_button.grid(column=1, row=9)

    root.mainloop()


if __name__ == '__main__':
    design_window()
