"""
File Name: pc_Final_Project_Cheryl_He
Date Created: Feb 14, 2018
Author: Cheryl He
Introduction:

"""

import tkinter
from tkinter import ttk
from tkinter import *

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Hangman!")

    main_frame = ttk.Frame(root, padding=40, relief='raised')
    main_frame.grid()

    letter1 = ttk.Label(main_frame, text="____")
    letter1.grid(row=1, column=1)
    letter_entry1 = ttk.Entry(main_frame, width=4)
    letter_entry1.grid(row=0, column=1)

    letter2 = ttk.Label(main_frame, text="____")
    letter2.grid(row=1, column=2)
    letter_entry2 = ttk.Entry(main_frame, width=4)
    letter_entry2.grid(row=0, column=2)

    letter3 = ttk.Label(main_frame, text="____")
    letter3.grid(row=1, column=3)
    letter_entry3 = ttk.Entry(main_frame, width=4)
    letter_entry3.grid(row=0, column=3)

    letter4 = ttk.Label(main_frame, text="____")
    letter4.grid(row=1, column=4)
    letter_entry4 = ttk.Entry(main_frame, width=4)
    letter_entry4.grid(row=0, column=4)

    letter5 = ttk.Label(main_frame, text="____")
    letter5.grid(row=1, column=5)
    letter_entry5 = ttk.Entry(main_frame, width=4)
    letter_entry5.grid(row=0, column=5)

    letter6 = ttk.Label(main_frame, text="____")
    letter6.grid(row=1, column=6)
    letter_entry6 = ttk.Entry(main_frame, width=4)
    letter_entry6.grid(row=0, column=6)

    letter7 = ttk.Label(main_frame, text="____")
    letter7.grid(row=1, column=7)
    letter_entry7 = ttk.Entry(main_frame, width=4)
    letter_entry7.grid(row=0, column=7)

    check_button1 = ttk.Button(main_frame, text='Check!')
    check_button1.grid(row=0, column=9)
    check_button1['command'] = lambda: set_guess(mqtt_client, letter_entry1, letter_entry2, letter_entry3,
                                                letter_entry4, letter_entry5, letter_entry6, letter_entry7)

    root.mainloop()


def set_guess(mqtt_client, letter_entry1, letter_entry2, letter_entry3, letter_entry4,
              letter_entry5, letter_entry6, letter_entry7):
    """ Calls a method on EV3 called 'check_for_answer' passing in a string from the word_to_check_entry. """
    guess = [str(letter_entry1.get()), str(letter_entry2.get()), str(letter_entry3.get()),
             str(letter_entry4.get()), str(letter_entry5.get()), str(letter_entry6.get()),
             str(letter_entry7.get())]
    mqtt_client.send_message("check_for_answer", [guess])
    print('guess sent')


main()
