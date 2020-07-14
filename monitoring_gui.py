import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import io
import matplotlib.image as mpimg
import requests
from tkinter.filedialog import asksaveasfile

server_name = "http://127.0.0.1:5000"


def get_available_physician_ids():
    """
    This function makes a GET request and returns a list of patient ids

    This function makes a GET request to the cloud server that stores
    physician data. This GET request will return a list of patient ids
    that are present in the database. This list is returned.
    :return: a list of patient ids in the database
    """
    # This will make a request
    r = requests.get(server_name + "/api/available_physician_ids")
    return r.json()


def load_physician_dates(phys_id):
    r = requests.get(server_name + "/api/retrieve_phys_dates/" + phys_id)
    return r.json()


def design_window():

    def load_dates():
        return load_physician_dates(str(physician_choice.get()))

    def send_data():
        physician_session_box['values'] = load_dates()

    root = tk.Tk()
    root.title("Physician User Interface")

    physician_id_text = ttk.Label(root, text="Select Physician ID")
    physician_id_text.grid(column=0, row=0)

    physician_choice = tk.StringVar()
    physician_id_box = ttk.Combobox(root, textvariable=physician_choice)
    physician_id_box['values'] = get_available_physician_ids()
    physician_id_box.state(["readonly"])
    physician_id_box.grid(column=1, row=0)

    physician_session_text = ttk.Label(root, text="Select Date")
    physician_session_text.grid(column=0, row=1)

    session_choice = tk.StringVar()
    physician_session_box = ttk.Combobox(root, textvariable=session_choice)
    physician_session_box.state(["readonly"])
    physician_session_box.grid(column=1, row=1)

    load_physician_button = ttk.Button(root, text="Confirm", command=send_data)
    load_physician_button.grid(column=2, row=0)

    load_physician_button = ttk.Button(root, text="Load Session Data")
    # command=new_patient)
    load_physician_button.grid(column=2, row=1)

    display_physician_id_text = ttk.Label(root, text="Physician ID:")
    display_physician_id_text.grid(column=0, row=2, sticky="E")

    display_physician_name_text = ttk.Label(root, text="Physician Name:")
    display_physician_name_text.grid(column=0, row=3, sticky="E")

    display_timestamp_text = ttk.Label(root,
                                       text="Time range of data collected:")
    display_timestamp_text.grid(column=0, row=4)

    display_physician_id_value = ttk.Label(root)
    display_physician_id_value.grid(column=1, row=2)

    display_physician_name_value = ttk.Label(root)
    display_physician_name_value.grid(column=1, row=3)

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
