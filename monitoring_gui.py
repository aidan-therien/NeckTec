import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import io
from io import BytesIO
import matplotlib.image as mpimg
import requests
from configparser import ConfigParser
import numpy as np
import base64
import csv
import csv

config = ConfigParser()
config.read('config.ini')

server_name = config['connections']['local_server']
vm_server_name = config['connections']['vm_server']


def load_image_for_display(file_name):
    image_object = Image.open(file_name)
    image_object = image_object.resize((300, 300), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(image_object)
    return tk_image


def get_available_physician_ids():
    # This will make a request
    r = requests.get(server_name + "/api/available_physician_ids")
    return r.json()


def load_physician_dates(phys_id):
    r = requests.get(server_name + "/api/retrieve_phys_dates/" + phys_id)
    return r.json()


def load_plot_data(phys_id, date):
    r = requests.get(server_name + "/api/get_data/" + str(phys_id) +
                     "/" + date)
    return r.json()


def design_window():

    def load_dates():
        return load_physician_dates(str(physician_choice.get()))

    def send_data():
        physician_session_box['values'] = load_dates()

    def display_timestamp_range(data):
        first = data[1]
        last = data[-1]
        str_out = first + " - " + last
        display_timestamp.configure(text=str_out)

    def save_plot(plot):
        image_bytes = base64.b64decode(plot)
        with open("temp_image", "wb") as out_file:
            out_file.write(image_bytes)

    def load_plot_for_display():
        tk_image = load_image_for_display("temp_image")
        display_plot.image = tk_image
        display_plot.configure(image=tk_image)

    def save_data():
        return True

    def display_plot():
        phys_id = physician_choice.get()
        date = session_choice.get()
        data = load_plot_data(phys_id, date)
        plt.clf()
        plt.plot(data[0], np.linspace(0, len(data[0])-1, len(data[0])))
        plt.xlabel("Time (s)")
        plt.ylabel("Angle (degree)")
        plot_bytes = BytesIO()
        plt.savefig(plot_bytes, format='png')
        plot_bytes.seek(0)
        temp = base64.b64encode(plot_bytes.read())
        plot_hash = str(temp, encoding='utf-8')
        save_plot(plot_hash)
        load_plot_for_display()
        display_timestamp_range(data[1])

    def data_save():
        physician_id = physician_choice.get()
        time = session_choice.get()
        time_data = load_plot_data(physician_id, time)
        d = {}
        for elem in time_data:
            if elem[1] in d:
                d[elem[1]].append(elem[0])
            else:
                d[elem[1]] = [elem[0]]
        filename = "neck angle data: " + time
        fields = ['neck angles', 'timestamps']
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(d)

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

    load_physician_button = ttk.Button(root, text="Save Session Data",
                                       command=save_data)
    load_physician_button.grid(column=2, row=1)

    display_physician_name_text = ttk.Label(root, text="Physician Name:")
    display_physician_name_text.grid(column=0, row=2, sticky="E")

    plot_text = ttk.Label(root, text="Neck Angle Plot:")
    plot_text.grid(column=0, row=3)

    plot_button = ttk.Button(root, text="Load Plot",
                             command=display_plot)
    plot_button.grid(column=1, row=8)

    display_plot = ttk.Label(root)
    display_plot.grid(column=1, row=3)

    timestamp_text = ttk.Label(root, text="Time range of data collected:")
    timestamp_text.grid(column=0, row=4)

    display_timestamp = ttk.Label(root)
    display_timestamp.grid(column=1, row=4)

    display_physician_id_value = ttk.Label(root)
    display_physician_id_value.grid(column=1, row=2)

    display_physician_name_value = ttk.Label(root)
    display_physician_name_value.grid(column=1, row=3)

    display_timestamp_value = ttk.Label(root)
    display_timestamp_value.grid(column=1, row=5)

    csv_button = ttk.Button(root, text="Download Data", command=data_save)
    csv_button.grid(column=2, row=8)

    exit_button = ttk.Button(root, text="Exit")
    # command=cancel)
    exit_button.grid(column=3, row=8)

    reset_button = ttk.Button(root, text="Reset Data")
    # command=reset)
    reset_button.grid(column=0, row=8)

    root.mainloop()


if __name__ == '__main__':
    design_window()
