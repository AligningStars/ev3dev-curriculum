"""
Contains the necessary code run on the pc for user input and selection to
make it run in the desired manner.

The project is that the robot is going on vacation and they are allowed to
select one of three locations to visit. The code then has the robot turn a
desired number of degrees to reach the "location" (really just a color that
the robot has to sense for and then stop when it "arrives"). When the robot
arrives to the desired location, the user is then allowed to control the
robot to use the keys to meander down the road avoiding pedestrains to get
to the downtown of the city!

Author: Sydney Larson
"""
import tkinter
from tkinter import ttk

import ev3dev.ev3 as ev3

import mqtt_remote_method_calls as com

def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    #Setting up the window in which the user is able to decide where they
    # want to go.
    root = tkinter.Tk()
    root.title("Going on Vacation")

    #Defining the style for the tkinter window
    s = ttk.Style()
    s.configure('My.TFrame',background = "#a1dbcd",font=('Candara',12))

    #Defining the style for the buttons on the window
    bs = ttk.Style()
    bs.configure('my.TButton', font=('Candara', 12))

    main_frame = ttk.Frame(root, padding=20,relief='raised',style='My.TFrame')
    main_frame.grid()

    vacation_label = ttk.Label(main_frame, text="Select where you would like to go on vacation:",background = "#a1dbcd",font = ('Candara',15))
    vacation_label.grid(row=0, column=0)

    #Defining the variables that are necessary later in defining the
    # movement of the robot
    speed_to_turn = 600


    #Entry values for the motors when the user is able to use the keyboard
    # to control the movements
    left_speed_entry = ttk.Entry()
    left_speed_entry.insert(0, "600")

    right_speed_entry = ttk.Entry()
    right_speed_entry.insert(0, "600")

    #Variables that hold the values for the turn degrees, whether it be a
    # full 90 degree turn or for when the keys move the robot and the
    # degrees to turn is much smaller
    turn_degrees = 90
    small_turn = 10

    #Setting up the button that directs the robot to go on vacation to Shanghai
    shanghai_button = ttk.Button(main_frame, text="Shanghai",style='my.TButton')
    shanghai_button.grid(row=4, column=0)
    shanghai_button['command'] = lambda: to_shanghai(mqtt_client,
                                                     turn_degrees,
                                                     speed_to_turn,
                                                     ev3.ColorSensor.COLOR_WHITE)

    #Setting up the button that directs the robot to go on vacation to Tokyo
    tokyo_button = ttk.Button(main_frame, text="Tokyo",style='my.TButton')
    tokyo_button.grid(row=5, column=0)
    tokyo_button['command'] = lambda: to_tokyo(mqtt_client,0,
                                                  speed_to_turn,
                                               ev3.ColorSensor.COLOR_BLUE)

    #Setting up the button that directs the robot to go on vacation to Seoul
    seoul_button = ttk.Button(main_frame, text="Seoul",style='my.TButton')
    seoul_button.grid(row=6, column=0)
    seoul_button['command'] = lambda: to_seoul(mqtt_client,
                                                  -turn_degrees,
                                                  speed_to_turn,ev3.ColorSensor.COLOR_RED)

    #Setting up the buttons that will allow the user to control the movement
    #  of the robot.
    root.bind('<Up>', lambda event: send_forward(mqtt_client,
                                                  left_speed_entry,
                                        right_speed_entry))
    root.bind('<Left>', lambda event: send_left(mqtt_client, small_turn,
                                             left_speed_entry))
    root.bind('<s>', lambda event: send_stop(mqtt_client))
    root.bind('<Right>', lambda event: send_right(mqtt_client, -small_turn,
                                               right_speed_entry))
    root.bind('<Down>', lambda event: send_back(mqtt_client, left_speed_entry,
                                             right_speed_entry))

    root.mainloop()

#Defining the functions that tell the robot what to do depending on the
# location that the user selected.

#Function for when the user clicked the Shanghai button
def to_shanghai(mqtt_client,entry,entry1,entry2):
    print("Off to Shanghai")
    mqtt_client.send_message("turn_degrees", [entry,entry1])
    mqtt_client.send_message("drive_to_color",[entry2])
    print("Arrived in Shanghai, China")
    arrived()

#Function for when the user clicked the Tokyo button
def to_tokyo(mqtt_client,entry,entry1,entry2):
    print("Off to Tokyo")
    mqtt_client.send_message("turn_degrees", [entry,entry1])
    mqtt_client.send_message("drive_to_color",[entry2])
    print("Arrived in Tokyo, Japan")
    arrived()

#Function for when the user clicked the Seoul button
def to_seoul(mqtt_client,entry,entry1,entry2):
    print("Off to Seoul")
    mqtt_client.send_message("turn_degrees", [entry,entry1])
    mqtt_client.send_message("drive_to_color",[entry2])
    print("Arrived in Seoul, Korea")
    arrived()

#Defining the functions that control the movements of the robot based upon
# the keys that the user presses.

#Moving the robot forward when the Up key is pressed
def send_forward(mqtt_client, entry, entry1):
    mqtt_client.send_message("drive_forward", [int(entry.get()),
                                               int(entry1.get())])
#Turning the robot 10 degrees to the left when the Left key is pressed
def send_left(mqtt_client, entry, entry1):
    mqtt_client.send_message("turn_degrees", [entry, int(entry1.get())])

#Turning the robot 10 degrees to the right when the Right key is pressed
def send_right(mqtt_client, entry, entry1):
    mqtt_client.send_message("turn_degrees", [entry,
                                              int(entry1.get())])
#Stopping the robots moveemtns when the s button is pressed
def send_stop(mqtt_client):
    mqtt_client.send_message("shutdown")
#Moving the robot backward when the Down key is pressed
def send_back(mqtt_client, entry, entry1):
    mqtt_client.send_message("drive_backward", [int(entry.get()),
                                                int(entry1.get())])
#Calling the shutdown function of the robot to quit the program
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()

#Defining the fucntion that creates a window that says that the user
# 'arrived' to their desired location and the next steps that they should take
def arrived():
#    robot = robo.Snatch3r()

    root = tkinter.Tk()
    root.title("Arrived!")

    main_frame = ttk.Frame(root, padding=20,relief='raised')
    main_frame.grid()

    arrival_label = ttk.Label(main_frame, text="We've arrived! Now let's go "
                                                "downtown, we'll arrive "
                                               "after we avoid these "
                                               "pedestrians!" ,
                               font = ('Candara',15))
    arrival_label.grid(row=0, column=0)

main()