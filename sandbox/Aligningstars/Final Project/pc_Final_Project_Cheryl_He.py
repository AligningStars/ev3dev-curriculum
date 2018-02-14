"""
File Name: pc_Final_Project_Cheryl_He
Date Created: Feb 14, 2018
Author: Cheryl He
Introduction:

"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=40, relief='raised')
    main_frame.grid()

    word = 'project'
    for k in range(len(word)):
        letter = ttk.Label(main_frame, text="____")
        letter.grid(row=1, column=k)
        letter_entry = ttk.Entry(main_frame, width=4)
        letter_entry.grid(row=0, column=k)

    root.mainloop()


main()