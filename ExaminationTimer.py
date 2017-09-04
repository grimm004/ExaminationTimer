# Examination Timer
# 06/06/2015 | All rights Reserved
# @version: B6.0
# @author Max Grimmett (10.3)

# Imports
import debug
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from os import path, getenv
from datetime import datetime
import configparser
import authenticate_key
import encode_string_general
import time
import math
import re
import gc
import winsound
import threading
import registry

# TODO: Change storage to Database
# TODO: Implement winreg key storage
# TODO: Fix monitor resolutions

# Author Variable
__author__ = 'Max Grimmett'

# Version
__version__ = 6.0

# DEBUG Mode Variable
is_debug = False
if debug.MASTER_DEBUG or debug.ExaminationTimer:
    is_debug = True
__DEBUG__ = is_debug

# If DEBUG mode is on, print more information to the console.
if __DEBUG__:
    print("Examination Timer %s by %s, Debug Mode." % (__version__, __author__))
else:
    print("Examination Timer %s by %s." % (__version__, __author__))

if __DEBUG__:
    print("Managing Imports...")

# Program Access Verification
if __DEBUG__:
    print("Authenticating...")
# Variable that stores if the program has been authenticated in the past, stopping the need to download data again
has_been_authenticated = False
# Licence holder temp variables
user_short = "MG"
user_long = "Max Grimmett"
# Set the data file directory
APP_DATA = getenv('APPDATA')
ROOT_DIR = '\\ExaminationTimer\\'
PRE_EXECUTED_FILE = 'user_data.lic'
CONFIG_FILE = 'config.ini'
LOGO_FILE_NAME = "logo.png"
DIR = str(APP_DATA + ROOT_DIR)
PRE_EXECUTED_FILE_DIR = str(DIR + PRE_EXECUTED_FILE)
LOGO_FILE_DIRECTORY = str(DIR + LOGO_FILE_NAME)
CONFIG_FILE_DIR = str(DIR + CONFIG_FILE)
REG_DIR = "SOFTWARE\ExaminationTimer"
licence_array_bytes = [b"Developer", b"Trial", b"Full", b"Redistributed"]
licence_array = ["Developer", "Trial", "Full", "Redistributed"]
active_licence_index = 0
current_reg_key = registry.get_reg_value(registry.HKEY_CURRENT_USER, REG_DIR, "reg_key")


# Function that calls relevant external functions to authenticate the entered reg key
def authenticate_internal():
    if not has_been_authenticated:
        if authenticate_key.authenticate():
            authenticate_key.write_auth_data()


# Function that checks if the program has been run successfully in the past, and return true if so, else return false
def internal_authenticate():
    global has_been_authenticated, user_short, user_long, active_licence_index
    if path.exists(PRE_EXECUTED_FILE_DIR):
        with open(PRE_EXECUTED_FILE_DIR, 'r') as f:
            file_content = [x.strip('\n') for x in f.readlines()]
            if __DEBUG__:
                print("Data Storage:", file_content)
                print("Licence Index\t Licence Type\tCode")
            if file_content:
                if not current_reg_key or current_reg_key is "":
                    return False
                # Get an encoded version of the licence key with "True " in front of it
                for current_index, current_licence in enumerate(licence_array):
                    encode_string_general.EncodeString(current_licence + current_reg_key)
                    if __DEBUG__:
                        print(current_index, "\t\t\t\t",
                              current_licence, "\t\t", encode_string_general.get_encoded_string_variable())
                    if str(encode_string_general.get_encoded_string_variable()) in str(file_content[0]):
                        active_licence_index = current_index
                        has_been_authenticated = True
                        user_short = file_content[1]
                        user_long = file_content[2]
                        if __DEBUG__:
                            print("Found Match at index " + str(active_licence_index) + ", unpacking information.")
                        return True
                    if current_index > int(len(licence_array)+1):
                        if __DEBUG__:
                            print("End of licence list.")
                        return False
    else:
        return False

# Store the returned value of the internal_authenticate function in allow_launch
allow_launch = internal_authenticate()

# If the internal_authenticate returns false, try to authenticate reg key online
if not allow_launch:
    if __DEBUG__:
        print("Trying to authenticate online...")
    authenticate_internal()
    allow_launch = internal_authenticate()

if __DEBUG__ and allow_launch:
    print("Authentication Success...")
elif __DEBUG__:
    print("Authentication Error...")

# Main Licence Variables
if __DEBUG__:
    print("Creating FINAL Information Storage Variables...")
LICENCE_HOLDER_SHORT = str(user_short)
LICENCE_HOLDER_LONG = str(user_long)
LICENCE_TYPE = str(licence_array[active_licence_index])
if __DEBUG__:
    print("Done!")

# General Configuration
minimum_exam_time = 1800
flash_red_time = 120
# Default Data Entry
default_exam_one_name = "Examination Name"
default_exam_one_time = "HH:MM:SS"
default_exam_one_extra_time = "HH:MM:SS"
default_exam_two_name = ""
default_exam_two_time = ""
default_exam_two_extra_time = ""
default_exam_three_name = ""
default_exam_three_time = ""
default_exam_three_extra_time = ""
default_exam_four_name = ""
default_exam_four_time = ""
default_exam_four_extra_time = ""
# General Colours
main_bg = "#00FFFF"
# Entry Window Colours
input_titles_text = "#000000"
input_titles_background = "#FFFFFF"
input_examination_title_text = "#FFFFFF"
input_examination_title_background = "#0000FF"
input_examination_duration_text = "#000000"
input_examination_duration_background = "#00FF00"
input_examination_extra_time_text = "#000000"
input_examination_extra_time_background = "#00FF00"
input_exit_button_text = "#000000"
input_exit_button_background = "#FF0000"
input_submit_button_text = "#000000"
input_submit_button_background = "#FF0000"
input_voice_sound_button_text = "#000000"
input_voice_sound_button_background = "#00FF00"
# Main Window Colours
titles_text = "#FFFFFF"
titles_backgrounds = "#FFFFFF"
examination_name_text = "#000000"
examination_name_background = "#FF0000"
examination_allowed_time_text = "#000000"
examination_allowed_time_background = "#FF0000"
examination_remaining_time_text = "#000000"
examination_remaining_time_background = "#FF0000"
examination_extra_time_text = "#FF0000"
examination_start_time_text = "#000000"
examination_start_time_background = "#00FF00"
examination_end_time_text = "#000000"
examination_end_time_background = "#FFFF00"
examination_end_plus_extra_time_text = "#000000"
examination_end_time_plus_extra_background = "#FFFF00"
examination_start_button_text = "#000000"
examination_start_button_background = "#00FF00"
examination_start_button_active_background = "#0000FF"
pause_all_button_text = "#000000"
pause_all_button_background = "#00FF00"
pause_all_button_active_background = "#0000FF"
exit_button_text = "#000000"
exit_button_background = "#FF0000"
restart_button_text = "#000000"
restart_button_background = "#FF0000"
# Analogue Clock Colours
analogue_center_point = "#000000"
analogue_second_hand = "#000000"
analogue_minute_hand = "#000000"
analogue_hour_hand = "#000000"
analogue_markers = "#000000"
analogue_outer_ring = "#000000"
# Digital Clock Colours
digital_background_colour = "#FF0000"
digital_text_colour = "#000000"

# Root Window Creation and Configuration
if __DEBUG__:
    print("Setting Up Root Window...")
root = Tk()
root.resizable(width=True, height=True)
LICENCE_HOLDER_SHORT_TITLE_FORMAT = format("Examination Timer %s [%s - %s Licence]"
                                           % (str(__version__), str(LICENCE_HOLDER_SHORT), str(LICENCE_TYPE)))
root.title(LICENCE_HOLDER_SHORT_TITLE_FORMAT)
if __DEBUG__:
    print("Done!")

if __DEBUG__:
    print("Pre-Defining Variables...")


def update_config():
    global minimum_exam_time, flash_red_time
    global default_exam_one_name, default_exam_one_time, default_exam_one_extra_time
    global default_exam_two_name, default_exam_two_time, default_exam_two_extra_time
    global default_exam_three_name, default_exam_three_time, default_exam_three_extra_time
    global default_exam_four_name, default_exam_four_time, default_exam_four_extra_time
    global main_bg, input_titles_text, input_titles_background, input_examination_title_text
    global input_examination_title_background, input_examination_duration_text, input_examination_duration_background
    global input_examination_extra_time_text, input_examination_extra_time_background, input_exit_button_text
    global input_exit_button_background, input_submit_button_text, input_submit_button_background
    global input_voice_sound_button_text, input_voice_sound_button_background, titles_text, titles_backgrounds
    global examination_name_text, examination_name_background, examination_allowed_time_text
    global examination_allowed_time_background, examination_remaining_time_text, examination_remaining_time_background
    global examination_extra_time_text, examination_start_time_text, examination_start_time_background
    global examination_end_time_text, examination_end_time_background, examination_end_plus_extra_time_text
    global examination_end_time_plus_extra_background, examination_start_button_text
    global examination_start_button_background, examination_start_button_active_background, pause_all_button_text
    global pause_all_button_background, pause_all_button_active_background, exit_button_text, exit_button_background
    global restart_button_text, restart_button_background, analogue_center_point, analogue_second_hand
    global analogue_minute_hand, analogue_hour_hand, analogue_markers, analogue_outer_ring
    global digital_background_colour, digital_text_colour

    # Begin User Configuration
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_DIR)

    try:
        main_bg = "#" + config["Colours.General"]["main background"]
        root.configure(background=main_bg)
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        # General Configuration
        minimum_exam_time = int(config["General"]["minimum exam time seconds"])
        flash_red_time = int(config["General"]["flash red time seconds"])
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    # Default Data Entry
    default_data_entry = "Default Data Entry"
    try:
        default_exam_one_name = config[default_data_entry]["exam one name"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_one_time = config[default_data_entry]["exam one time"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_one_extra_time = config[default_data_entry]["exam one extra time"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_two_name = config[default_data_entry]["exam two name"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_two_time = config[default_data_entry]["exam two time"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_two_extra_time = config[default_data_entry]["exam two extra time"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_three_name = config[default_data_entry]["exam three name"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_three_time = config[default_data_entry]["exam three time"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_three_extra_time = config[default_data_entry]["exam three extra time"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_four_name = config[default_data_entry]["exam four name"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_four_time = config[default_data_entry]["exam four time"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        default_exam_four_extra_time = config[default_data_entry]["exam four extra time"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    # Entry Window Colours
    entry_colours = "Colours.Input"
    try:
        input_titles_text = "#" + config[entry_colours]["titles text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_titles_background = "#" + config[entry_colours]["titles background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_examination_title_text = "#" + config[entry_colours]["examination title text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_examination_title_background = "#" + config[entry_colours]["examination title background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_examination_duration_text = "#" + config[entry_colours]["examination duration text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_examination_duration_background = "#" + config[entry_colours]["examination duration background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_examination_extra_time_text = "#" + config[entry_colours]["examination extra time text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_examination_extra_time_background = "#" + config[entry_colours]["examination extra time background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_exit_button_text = "#" + config[entry_colours]["exit button text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_exit_button_background = "#" + config[entry_colours]["exit button background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_submit_button_text = "#" + config[entry_colours]["submit button text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_submit_button_background = "#" + config[entry_colours]["submit button background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_voice_sound_button_text = "#" + config[entry_colours]["voice sound button text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        input_voice_sound_button_background = "#" + config[entry_colours]["voice sound button background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    # Main Window Colours
    main_colours = "Colours.Main"
    try:
        titles_text = "#" + config[main_colours]["titles text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        titles_backgrounds = "#" + config[main_colours]["titles background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_name_text = "#" + config[main_colours]["examination name text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_name_background = "#" + config[main_colours]["examination name background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_allowed_time_text = "#" + config[main_colours]["examination allowed time text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_allowed_time_background = "#" + config[main_colours]["examination allowed time background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_remaining_time_text = "#" + config[main_colours]["examination remaining time text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_remaining_time_background = "#" + config[main_colours]["examination remaining time background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_extra_time_text = "#" + config[main_colours]["examination extra time text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_start_time_text = "#" + config[main_colours]["examination start time text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_start_time_background = "#" + config[main_colours]["examination start time background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_end_time_text = "#" + config[main_colours]["examination end time text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_end_time_background = "#" + config[main_colours]["examination end time background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_end_plus_extra_time_text = "#" + config[main_colours]["examination end plus extra time text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_end_time_plus_extra_background = "#" +\
                                                     config[main_colours]["examination end time plus extra background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_start_button_text = "#" + config[main_colours]["examination start button text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_start_button_background = "#" + config[main_colours]["examination start button background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        examination_start_button_active_background = "#" +\
                                                     config[main_colours]["examination start button active background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        pause_all_button_text = "#" + config[main_colours]["pause all button text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        pause_all_button_background = "#" + config[main_colours]["pause all button background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        pause_all_button_active_background = "#" + config[main_colours]["pause all button active background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        exit_button_text = "#" + config[main_colours]["exit button text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        exit_button_background = "#" + config[main_colours]["exit button background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        restart_button_text = "#" + config[main_colours]["restart button text"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        restart_button_background = "#" + config[main_colours]["restart button background"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    # Analogue Clock Colours
    analogue_colours = "Colours.Clocks.Analogue"
    try:
        analogue_center_point = "#" + config[analogue_colours]["center point"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        analogue_second_hand = "#" + config[analogue_colours]["second hand"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        analogue_minute_hand = "#" + config[analogue_colours]["minute hand"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        analogue_hour_hand = "#" + config[analogue_colours]["hour hand"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        analogue_markers = "#" + config[analogue_colours]["markers"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        analogue_outer_ring = "#" + config[analogue_colours]["outer ring"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    # Digital Clock Colours
    digital_colours = "Colours.Clocks.Digital"
    try:
        digital_background_colour = "#" + config[digital_colours]["background colour"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")
    try:
        digital_text_colour = "#" + config[digital_colours]["text colour"]
    except KeyError:
        if __DEBUG__:
            print("KeyError Occurred")

# Pre-Defining Variables
# Number of exams there will be
number_of_exams = 1

# Number of exams that have started
number_of_started_exams = 0

# Number of exams that have started as a result of the start_all_button
number_of_start_all_exams = 0

# Number of exams that have stopped
number_of_stopped_exams = 0

# Number of exams that require sounds
number_of_exams_that_need_five_min_sound = number_of_exams_that_need_end_sound = 0

# Variable that stores if the program has restarted or not
has_restarted = False

# Variable that allows the timer to update
allow_update = False

# Variable that allows exam times to update
allow_one = allow_two = allow_three = allow_four = False

# Variable that allows exam extra times to update
allow_extra_one = allow_extra_two = allow_extra_three = allow_extra_four = False

# Variable that allows the clock to update
allow_clock = False

# Variable that allows the check_start_all function to be run
allow_check_start_all = True

# Variables that store whether sound should be played on exam start
allow_sound_one = allow_sound_two = allow_sound_three = allow_sound_four = True

# Variables that store whether the exams contain data or not
one_has_data = two_has_data = three_has_data = four_has_data = False

# Variables that store whether the exams have extra time over 00:00:01
one_has_extra_time = two_has_extra_time = three_has_extra_time = four_has_extra_time = False

# Variables that store whether the exams have started or not
one_has_started = two_has_started = three_has_started = four_has_started = False

# Variables that store whether individual exams have been started using the start all button or not
one_start_all = two_start_all = three_start_all = four_start_all = False

# Variables that store whether the exams have finished or not
one_has_finished = two_has_finished = three_has_finished = four_has_finished = False

# Variables that store information to do with flashing red at the end for two minutes
continue_count_one = continue_count_two = continue_count_three = continue_count_four = False

red_flash_one = red_flash_two = red_flash_three = red_flash_four = False

red_flash_one_t = red_flash_two_t = red_flash_three_t = red_flash_four_t = 0

# Variables that store the number of completed exams
number_of_completed_exams = 0

# Variable that stores whether the user wants the voice sound to play or not
allow_voice_sound = False

# Variable that stores whether all examinations are paused or not
all_paused = False

# Variables that store the allowed time for the exams
e1_allowed_time = e2_allowed_time = e3_allowed_time = e4_allowed_time = 0

# Variables that store how long pauses last for
e1_pause_time = e2_pause_time = e3_pause_time = e4_pause_time = 0

# Variables that store how long pauses last for in extra time
e1_pause_extra_time = e2_pause_extra_time = e3_pause_extra_time = e4_pause_extra_time = 0

# Variables that store any allowed extra time for the exams
e1_allowed_extra_time = e2_allowed_extra_time = e3_allowed_extra_time = e4_allowed_extra_time = 0

# Variables that store the total time for each exam (normal time plus extra time)
e1_total_time = e2_total_time = e3_total_time = e4_total_time = 0
if __DEBUG__:
    print("Done!")

if __DEBUG__:
    print("Defining Functions and Classes...")


# Exit Function
def exit_program():
    global allow_update
    if __DEBUG__:
        print("Exiting Program...")
    allow_update = False
    root.destroy()
    root.quit()


# Classes
# Class Object for resetting all the above variables
class Restart:
    def __init__(self):
        # Allowing the function to use the global variables
        global number_of_exams, number_of_start_all_exams, number_of_started_exams, number_of_stopped_exams
        global number_of_exams_that_need_five_min_sound, number_of_exams_that_need_end_sound
        global has_restarted, allow_update
        global allow_one, allow_two, allow_three, allow_four
        global allow_extra_one, allow_extra_two, allow_extra_three, allow_extra_four
        global allow_clock, allow_check_start_all
        global allow_sound_one, allow_sound_two, allow_sound_three, allow_sound_four
        global one_has_extra_time, two_has_extra_time, three_has_extra_time, four_has_extra_time
        global one_has_data, two_has_data, three_has_data, four_has_data
        global one_has_started, two_has_started, three_has_started, four_has_started
        global one_start_all, two_start_all, three_start_all, four_start_all
        global one_has_finished, two_has_finished, three_has_finished, four_has_finished
        global continue_count_one, continue_count_two, continue_count_three, continue_count_four
        global red_flash_one, red_flash_two, red_flash_three, red_flash_four
        global red_flash_one_t, red_flash_two_t, red_flash_three_t, red_flash_four_t
        global number_of_completed_exams, allow_voice_sound, all_paused
        global e1_allowed_time, e2_allowed_time, e3_allowed_time, e4_allowed_time
        global e1_pause_time, e2_pause_time, e3_pause_time, e4_pause_time
        global e1_pause_extra_time, e2_pause_extra_time, e3_pause_extra_time, e4_pause_extra_time
        global e1_allowed_extra_time, e2_allowed_extra_time, e3_allowed_extra_time, e4_allowed_extra_time
        global e1_total_time, e2_total_time, e3_total_time, e4_total_time

        # Re-Defining Variables
        # Number of exams there will be
        number_of_exams = 1

        # Number of exams that have started
        number_of_started_exams = 0

        # Number of exams that have started as a result of the start_all_button
        number_of_start_all_exams = 0

        # Number of exams that have stopped
        number_of_stopped_exams = 0

        # Number of exams that require sounds
        number_of_exams_that_need_five_min_sound = number_of_exams_that_need_end_sound = 0

        # Variable that stores if the program has restarted or not
        has_restarted = False

        # Variable that allows the timer to update
        allow_update = False

        # Variable that allows exam times to update
        allow_one = allow_two = allow_three = allow_four = False

        # Variable that allows exam extra times to update
        allow_extra_one = allow_extra_two = allow_extra_three = allow_extra_four = False

        # Variable that allows the clock to update
        allow_clock = False

        # Variable that allows the check_start_all function to be run
        allow_check_start_all = True

        # Variables that store whether sound should be played on exam start
        allow_sound_one = allow_sound_two = allow_sound_three = allow_sound_four = True

        # Variables that store whether the exams contain data or not
        one_has_data = two_has_data = three_has_data = four_has_data = False

        # Variables that store whether the exams have extra time over 00:00:01
        one_has_extra_time = two_has_extra_time = three_has_extra_time = four_has_extra_time = False

        # Variables that store whether the exams have started or not
        one_has_started = two_has_started = three_has_started = four_has_started = False

        # Variables that store whether individual exams have been started using the start all button or not
        one_start_all = two_start_all = three_start_all = four_start_all = False

        # Variables that store whether the exams have finished or not
        one_has_finished = two_has_finished = three_has_finished = four_has_finished = False

        # Variables that store information to do with flashing red at the end for two minutes
        continue_count_one = continue_count_two = continue_count_three = continue_count_four = False

        red_flash_one = red_flash_two = red_flash_three = red_flash_four = False

        red_flash_one_t = red_flash_two_t = red_flash_three_t = red_flash_four_t = 0

        # Variables that store the number of completed exams
        number_of_completed_exams = 0

        # Variable that stores whether all examinations are paused or not
        all_paused = False

        # Variables that store the allowed time for the exams
        e1_allowed_time = e2_allowed_time = e3_allowed_time = e4_allowed_time = 0

        # Variables that store how long pauses last for
        e1_pause_time = e2_pause_time = e3_pause_time = e4_pause_time = 0

        # Variables that store how long pauses last for in extra time
        e1_pause_extra_time = e2_pause_extra_time = e3_pause_extra_time = e4_pause_extra_time = 0

        # Variables that store any allowed extra time for the exams
        e1_allowed_extra_time = e2_allowed_extra_time = e3_allowed_extra_time = e4_allowed_extra_time = 0

        # Variables that store the total time for each exam (normal time plus extra time)
        e1_total_time = e2_total_time = e3_total_time = e4_total_time = 0

        self.restart()

    @staticmethod
    def restart():
        # FirstScreen Class Initialization
        input_screen.start()


# Class Object for Sounds
class Sounds:
    # Declare as Static
    @staticmethod
    def change_allow_voice_sounds(button):
        # Declare global used variable
        global allow_voice_sound
        # If allow_voice_sound is true, change pre-made button text, set variable to false
        if allow_voice_sound:
            if __DEBUG__:
                print("Voice Sound Disabled.")
            button.configure(text="Voice Sound Disabled")
            allow_voice_sound = False
        # If allow_voice_sound is false, change pre-made button text, set variable to true
        else:
            if __DEBUG__:
                print("Voice Sound Allowed.")
            button.configure(text="Voice Sound Allowed")
            allow_voice_sound = True

    @staticmethod
    def start_sound():
        if __DEBUG__:
            print("Playing Start Sound...")
        # Create a 500Hz beep for 1/2 a second
        winsound.Beep(500, 500)
        # If the voice sound is allowed, play a voice sound
        if allow_voice_sound:
            winsound.PlaySound('YMS.wav', winsound.SND_FILENAME)
        if __DEBUG__:
            print("Done!")

    @staticmethod
    def five_min_sound():
        if __DEBUG__:
            print("Playing Five Minute Sound...")
        winsound.Beep(750, 205)
        time.sleep(0.2)
        winsound.Beep(750, 205)
        time.sleep(0.2)
        winsound.Beep(750, 205)
        if allow_voice_sound:
            winsound.PlaySound('5MR.wav', winsound.SND_FILENAME)
        if __DEBUG__:
            print("Done!")

    @staticmethod
    def end_sound():
        if __DEBUG__:
            print("Playing End Sound...")
        winsound.Beep(500, 1000)
        if allow_voice_sound:
            winsound.PlaySound('EOE.wav', winsound.SND_FILENAME)
        if __DEBUG__:
            print("Done!")


# Class Object for the First Screen
class Input:
    def __init__(self, frame):
        if __DEBUG__:
            print("Initializing Variables and Widgets...")

        # Initialize Frame
        self.frame = frame

        # String Entry Variables
        # Note: These cannot be stacked, as they are treated separate objects not values
        self.e1n = StringVar()
        self.e2n = StringVar()
        self.e3n = StringVar()
        self.e4n = StringVar()

        self.e1t = StringVar()
        self.e2t = StringVar()
        self.e3t = StringVar()
        self.e4t = StringVar()

        self.ee1t = StringVar()
        self.ee2t = StringVar()
        self.ee3t = StringVar()
        self.ee4t = StringVar()

        # Colour Storage Variables
        self.TITLE_LABEL_BACKGROUND_C = input_titles_background
        self.NAME_LABEL_BACKGROUND_C = input_examination_title_background
        self.TIME_LABEL_BACKGROUND_C = input_examination_duration_background
        self.EXTRA_TIME_LABEL_BACKGROUND_C = input_examination_extra_time_background
        self.NAME_LABEL_FOREGROUND_C = input_examination_title_text

        # Size Storage Variables
        # Width Storage Variables
        self.NAME_LABEL_WIDTH = 25
        self.NAME_TITLE_LABEL_WIDTH = 23
        self.NAME_COLUMN_WIDTH = 45
        self.TIME_TITLE_LABEL_WIDTH = 9
        self.TIME_LABEL_WIDTH = 12
        self.TIME_COLUMN_WIDTH = 16

        # Height Storage Variables
        self.nameLabelHeight = 2

        # Filler Widgets
        # Main Frame
        Label(frame, height=self.nameLabelHeight, width=self.NAME_COLUMN_WIDTH, bg=main_bg)\
            .grid(row=0, column=0, columnspan=2)
        Label(frame, height=self.nameLabelHeight, bg=main_bg).grid(row=1, column=0, columnspan=2)
        Label(frame, height=self.nameLabelHeight, bg=main_bg).grid(row=2, column=0, columnspan=2)
        Label(frame, height=self.nameLabelHeight, bg=main_bg).grid(row=3, column=0, columnspan=2)
        Label(frame, height=self.nameLabelHeight, bg=main_bg).grid(row=4, column=0, columnspan=2)
        Label(frame, height=self.nameLabelHeight, bg=main_bg).grid(row=5, column=0, columnspan=2)
        Label(frame, height=self.nameLabelHeight, width=self.TIME_COLUMN_WIDTH, bg=main_bg).grid(row=0, column=2)
        Label(frame, height=self.nameLabelHeight, width=self.TIME_COLUMN_WIDTH, bg=main_bg).grid(row=0, column=3)

        # Titles
        exam_title_label = Label(frame, width=self.NAME_TITLE_LABEL_WIDTH, bd=2, relief=GROOVE,
                                 fg=input_titles_text, font=("Arial", 16), text="Exam Title",
                                 bg=self.TITLE_LABEL_BACKGROUND_C)
        exam_time_label = Label(frame, width=self.TIME_TITLE_LABEL_WIDTH, bd=2, relief=GROOVE,
                                fg=input_titles_text, font=("Arial", 16), text="Duration",
                                bg=self.TITLE_LABEL_BACKGROUND_C)
        exam_extra_time_label = Label(frame, width=self.TIME_TITLE_LABEL_WIDTH, bd=2, relief=GROOVE,
                                      fg=input_titles_text, font=("Arial", 16), text="Extra Time",
                                      bg=self.TITLE_LABEL_BACKGROUND_C)

        self.timeEntryWidth = 10

        # Exam Name
        exam_one_name = Entry(frame, width=self.NAME_LABEL_WIDTH, bd=2, relief=GROOVE, font=("Arial", 14),
                              fg=self.NAME_LABEL_FOREGROUND_C, bg=self.NAME_LABEL_BACKGROUND_C, textvariable=self.e1n)
        exam_two_name = Entry(frame, width=self.NAME_LABEL_WIDTH, bd=2, relief=GROOVE, font=("Arial", 14),
                              fg=self.NAME_LABEL_FOREGROUND_C, bg=self.NAME_LABEL_BACKGROUND_C, textvariable=self.e2n)
        exam_three_name = Entry(frame, width=self.NAME_LABEL_WIDTH, bd=2, relief=GROOVE, font=("Arial", 14),
                                fg=self.NAME_LABEL_FOREGROUND_C, bg=self.NAME_LABEL_BACKGROUND_C, textvariable=self.e3n)
        exam_four_name = Entry(frame, width=self.NAME_LABEL_WIDTH, bd=2, relief=GROOVE, font=("Arial", 14),
                               fg=self.NAME_LABEL_FOREGROUND_C, bg=self.NAME_LABEL_BACKGROUND_C, textvariable=self.e4n)

        self.e1n.set(default_exam_one_name)
        self.e2n.set(default_exam_two_name)
        self.e3n.set(default_exam_three_name)
        self.e4n.set(default_exam_four_name)

        # Main Time
        exam_one_time = Entry(frame, justify=CENTER, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                              font=("Arial", 13), bg=self.TIME_LABEL_BACKGROUND_C, textvariable=self.e1t,
                              fg=input_examination_duration_text)
        exam_two_time = Entry(frame, justify=CENTER, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                              font=("Arial", 13), bg=self.TIME_LABEL_BACKGROUND_C, textvariable=self.e2t,
                              fg=input_examination_duration_text)
        exam_three_time = Entry(frame, justify=CENTER, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                font=("Arial", 13), bg=self.TIME_LABEL_BACKGROUND_C, textvariable=self.e3t,
                                fg=input_examination_duration_text)
        exam_four_time = Entry(frame, justify=CENTER, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                               font=("Arial", 13), bg=self.TIME_LABEL_BACKGROUND_C, textvariable=self.e4t,
                               fg=input_examination_duration_text)

        self.e1t.set(default_exam_one_time)
        self.e2t.set(default_exam_two_time)
        self.e3t.set(default_exam_three_time)
        self.e4t.set(default_exam_four_time)

        # Extra Time
        exam_one_extra_time = Entry(frame, justify=CENTER, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                    font=("Arial", 13), bg=self.EXTRA_TIME_LABEL_BACKGROUND_C, textvariable=self.ee1t,
                                    fg=input_examination_extra_time_text)
        exam_two_extra_time = Entry(frame, justify=CENTER, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                    font=("Arial", 13), bg=self.EXTRA_TIME_LABEL_BACKGROUND_C, textvariable=self.ee2t,
                                    fg=input_examination_extra_time_text)
        exam_three_extra_time = Entry(frame, justify=CENTER, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                      font=("Arial", 13), bg=self.EXTRA_TIME_LABEL_BACKGROUND_C, textvariable=self.ee3t,
                                      fg=input_examination_extra_time_text)
        exam_four_extra_time = Entry(frame, justify=CENTER, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                     font=("Arial", 13), bg=self.EXTRA_TIME_LABEL_BACKGROUND_C, textvariable=self.ee4t,
                                     fg=input_examination_extra_time_text)

        self.ee1t.set(default_exam_one_extra_time)
        self.ee2t.set(default_exam_two_extra_time)
        self.ee3t.set(default_exam_three_extra_time)
        self.ee4t.set(default_exam_four_extra_time)

        # Test Beep ttk.Button
        allow_voice_sound_button = ttk.Button(frame,
                                          text="Voice Sound Disabled",
                                          command=lambda: Sounds.change_allow_voice_sounds(allow_voice_sound_button))

        update_config_button = ttk.Button(frame,
                                      text="Update Config",
                                      command=self.update_config)

        # Exit ttk.Button
        exit_button = ttk.Button(frame,
                             text="Exit Program",
                             command=exit_program)

        # Standby ttk.Button
        standby_button = ttk.Button(frame,
                                text="Standby",
                                command=self.validate_data)
        if __DEBUG__:
            print("Done!")

        # Add Widgets to the Screen
        if __DEBUG__:
            print("Adding Widgets to Frame!")
        exam_title_label.grid(row=0, column=0, columnspan=2)
        exam_time_label.grid(row=0, column=2)
        exam_extra_time_label.grid(row=0, column=3)

        exam_one_name.grid(row=1, column=0, columnspan=2)
        exam_two_name.grid(row=2, column=0, columnspan=2)
        exam_three_name.grid(row=3, column=0, columnspan=2)
        exam_four_name.grid(row=4, column=0, columnspan=2)

        exam_one_time.grid(row=1, column=2)
        exam_two_time.grid(row=2, column=2)
        exam_three_time.grid(row=3, column=2)
        exam_four_time.grid(row=4, column=2)

        exam_one_extra_time.grid(row=1, column=3)
        exam_two_extra_time.grid(row=2, column=3)
        exam_three_extra_time.grid(row=3, column=3)
        exam_four_extra_time.grid(row=4, column=3)

        allow_voice_sound_button.grid(row=5, column=0)
        update_config_button.grid(row=5, column=1)

        exit_button.grid(row=5, column=2)

        standby_button.grid(row=5, column=3)
        if __DEBUG__:
            print("Done!")

    def start(self):
        self.frame.grid(row=0, column=1)

    # Function that validates entered data
    def validate_data(self):
        # Declare global variables
        global one_has_data, two_has_data, three_has_data, four_has_data
        global one_has_extra_time, two_has_extra_time, three_has_extra_time, four_has_extra_time
        global e1_allowed_time, e2_allowed_time, e3_allowed_time, e4_allowed_time
        global e1_total_time, e2_total_time, e3_total_time, e4_total_time
        global e1_allowed_extra_time, e2_allowed_extra_time, e3_allowed_extra_time, e4_allowed_extra_time
        global number_of_exams

        # Set initial variables
        one_pass = False
        initial_pass = False

        number_of_exams = 0

        # Build Format for Time
        time_format = re.compile(r'\d\d:\d\d:\d\d')

        # Check Formatting and Names
        # Exam 1
        # This checks if data is entered, and if so, then if that data has the correct format
        if time_format.match(self.e1t.get()) is not None \
                and time_format.match(self.ee1t.get()) is not None \
                and self.e1n.get() is not "":
            # If tests pass and have data, set some later used variables (that show the data has passed with data)
            one_has_data = True
            one_pass = True
            number_of_exams += 1
        elif len(self.e1n.get()) == 0 or len(self.ee1t.get()) == 0 or len(self.e1t.get()) == 0:
            # If nothing is entered, set variable that shows if one has data or not
            one_has_data = False
            # Not sure why I put this code here but it is
            if time_format.match(self.e1t.get()) is not None \
                    and time_format.match(self.ee1t.get()) is not None:
                one_pass = True
        else:
            # If anything else happens, stop program continuing
            one_pass = False
            
        # Exam 2
        if time_format.match(self.e2t.get()) is not None \
                and time_format.match(self.ee2t.get()) is not None \
                and self.e2n.get() is not "":
            two_has_data = True
            two_pass = True
            number_of_exams += 1
        elif len(self.e2n.get()) == 0 and len(self.ee2t.get()) == 0 and len(self.e2t.get()) == 0:
            two_pass = True
        else:
            two_pass = False
            
        # Exam 3
        if time_format.match(self.e3t.get()) is not None \
                and time_format.match(self.ee3t.get()) is not None \
                and self.e3n.get() is not "":
            three_has_data = True
            three_pass = True
            number_of_exams += 1
        elif len(self.e3n.get()) == 0 and len(self.ee3t.get()) == 0 and len(self.e3t.get()) == 0:
            three_pass = True
        else:
            three_pass = False
            
        # Exam 4
        if time_format.match(self.e4t.get()) is not None \
                and time_format.match(self.ee4t.get()) is not None \
                and self.e4n.get() is not "":
            four_has_data = True
            four_pass = True
            number_of_exams += 1
        elif len(self.e4n.get()) == 0 and len(self.ee4t.get()) == 0 and len(self.e4t.get()) == 0:
            four_pass = True
        else:
            four_pass = False
        
        # Check if the syntax (format) for all exams passe
        if one_has_data and one_pass:
            if __DEBUG__:
                print("one_has_data:", one_has_data, "one_pass:", one_pass)
            if one_pass and two_pass and three_pass and four_pass:
                if __DEBUG__:
                    print("Initial Validation Success!")
                initial_pass = True
            else:
                initial_pass = False
                messagebox.showinfo("Formatting Error",
                                    "Insure exams have names, and that you have entered times in the format: HH:MM:SS")
        elif one_has_data is False and one_pass:
            if __DEBUG__:
                print("one_has_data:", one_has_data, "one_pass:", one_pass)
            initial_pass = False
            messagebox.showinfo("Error", "Make sure you have at leased one exam in the first box!")
        elif one_has_data is False and one_pass is False:
            if __DEBUG__:
                print("one_has_data:", one_has_data, "one_pass:", one_pass)
            initial_pass = False
            messagebox.showinfo("Formatting Error",
                                "Insure exams have names, and that you have entered times in the format: HH:MM:SS")

        # Allows following code to be executed if initial_pass is true
        if initial_pass is True:
            # Get Strings Entered in the Time Entry Fields
            e1t_t = self.e1t.get()
            e2t_t = self.e2t.get()
            e3t_t = self.e3t.get()
            e4t_t = self.e4t.get()

            ee1t_t = self.ee1t.get()
            ee2t_t = self.ee2t.get()
            ee3t_t = self.ee3t.get()
            ee4t_t = self.ee4t.get()

            # Variables that handles if minute values are less than 30
            one_pass_a = True
            two_pass_a = True
            three_pass_a = True
            four_pass_a = True

            # Variables that handle if minute or second values are >= 60
            one_pass_b = True
            two_pass_b = True
            three_pass_b = True
            four_pass_b = True

            # Extract Time from Variables
            # Exam 1
            # If one has data, extract that data from longer string variables and put them in variables as seconds
            if one_has_data:
                e1th = int(e1t_t[0:2])
                e1tm = int(e1t_t[3:5])
                e1ts = int(e1t_t[6:8])

                ee1h = int(ee1t_t[0:2])
                ee1m = int(ee1t_t[3:5])
                ee1s = int(ee1t_t[6:8])

                e1_allowed_time = (e1th * 60**2) + (e1tm * 60) + e1ts
                e1_allowed_extra_time = (ee1h * 60**2) + (ee1m * 60) + ee1s

                e1_total_time = e1_allowed_time + e1_allowed_extra_time

                # Check the times entered are valid as times
                if e1_allowed_time < minimum_exam_time:
                    one_pass_a = False
                if e1tm >= 60 or e1ts >= 60:
                    one_pass_b = False

                if ee1h > 00 or ee1m > 00 or ee1s > 00:
                    one_has_extra_time = True
                    if __DEBUG__:
                        print("One Has Extra Time")
                if ee1m >= 60 or ee1s >= 60:
                    one_pass_b = False

            # Exam 2
            if two_has_data:
                e2th = int(e2t_t[0:2])
                e2tm = int(e2t_t[3:5])
                e2ts = int(e2t_t[6:8])

                ee2h = int(ee2t_t[0:2])
                ee2m = int(ee2t_t[3:5])
                ee2s = int(ee2t_t[6:8])

                e2_allowed_time = (e2th * 60**2) + (e2tm * 60) + e2ts
                e2_allowed_extra_time = (ee2h * 60**2) + (ee2m * 60) + ee2s

                e2_total_time = e2_allowed_time + e2_allowed_extra_time

                if e2_allowed_time < minimum_exam_time:
                    two_pass_a = False
                if e2tm >= 60 or e2ts >= 60:
                    two_pass_b = False

                if ee2h > 00 or ee2m > 00 or ee2s > 00:
                    two_has_extra_time = True
                    if __DEBUG__:
                        print("two Has Extra Time")
                if ee2m >= 60 or ee2s >= 60:
                    two_pass_b = False

            # Exam 3
            if three_has_data:
                e3th = int(e3t_t[0:2])
                e3tm = int(e3t_t[3:5])
                e3ts = int(e3t_t[6:8])

                ee3h = int(ee3t_t[0:2])
                ee3m = int(ee3t_t[3:5])
                ee3s = int(ee3t_t[6:8])

                e3_allowed_time = (e3th * 60**2) + (e3tm * 60) + e3ts
                e3_allowed_extra_time = (ee3h * 60**2) + (ee3m * 60) + ee3s

                e3_total_time = e3_allowed_time + e3_allowed_extra_time

                if e3_allowed_time < minimum_exam_time:
                    three_pass_a = False
                if e3tm >= 60 or e3ts >= 60:
                    three_pass_b = False

                if ee3h > 00 or ee3m > 00 or ee3s > 00:
                    three_has_extra_time = True
                    if __DEBUG__:
                        print("three Has Extra Time")
                if ee3m >= 60 or ee3s >= 60:
                    three_pass_b = False

            # Exam 4
            if four_has_data:
                e4th = int(e4t_t[0:2])
                e4tm = int(e4t_t[3:5])
                e4ts = int(e4t_t[6:8])

                ee4h = int(ee4t_t[0:2])
                ee4m = int(ee4t_t[3:5])
                ee4s = int(ee4t_t[6:8])

                e4_allowed_time = (e4th * 60**2) + (e4tm * 60) + e4ts
                e4_allowed_extra_time = (ee4h * 60**2) + (ee4m * 60) + ee4s

                e4_total_time = e4_allowed_time + e4_allowed_extra_time

                if e4_allowed_time < minimum_exam_time:
                    four_pass_a = False
                if e4tm >= 60 or e4ts >= 60:
                    four_pass_b = False

                if ee4h > 00 or ee4m > 00 or ee4s > 00:
                    four_has_extra_time = True
                    if __DEBUG__:
                        print("four Has Extra Time")
                if ee4m >= 60 or ee4s >= 60:
                    four_pass_b = False

            # Check that all exams pass time value requirements and return error message if not
            if one_pass_a and two_pass_a and three_pass_a and four_pass_a and \
                    one_pass_b and two_pass_b and three_pass_b and four_pass_b:
                self.main_window()  # Setup main (exam) window
            elif one_pass_a is False or two_pass_a is False or three_pass_a is False or four_pass_a is False:
                messagebox.showinfo("Error!", "Exam durations must be %s seconds or more!" % str(minimum_exam_time))
            elif one_pass_b is False or two_pass_b is False or three_pass_b is False or four_pass_b is False:
                messagebox.showinfo("Error!", "The second and the minute durations must be a value of 59 or less!")
            else:
                messagebox.showinfo("Error!", "Something has gone wrong!")

    @staticmethod
    def update_config():
        if licence_array[active_licence_index] is not licence_array[1]:
            update_config()
            messagebox.showwarning("Configuration",
                                   "Configuration Updated!\nPlease restart program for full functionality.")
        else:
            messagebox.showwarning("Configuration Error",
                                   "Error\nA full licence is required to use configuration.")

    # Function that sets up the next (exam) window
    def main_window(self):
        # Remove Old Frame
        self.frame.grid_remove()

        # Start Second Screen
        main_screen.start()


# Class Object for the Second Screen
class SecondScreen:
    def __init__(self, frame):
        # Frame
        self.frame = frame

        self.e1hd = one_has_data
        self.e2hd = two_has_data
        self.e3hd = three_has_data
        self.e4hd = four_has_data

        # Variable for later controlling part of the updater
        self.allow_completed_exam_code = True

        # Colour Storage Variables
        self.TITLE_LABEL_BACKGROUND_C = titles_backgrounds
        self.NAME_LABEL_BACKGROUND_C = examination_name_background
        self.ALLOWED_TIME_LABEL_BACKGROUND_C = examination_allowed_time_background
        self.REMAINING_TIME_LABEL_BACKGROUND_C = examination_remaining_time_background
        self.EXTRA_TIME_LABEL_BACKGROUND_C = examination_extra_time_text
        self.START_TIME_LABEL_BACKGROUND_C = examination_start_time_background
        self.END_TIME_LABEL_BACKGROUND_C = examination_end_time_background
        self.EXTRA_END_TIME_LABEL_BACKGROUND_C = examination_end_time_plus_extra_background

        # Size Storage Variables
        # Width Storage Variables
        self.NAME_LABEL_WIDTH = 25
        self.NAME_TITLE_LABEL_WIDTH = 23
        self.NAME_COLUMN_WIDTH = 45
        self.TIME_TITLE_LABEL_WIDTH = 9
        self.TIME_LABEL_WIDTH = 12
        self.TIME_COLUMN_WIDTH = 16

        # Height Storage Variables
        self.NAME_COLUMN_HEIGHT = 2

        # Filler Widgets
        # Main Frame
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, width=self.NAME_COLUMN_WIDTH, bg=main_bg)\
            .grid(row=0, column=0, columnspan=2)
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, bg=main_bg)\
            .grid(row=1, column=0)
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, bg=main_bg)\
            .grid(row=2, column=0)
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, bg=main_bg)\
            .grid(row=3, column=0)
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, bg=main_bg)\
            .grid(row=4, column=0)
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, bg=main_bg)\
            .grid(row=5, column=0)
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, width=self.TIME_COLUMN_WIDTH, bg=main_bg)\
            .grid(row=0, column=2)
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, width=self.TIME_COLUMN_WIDTH, bg=main_bg)\
            .grid(row=0, column=3)
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, width=self.TIME_COLUMN_WIDTH, bg=main_bg)\
            .grid(row=0, column=4)
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, width=self.TIME_COLUMN_WIDTH, bg=main_bg)\
            .grid(row=0, column=5)
        Label(self.frame, height=self.NAME_COLUMN_HEIGHT, width=self.TIME_COLUMN_WIDTH, bg=main_bg)\
            .grid(row=0, column=6)

        # Titles
        exam_title_label = Label(self.frame, width=self.NAME_TITLE_LABEL_WIDTH, bd=2, relief=GROOVE,
                                 font=("Arial", 16), text="Examination", bg=self.TITLE_LABEL_BACKGROUND_C)
        exam_allowed_time_label = Label(self.frame, width=self.TIME_TITLE_LABEL_WIDTH, bd=2, relief=GROOVE,
                                        font=("Arial", 16), text="Allowed", bg=self.TITLE_LABEL_BACKGROUND_C)
        exam_remaining_time_label = Label(self.frame, width=self.TIME_TITLE_LABEL_WIDTH, bd=2, relief=GROOVE,
                                          font=("Arial", 16), text="Remaining", bg=self.TITLE_LABEL_BACKGROUND_C)
        exam_start_time_label = Label(self.frame, width=self.TIME_TITLE_LABEL_WIDTH, bd=2, relief=GROOVE,
                                      font=("Arial", 16), text="Start Time", bg=self.TITLE_LABEL_BACKGROUND_C)
        exam_end_time_label = Label(self.frame, width=self.TIME_TITLE_LABEL_WIDTH, bd=2, relief=GROOVE,
                                    font=("Arial", 16), text="End Time", bg=self.TITLE_LABEL_BACKGROUND_C)
        exam_end_extra_time_label = Label(self.frame, width=self.TIME_TITLE_LABEL_WIDTH, bd=2, relief=GROOVE,
                                          font=("Arial", 16), text="Plus Extra", bg=self.TITLE_LABEL_BACKGROUND_C)

        # Exam Name
        self.exam_one_name = Label(self.frame, width=self.NAME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                   font=("Arial", 14), text="", bg=self.NAME_LABEL_BACKGROUND_C)
        self.exam_two_name = Label(self.frame, width=self.NAME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                   font=("Arial", 14), text="", bg=self.NAME_LABEL_BACKGROUND_C)
        self.exam_three_name = Label(self.frame, width=self.NAME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                     font=("Arial", 14), text="", bg=self.NAME_LABEL_BACKGROUND_C)
        self.exam_four_name = Label(self.frame, width=self.NAME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                    font=("Arial", 14), text="", bg=self.NAME_LABEL_BACKGROUND_C)

        # Main Time
        self.exam_one_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                   font=("Arial", 13), text="", bg=self.ALLOWED_TIME_LABEL_BACKGROUND_C,
                                   fg=examination_allowed_time_text)
        self.exam_two_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                   font=("Arial", 13), text="", bg=self.ALLOWED_TIME_LABEL_BACKGROUND_C,
                                   fg=examination_allowed_time_text)
        self.exam_three_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                     font=("Arial", 13), text="", bg=self.ALLOWED_TIME_LABEL_BACKGROUND_C,
                                     fg=examination_allowed_time_text)
        self.exam_four_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                    font=("Arial", 13), text="", bg=self.ALLOWED_TIME_LABEL_BACKGROUND_C,
                                    fg=examination_allowed_time_text)

        # Timers
        self.exam_one_remaining_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                             font=("Arial", 13), text="", bg=self.REMAINING_TIME_LABEL_BACKGROUND_C,
                                             fg=examination_remaining_time_text)
        self.exam_two_remaining_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                             font=("Arial", 13), text="", bg=self.REMAINING_TIME_LABEL_BACKGROUND_C,
                                             fg=examination_remaining_time_text)
        self.exam_three_remaining_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                               font=("Arial", 13), text="", bg=self.REMAINING_TIME_LABEL_BACKGROUND_C,
                                               fg=examination_remaining_time_text)
        self.exam_four_remaining_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                              font=("Arial", 13), text="", bg=self.REMAINING_TIME_LABEL_BACKGROUND_C,
                                              fg=examination_remaining_time_text)

        # Start time
        self.exam_one_start_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                         font=("Arial", 13), text="", bg=self.START_TIME_LABEL_BACKGROUND_C,
                                         fg=examination_start_time_text)
        self.exam_two_start_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                         font=("Arial", 13), text="", bg=self.START_TIME_LABEL_BACKGROUND_C,
                                         fg=examination_start_time_text)
        self.exam_three_start_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                           font=("Arial", 13), text="", bg=self.START_TIME_LABEL_BACKGROUND_C,
                                           fg=examination_start_time_text)
        self.exam_four_start_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                          font=("Arial", 13), text="", bg=self.START_TIME_LABEL_BACKGROUND_C,
                                          fg=examination_start_time_text)

        # Normal Time End Time
        self.exam_one_end_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                       font=("Arial", 13), text="", bg=self.END_TIME_LABEL_BACKGROUND_C,
                                       fg=examination_end_time_text)
        self.exam_two_end_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                       font=("Arial", 13), text="", bg=self.END_TIME_LABEL_BACKGROUND_C,
                                       fg=examination_end_time_text)
        self.exam_three_end_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                         font=("Arial", 13), text="", bg=self.END_TIME_LABEL_BACKGROUND_C,
                                         fg=examination_end_time_text)
        self.exam_four_end_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                        font=("Arial", 13), text="", bg=self.END_TIME_LABEL_BACKGROUND_C,
                                        fg=examination_end_time_text)

        # Extra Time End Time
        self.exam_one_extra_end_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                             font=("Arial", 13), text="", bg=self.EXTRA_END_TIME_LABEL_BACKGROUND_C,
                                             fg=examination_end_plus_extra_time_text)
        self.exam_two_extra_end_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                             font=("Arial", 13), text="", bg=self.EXTRA_END_TIME_LABEL_BACKGROUND_C,
                                             fg=examination_end_plus_extra_time_text)
        self.exam_three_extra_end_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                               font=("Arial", 13), text="", bg=self.EXTRA_END_TIME_LABEL_BACKGROUND_C,
                                               fg=examination_end_plus_extra_time_text)
        self.exam_four_extra_end_time = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                              font=("Arial", 13), text="", bg=self.EXTRA_END_TIME_LABEL_BACKGROUND_C,
                                              fg=examination_end_plus_extra_time_text)

        # Clock Label
        self.clock_label = Label(self.frame, width=self.TIME_LABEL_WIDTH, bd=2, relief=GROOVE,
                                 font=("Arial", 14), text="", bg=digital_background_colour, fg=digital_text_colour)

        # Exit ttk.Button
        self.exit_button = ttk.Button(self.frame, text="Close Program",
                                  command=exit_program)

        # Start All ttk.Button
        self.start_all_button = ttk.Button(self.frame, text="Start All",
                                       command=self.start_all)

        self.restart_button = ttk.Button(self.frame, text="Restart",
                                     command=self.restart)

        # Pause All ttk.Button
        self.pause_all_button = ttk.Button(self.frame, text="Pause All", command=self.pause_all)

        # Individual Start ttk.Buttons
        self.start_button_e1 = ttk.Button(self.frame, width=(self.TIME_LABEL_WIDTH + 3), text="Start",
                                      command=self.start_e1)
        self.start_button_e2 = ttk.Button(self.frame, width=(self.TIME_LABEL_WIDTH + 3), text="Start",
                                      command=self.start_e2)
        self.start_button_e3 = ttk.Button(self.frame, width=(self.TIME_LABEL_WIDTH + 3), text="Start",
                                      command=self.start_e3)
        self.start_button_e4 = ttk.Button(self.frame, width=(self.TIME_LABEL_WIDTH + 3), text="Start",
                                      command=self.start_e4)

        # Adding Widgets to the Screen
        exam_title_label.grid(row=0, column=0, columnspan=2)
        exam_allowed_time_label.grid(row=0, column=2)
        exam_remaining_time_label.grid(row=0, column=3)
        exam_start_time_label.grid(row=0, column=4)
        exam_end_time_label.grid(row=0, column=5)
        exam_end_extra_time_label.grid(row=0, column=6)

        self.clock_label.grid(row=5, column=4, columnspan=2)

        self.CANVAS_WIDTH = 250
        self.CANVAS_HEIGHT = 250

        self.canvas = Canvas(self.frame, background=main_bg,
                             highlightbackground=main_bg,
                             width=self.CANVAS_WIDTH,
                             height=self.CANVAS_HEIGHT)
        self.canvas.grid(row=0, column=7, rowspan=6)

        # Analogue Clock Creation
        # Pre-set a variable with the number of markers on the outside of the clock (in this case for hours)
        n = 12

        # Loop through the process n times
        for marker in range(n):
            # Get the current loop angle
            pointer_angle = marker * (360 / n)

            # Get the coordinates to start drawing the line at
            pointer_min_x_coord = 80*math.cos(math.radians(pointer_angle-90))
            pointer_min_y_coord = 80*math.sin(math.radians(pointer_angle-90))

            # Get the coordinates to finish drawing the line at
            pinter_max_x_coord = 110*math.cos(math.radians(pointer_angle-90))
            pointer_max_y_coord = 110*math.sin(math.radians(pointer_angle-90))

            # Draw the marker to the canvas, with a width of three
            self.canvas.create_line(125+pointer_min_x_coord,
                                    125+pointer_min_y_coord,
                                    125+pinter_max_x_coord,
                                    125+pointer_max_y_coord, width=3, fill=analogue_markers)

        # Do the same, except for hours and minutes
        n = 60

        for marker in range(n):
            pointer_angle = marker * (360 / n)

            # Make the markers smaller than the hour markers
            pointer_min_x_coord = 100*math.cos(math.radians(pointer_angle-90))
            pointer_min_y_coord = 100*math.sin(math.radians(pointer_angle-90))

            pinter_max_x_coord = 110*math.cos(math.radians(pointer_angle-90))
            pointer_max_y_coord = 110*math.sin(math.radians(pointer_angle-90))

            self.canvas.create_line(125+pointer_min_x_coord,
                                    125+pointer_min_y_coord,
                                    125+pinter_max_x_coord,
                                    # Also use a marker line that is less thick
                                    125+pointer_max_y_coord, width=2, fill=analogue_markers)

            # Draw the outer circle (clock boundaries)
            self.canvas.create_oval(10, 10, self.CANVAS_HEIGHT-10, self.CANVAS_WIDTH-10, width=5,
                                    outline=analogue_outer_ring)

        self.second_hand = self.canvas.create_line(125, 125, 125, 225, width=2,
                                                   fill=analogue_second_hand)
        self.minute_hand = self.canvas.create_line(125, 125, 125, 225, width=5,
                                                   fill=analogue_minute_hand)
        self.hour_hand = self.canvas.create_line(125, 125, 125, 200, width=7,
                                                 fill=analogue_hour_hand)

        # Draw the centre circle
        self.canvas.create_oval(118, 118, 132, 132, fill=analogue_center_point)

        # Set Private Pass Variables
        self.one_pass = True
        self.two_pass = True
        self.three_pass = True
        self.four_pass = True

        # Begin the Digital Clock
        self.e1_start_time = 0
        self.e2_start_time = 0
        self.e3_start_time = 0
        self.e4_start_time = 0

    def start(self):
        # String Storage Variables
        e1nc = input_screen.e1n.get()
        e2nc = input_screen.e2n.get()
        e3nc = input_screen.e3n.get()
        e4nc = input_screen.e4n.get()

        e1tc = input_screen.e1t.get()
        e2tc = input_screen.e2t.get()
        e3tc = input_screen.e3t.get()
        e4tc = input_screen.e4t.get()

        # Add widgets to the frame using grid layout if corresponding exam has data
        if one_has_data:
            self.exam_one_name.configure(text=e1nc)
            self.exam_one_name.grid(row=1, column=0, columnspan=2)
            self.exam_one_time.configure(text=e1tc)
            self.exam_one_time.grid(row=1, column=2)
            self.exam_one_remaining_time.grid(row=1, column=3)
            self.exam_one_start_time.grid(row=1, column=4)
            self.exam_one_end_time.grid(row=1, column=5)
            self.start_button_e1.grid(row=1, column=3)
            if one_has_extra_time:
                self.exam_one_extra_end_time.grid(row=1, column=6)
        else:
            self.exam_one_name.grid_remove()
            self.exam_one_time.grid_remove()
            self.exam_one_remaining_time.grid_remove()
            self.exam_one_start_time.grid_remove()
            self.exam_one_end_time.grid_remove()
            self.start_button_e1.grid_remove()
            self.exam_one_extra_end_time.grid_remove()

        if two_has_data:
            self.exam_two_name.configure(text=e2nc)
            self.exam_two_name.grid(row=2, column=0, columnspan=2)
            self.exam_two_time.configure(text=e2tc)
            self.exam_two_time.grid(row=2, column=2)
            self.exam_two_remaining_time.grid(row=2, column=3)
            self.exam_two_start_time.grid(row=2, column=4)
            self.exam_two_end_time.grid(row=2, column=5)
            self.start_button_e2.grid(row=2, column=3)
            if two_has_extra_time:
                self.exam_two_extra_end_time.grid(row=2, column=6)
        else:
            self.exam_two_name.grid_remove()
            self.exam_two_time.grid_remove()
            self.exam_two_remaining_time.grid_remove()
            self.exam_two_start_time.grid_remove()
            self.exam_two_end_time.grid_remove()
            self.start_button_e2.grid_remove()
            self.exam_two_extra_end_time.grid_remove()

        if three_has_data:
            self.exam_three_name.configure(text=e3nc)
            self.exam_three_name.grid(row=3, column=0, columnspan=2)
            self.exam_three_time.configure(text=e3tc)
            self.exam_three_time.grid(row=3, column=2)
            self.exam_three_remaining_time.grid(row=3, column=3)
            self.exam_three_start_time.grid(row=3, column=4)
            self.exam_three_end_time.grid(row=3, column=5)
            self.start_button_e3.grid(row=3, column=3)
            if three_has_extra_time:
                self.exam_three_extra_end_time.grid(row=3, column=6)
        else:
            self.exam_three_name.grid_remove()
            self.exam_three_time.grid_remove()
            self.exam_three_remaining_time.grid_remove()
            self.exam_three_start_time.grid_remove()
            self.exam_three_end_time.grid_remove()
            self.start_button_e3.grid_remove()
            self.exam_three_extra_end_time.grid_remove()

        if four_has_data:
            self.exam_four_name.configure(text=e4nc)
            self.exam_four_name.grid(row=4, column=0, columnspan=2)
            self.exam_four_time.configure(text=e4tc)
            self.exam_four_time.grid(row=4, column=2)
            self.exam_four_remaining_time.grid(row=4, column=3)
            self.exam_four_start_time.grid(row=4, column=4)
            self.exam_four_end_time.grid(row=4, column=5)
            self.start_button_e4.grid(row=4, column=3)
            if four_has_extra_time:
                self.exam_four_extra_end_time.grid(row=4, column=6)
        else:
            self.exam_four_name.grid_remove()
            self.exam_four_time.grid_remove()
            self.exam_four_remaining_time.grid_remove()
            self.exam_four_start_time.grid_remove()
            self.exam_four_end_time.grid_remove()
            self.start_button_e4.grid_remove()
            self.exam_four_extra_end_time.grid_remove()

        if one_has_data and (two_has_data or three_has_data or four_has_data):
            self.start_all_button.grid(row=5, column=2)

        self.pause_all_button.grid(row=5, column=3)

        # Add the frame to the screen
        self.frame.grid(row=0, column=1)
        self.start_updater()

    # Keeps the time of the program
    def main_updater(self):
        # Get time at the start of the cycle
        start_time = self.get_current_time()
        # Create a thread that calls the multi_updater function
        update_thread = threading.Thread(group=None, target=self.multi_updater)
        # Start the thread
        update_thread.start()
        # Clean up variables and memory
        gc.collect()
        # If the program is allowed to update...
        if allow_update:
            # Subtract the start time from the end time to get the time taken to update
            pro_1 = self.get_current_time() - start_time
            # Subtract this from one second and turn into milliseconds
            pro = (1 - pro_1) * 1000
            if __DEBUG__:
                print("Update took %s seconds, started at: %s, and finished at: %s, update timer: %s"
                      % (pro_1, start_time, self.get_current_time(), int(pro)))
            root.after(int(pro), self.main_updater)

    # Calls necessary updates every time the main_updater cycles
    def multi_updater(self):
        global number_of_exams_that_need_five_min_sound, number_of_exams_that_need_end_sound
        global e1_pause_time, e2_pause_time, e3_pause_time, e4_pause_time
        global e1_pause_extra_time, e2_pause_extra_time, e3_pause_extra_time, e4_pause_extra_time
        if allow_check_start_all:
            self.check_start_all()
        if allow_clock:
            self.digital_clock_update()
            self.analogue_clock_update()
        if allow_one or allow_extra_one or continue_count_one:
            self.e1_update()
        elif all_paused and one_has_started:
            e1_pause_time += 1
        elif one_has_extra_time and one_has_started:
            e1_pause_extra_time += 1
        if allow_two or allow_extra_two or continue_count_two:
            self.e2_update()
        elif all_paused and two_has_started:
            e2_pause_time += 1
        elif two_has_extra_time and two_has_started:
            e2_pause_extra_time += 1
        if allow_three or allow_extra_three or continue_count_three:
            self.e3_update()
        elif all_paused and three_has_started:
            e3_pause_time += 1
        elif three_has_extra_time and three_has_started:
            e3_pause_extra_time += 1
        if allow_four or allow_extra_four or continue_count_four:
            self.e4_update()
        elif all_paused and four_has_started:
            e4_pause_time += 1
        elif four_has_extra_time and four_has_started:
            e4_pause_extra_time += 1
        # Check if all exams have finished
        if number_of_completed_exams >= number_of_exams and self.allow_completed_exam_code:
            self.allow_completed_exam_code = False
            self.pause_all_button.grid_remove()
            try:
                self.exit_button.grid(row=5, column=2)
                self.restart_button.grid(row=5, column=3)
            except TclError:
                if __DEBUG__:
                    print("TclError Occurred")
        # Check if any exams require the five minute sound to be played
        if number_of_exams_that_need_five_min_sound > 0:
            # Set number to zero (stop it being played more than once per update)
            number_of_exams_that_need_five_min_sound = 0
            # Create a sound thread (allow the main thread to carry on updating)
            five_minute_sound_thread = threading.Thread(target=Sounds.five_min_sound)
            # Start the thread
            five_minute_sound_thread.start()
        # Check if any exams require the end sound to be played
        if number_of_exams_that_need_end_sound > 0:
            # Set number to zero (stop it being played more than once per update)
            number_of_exams_that_need_end_sound = 0
            # Create a sound thread (allow the main thread to carry on updating)
            end_sound_thread = threading.Thread(target=Sounds.end_sound)
            # Start the thread
            end_sound_thread.start()

    # Function that allows the clock to start updating
    def start_updater(self):
        global allow_clock, allow_update
        # Allows the clock to update
        allow_clock = True

        # Allow and begin the main_updater loop
        allow_update = True
        self.main_updater()

    # Functions that handle the removal of the start buttons, and allow the countdown to start
    # Exam 1
    def start_e1(self):
        # Declare global variables
        global allow_sound_one, number_of_started_exams, allow_one, one_has_started
        # If allowed, play the start sound, stop it being played again
        if allow_sound_one:
            allow_sound_one = False
            # Run as a sound thread
            e1_thread = threading.Thread(target=Sounds.start_sound)
            # Start the thread
            e1_thread.start()
        # Add one to the number of started exams
        number_of_started_exams += 1
        # Declare that one has started (as a boolean variable)
        one_has_started = True
        # Get the time of the examination start
        self.e1_start_time = self.get_current_time()
        # Set the examination one start time label to this time
        self.exam_one_start_time.configure(bg='#00FF00', text=str(self.get_formatted_time(self.e1_start_time)))
        # Get the end time of the examination
        changed_time = self.change_time(e1_allowed_time)
        # Change it from seconds to the digital display time
        formatted_time = self.get_formatted_time(changed_time)
        # Set the label to the formatted end time
        self.exam_one_end_time.configure(text=formatted_time)
        # Do the same for finish time including extra time, if there is extra time
        if one_has_extra_time:
            changed_total_time = self.change_time(e1_total_time)
            formatted_extra_time = self.get_formatted_time(changed_total_time)
            self.exam_one_extra_end_time.configure(text=formatted_extra_time)
        # Allow examination one to update
        allow_one = True
        # Remove the start button from the screen
        self.start_button_e1.grid_remove()

    # Exam 2
    def start_e2(self):
        global allow_sound_two, number_of_started_exams, allow_two, two_has_started
        if allow_sound_two:
            allow_sound_two = False
            e2_thread = threading.Thread(target=Sounds.start_sound)
            e2_thread.start()
        number_of_started_exams += 1
        two_has_started = True
        self.e2_start_time = self.get_current_time()
        self.exam_two_start_time.configure(bg='#00FF00', text=str(self.get_formatted_time(self.e2_start_time)))
        changed_time = self.change_time(e2_allowed_time)
        formatted_time = self.get_formatted_time(changed_time)
        self.exam_two_end_time.configure(text=formatted_time)
        if two_has_extra_time:
            changed_total_time = self.change_time(e2_total_time)
            formatted_extra_time = self.get_formatted_time(changed_total_time)
            self.exam_two_extra_end_time.configure(text=formatted_extra_time)
        allow_two = True
        self.start_button_e2.grid_remove()

    # Exam 3
    def start_e3(self):
        global allow_sound_three, number_of_started_exams, allow_three, three_has_started
        if allow_sound_three:
            allow_sound_three = False
            e3_thread = threading.Thread(target=Sounds.start_sound)
            e3_thread.start()
        number_of_started_exams += 1
        three_has_started = True
        self.e3_start_time = self.get_current_time()
        self.exam_three_start_time.configure(bg='#00FF00', text=str(self.get_formatted_time(self.e3_start_time)))
        changed_time = self.change_time(e3_allowed_time)
        formatted_time = self.get_formatted_time(changed_time)
        self.exam_three_end_time.configure(text=formatted_time)
        if three_has_extra_time:
            changed_total_time = self.change_time(e3_total_time)
            formatted_extra_time = self.get_formatted_time(changed_total_time)
            self.exam_three_extra_end_time.configure(text=formatted_extra_time)
        allow_three = True
        self.start_button_e3.grid_remove()

    # Exam 4
    def start_e4(self):
        global allow_sound_four, number_of_started_exams, allow_four, four_has_started
        if allow_sound_four:
            allow_sound_four = False
            e4_thread = threading.Thread(target=Sounds.start_sound)
            e4_thread.start()
        number_of_started_exams += 1
        four_has_started = True
        self.e4_start_time = self.get_current_time()
        self.exam_four_start_time.configure(bg='#00FF00', text=str(self.get_formatted_time(self.e4_start_time)))
        changed_time = self.change_time(e4_allowed_time)
        formatted_time = self.get_formatted_time(changed_time)
        self.exam_four_end_time.configure(text=formatted_time)
        if four_has_extra_time:
            changed_total_time = self.change_time(e4_total_time)
            formatted_extra_time = self.get_formatted_time(changed_total_time)
            self.exam_four_extra_end_time.configure(text=formatted_extra_time)
        allow_four = True
        self.start_button_e4.grid_remove()

    # Function that starts all of the exams that have not already started
    def start_all(self):
        # Declare global variables that will be used
        global allow_check_start_all, allow_sound_one, allow_sound_two, allow_sound_three, allow_sound_four
        global one_has_data, two_has_data, three_has_data, four_has_data, number_of_exams, number_of_started_exams
        global one_start_all, two_start_all, three_start_all, four_start_all
        global number_of_start_all_exams

        # If the number of started exams is not equal to the total number of exams, play the start sound
        if number_of_started_exams != number_of_exams:
            t1 = threading.Thread(target=Sounds.start_sound)
            t1.start()

        global allow_one
        # If exam one contains data (which it should), run statement code
        if one_has_data and allow_one is False:
            # If the sound is allowed to be run, stop it from being run then call the exam's start method
            # Also add one to the number of exams that have been started using the start_all function
            if allow_sound_one is True:
                number_of_start_all_exams += 1
                allow_sound_one = False
                one_start_all = True
                self.start_e1()
        global allow_two
        if two_has_data and allow_two is False:
            if allow_sound_two is True:
                number_of_start_all_exams += 1
                allow_sound_two = False
                two_start_all = True
                self.start_e2()
        global allow_three
        if three_has_data and allow_three is False:
            if allow_sound_three is True:
                number_of_start_all_exams += 1
                allow_sound_three = False
                three_start_all = True
                self.start_e3()
        global allow_four
        if four_has_data and allow_four is False:
            if allow_sound_four is True:
                number_of_start_all_exams += 1
                allow_sound_four = False
                four_start_all = True
                self.start_e4()

        # Since this should only ever be run once, stop the check_start_all method being run every update cycle
        allow_check_start_all = False
        # Also, remove the start all button
        self.start_all_button.grid_remove()

    # Check if the start_all_button can be removed from screen (if all exams have been started)
    def check_start_all(self):
        # Declare any global variables that will be used or changed
        global allow_check_start_all, number_of_exams, number_of_started_exams
        # If the number of started exams is equal to the total number of exams, remove the start all button
        # Also stop this function being called again on the update cycle
        if number_of_started_exams == number_of_exams:
            self.start_all_button.grid_remove()
            allow_check_start_all = False

    # Digital Clock Update
    def digital_clock_update(self):
        # Get current second
        current_time_s = datetime.now().second
        # Get current minute
        current_time_m = datetime.now().minute
        # Get current hour
        current_time_h = datetime.now().hour

        # Pre-define current_time
        current_time = ''
        # Declare that global variable allow_clock will be used
        global allow_clock
        # If the clock is allowed to update, change the current time to a HH:MM:SS format with the current time
        if allow_clock:
            current_time = str("%.2d:%.2d:%.2d" % (current_time_h, current_time_m, current_time_s))
        # Set the clock label to the current_time variable
        try:
            self.clock_label.configure(text=current_time)
        except TclError:
            if __DEBUG__:
                print("TclError Occurred")

    # Analogue Clock Update
    def analogue_clock_update(self):
        # Get current second
        current_time_s = datetime.now().second
        # Get current minute
        current_time_m = datetime.now().minute
        # Get current hour
        current_time_h = datetime.now().hour

        # Get the corresponding angles for the times
        second_angle = ((current_time_s/60)*360)
        minute_angle = ((current_time_m/60)*360)+((current_time_s/60)*6)
        hour_angle = ((current_time_h/12)*360)+((current_time_m/60)*30)+((current_time_s/60)*0.1)

        # Get the coordinates the clock hands need to be drawn to
        sec_x_coord = 125+(100*math.cos(math.radians(second_angle-90)))
        sec_y_coord = 125+(100*math.sin(math.radians(second_angle-90)))
        minute_x_coord = 125+(100*math.cos(math.radians(minute_angle-90)))
        minute_y_coord = 125+(100*math.sin(math.radians(minute_angle-90)))
        hour_x_coord = 125+(75*math.cos(math.radians(hour_angle-90)))
        hour_y_coord = 125+(75*math.sin(math.radians(hour_angle-90)))

        try:
            # Draw the hours, minutes and seconds hand from the centre of the canvas
            self.canvas.coords(self.second_hand, 125, 125, sec_x_coord, sec_y_coord)
            self.canvas.coords(self.minute_hand, 125, 125, minute_x_coord, minute_y_coord)
            self.canvas.coords(self.hour_hand, 125, 125, hour_x_coord, hour_y_coord)
        except TclError:
            if __DEBUG__:
                print("TclError Occurred")

    # Function that pauses all examinations
    def pause_all(self):
        # Declare any global variables that will be used or changed
        global one_has_started, two_has_started, three_has_started, four_has_started
        global one_has_finished, two_has_finished, three_has_finished, four_has_finished
        global all_paused
        global allow_one, allow_two, allow_three, allow_four
        global allow_extra_one, allow_extra_two, allow_extra_three, allow_extra_four
        global continue_count_one, continue_count_two, continue_count_three, continue_count_four
        self.exit_button.grid_remove()
        self.restart_button.grid_remove()
        # Like the allow_voice_sound button, if all_paused is true, set it to false, remove pause button
        if all_paused:
            if one_has_started and one_has_finished is False:
                changed_time = self.change_time(e1_allowed_time)
                formatted_time = self.get_formatted_time(changed_time)
                self.exam_one_end_time.configure(text=formatted_time)
                if one_has_extra_time:
                    changed_total_time = self.change_time(e1_total_time)
                    formatted_extra_time = self.get_formatted_time(changed_total_time)
                    self.exam_one_extra_end_time.configure(text=formatted_extra_time)
                allow_one = True
            if two_has_started and two_has_finished is False:
                changed_time = self.change_time(e2_allowed_time)
                formatted_time = self.get_formatted_time(changed_time)
                self.exam_two_end_time.configure(text=formatted_time)
                if two_has_extra_time:
                    changed_total_time = self.change_time(e2_total_time)
                    formatted_extra_time = self.get_formatted_time(changed_total_time)
                    self.exam_two_extra_end_time.configure(text=formatted_extra_time)
                allow_two = True
            if three_has_started and three_has_finished is False:
                changed_time = self.change_time(e3_allowed_time)
                formatted_time = self.get_formatted_time(changed_time)
                self.exam_three_end_time.configure(text=formatted_time)
                if three_has_extra_time:
                    changed_total_time = self.change_time(e3_total_time)
                    formatted_extra_time = self.get_formatted_time(changed_total_time)
                    self.exam_three_extra_end_time.configure(text=formatted_extra_time)
                allow_three = True
            if four_has_started and four_has_finished is False:
                changed_time = self.change_time(e4_allowed_time)
                formatted_time = self.get_formatted_time(changed_time)
                self.exam_four_end_time.configure(text=formatted_time)
                if four_has_extra_time:
                    changed_total_time = self.change_time(e4_total_time)
                    formatted_extra_time = self.get_formatted_time(changed_total_time)
                    self.exam_four_extra_end_time.configure(text=formatted_extra_time)
                allow_four = True
            if one_has_finished and continue_count_one is False:
                allow_extra_one = True
            elif one_has_finished and continue_count_one:
                allow_extra_one = True
                continue_count_one = True
            if two_has_finished:
                allow_extra_two = True
            if three_has_finished:
                allow_extra_three = True
            if four_has_finished:
                allow_extra_four = True
            self.exit_button.grid_remove()
            self.restart_button.grid_remove()
            self.pause_all_button.configure(text="Pause All")
            all_paused = False
        # Else if all_paused is false, set it to true, display pause buttons
        else:
            if one_has_started and one_has_finished is False:
                allow_one = False
            if two_has_started and two_has_finished is False:
                allow_two = False
            if three_has_started and three_has_finished is False:
                allow_three = False
            if four_has_started and four_has_finished is False:
                allow_four = False
            if one_has_finished and continue_count_one is False:
                allow_extra_one = False
            elif one_has_finished and continue_count_one:
                allow_extra_one = False
                continue_count_one = False
            if two_has_finished:
                allow_extra_two = False
            if three_has_finished:
                allow_extra_three = False
            if four_has_finished:
                allow_extra_four = False
            self.exit_button.grid(row=5, column=0)
            self.restart_button.grid(row=5, column=1)
            self.pause_all_button.configure(text="Un Pause")
            all_paused = True

    # Handle Updating the Individual Examinations
    # Exam 1
    def e1_update(self):
        # Declare global variables
        global allow_one, allow_extra_one, one_has_finished, e1_pause_time, e1_pause_extra_time
        global red_flash_one, red_flash_one_t, continue_count_one, number_of_completed_exams
        global number_of_exams_that_need_five_min_sound, number_of_exams_that_need_end_sound

        # Set the remaining time to 0 (allow full access to it later)
        e1_remaining_time = 0

        # If one has not finished and it is allowed to update
        if not one_has_finished and allow_one:
            # Get the current remaining time for the examination using the allowed, current and start time
            e1_remaining_time = e1_pause_time + (e1_allowed_time -
                                                 (self.get_current_time() - self.e1_start_time))
        elif not allow_one and allow_extra_one and one_has_finished and one_has_extra_time:
            # Do the same if it is in extra time, using the extra time variables
            e1_remaining_time = e1_pause_extra_time + (e1_allowed_extra_time -
                                                       (self.get_current_time() - self.e1_start_time))

        # Check if there is five minutes remaining
        if int(e1_remaining_time) == 300:
            # Change the font colour of the countdown
            self.exam_one_remaining_time.configure(fg='#FF8C00')
            # Request that the five minute sound be played
            number_of_exams_that_need_five_min_sound += 1

        # If there is no time left
        if int(e1_remaining_time) == 0:
            # If one is allowed to update
            if allow_one:
                # Stop it from being able to update the normal time
                allow_one = False
                # If it has extra time
                if one_has_extra_time:
                    # Change the background and font colour, make sure it shows zero on the display
                    self.exam_one_remaining_time.configure(bg='#0000FF', fg=self.EXTRA_TIME_LABEL_BACKGROUND_C,
                                                           text="00:00:00")
                    # Allow the countdown to update using the extra time
                    allow_extra_one = True
                    # Declare that one has finished
                    one_has_finished = True
                else:
                    # Make sure it shows zero on the display
                    self.exam_one_remaining_time.configure(text="00:00:00")
                    # Allow the exam to continue updating so that it can flash red
                    continue_count_one = True
                    # Declare that one has finished
                    one_has_finished = True
                # Request that the end sound be played
                number_of_exams_that_need_end_sound += 1
            # If the main time is not allowed to update, but the extra time is
            elif allow_extra_one:
                # Make sure it shows zero on the display
                self.exam_one_remaining_time.configure(text="00:00:00")
                # Declare that one has finished
                one_has_finished = True
                # Stop the extra time being updated
                allow_extra_one = False
                # Allow the exam to continue updating so that it can flash red
                continue_count_one = True
                # Request that the end sound be played
                number_of_exams_that_need_end_sound += 1
            # Else it must be that it needs to flash red
            else:
                # Declare that one has finished
                one_has_finished = True
                # If it is able to continue count
                if continue_count_one:
                    # If red_flash_one is true
                    if red_flash_one:
                        # Change the font colour to red, and the background to white
                        self.exam_one_remaining_time.configure(bg='#FFFFFF', fg='#FF0000')
                        # Set red_flash_one to false
                        red_flash_one = False
                        # Add one to the number of times the red flash cycle has occurred
                        red_flash_one_t += 1
                        # If the red flash has been going on for two minutes or more (60 times, once every two updates)
                        if red_flash_one_t >= int(int(flash_red_time)/2):
                            # Show that the exam is completed
                            self.exam_one_remaining_time.configure(text="COMPLETED")
                            # Add one to the number of fully completed exams
                            number_of_completed_exams += 1
                            # Stop the updater from updating exam one
                            continue_count_one = False
                    # Else the display needs to change (flash the other colour)
                    else:
                        # Change the font colour to white, and the background to red
                        self.exam_one_remaining_time.configure(bg='#FF0000', fg='#FFFFFF')
                        # Set red_flash_one to true
                        red_flash_one = True

        # Get the displayable remaining time from the remaining time in seconds
        new_time = self.get_formatted_time(e1_remaining_time)

        # If the time is allowed to update
        if allow_one or allow_extra_one:
            # Change the display to the new, formatted remaining time
            self.exam_one_remaining_time.configure(text=new_time)

    # Exam 2
    def e2_update(self):
        global allow_two, allow_extra_two, two_has_finished
        global red_flash_two, red_flash_two_t, continue_count_two, number_of_completed_exams
        global number_of_exams_that_need_five_min_sound, number_of_exams_that_need_end_sound

        e2_remaining_time = 0

        if not two_has_finished and allow_two:
            e2_remaining_time = e2_allowed_time - (self.get_current_time() - self.e2_start_time)
        elif not allow_two and allow_extra_two and two_has_finished and two_has_extra_time:
            e2_remaining_time = e2_allowed_extra_time - (self.get_current_time() - self.e2_start_time)

        if int(e2_remaining_time) == 300:
            self.exam_two_remaining_time.configure(fg='#FF8C00')
            number_of_exams_that_need_five_min_sound += 1
        if int(e2_remaining_time) == 0:
            if allow_two:
                allow_two = False
                if two_has_extra_time:
                    self.exam_two_remaining_time.configure(bg='#0000FF', fg=self.EXTRA_TIME_LABEL_BACKGROUND_C,
                                                           text="00:00:00")
                    allow_extra_two = True
                    two_has_finished = True
                else:
                    self.exam_two_remaining_time.configure(text="00:00:00")
                    continue_count_two = True
                    two_has_finished = True
                number_of_exams_that_need_end_sound += 1
            elif allow_extra_two:
                self.exam_two_remaining_time.configure(text="00:00:00")
                two_has_finished = True
                allow_extra_two = False
                continue_count_two = True
                number_of_exams_that_need_end_sound += 1
            else:
                two_has_finished = True
                if continue_count_two:
                    if red_flash_two:
                        self.exam_two_remaining_time.configure(bg='#FFFFFF', fg='#FF0000')
                        red_flash_two = False
                        red_flash_two_t += 1
                        if red_flash_two_t >= int(120/2):
                            self.exam_two_remaining_time.configure(text="COMPLETED")
                            number_of_completed_exams += 1
                            continue_count_two = False
                    else:
                        self.exam_two_remaining_time.configure(bg='#FF0000', fg='#FFFFFF')
                        red_flash_two = True

        new_time = self.get_formatted_time(e2_remaining_time)

        if allow_two or allow_extra_two:
            self.exam_two_remaining_time.configure(text=new_time)

    # Exam 3
    def e3_update(self):
        global allow_three, allow_extra_three, three_has_finished
        global red_flash_three, red_flash_three_t, continue_count_three, number_of_completed_exams
        global number_of_exams_that_need_five_min_sound, number_of_exams_that_need_end_sound

        e3_remaining_time = 0

        if not three_has_finished and allow_three:
            e3_remaining_time = e3_allowed_time - (self.get_current_time() - self.e3_start_time)
        elif not allow_three and allow_extra_three and three_has_finished and three_has_extra_time:
            e3_remaining_time = e3_allowed_extra_time - (self.get_current_time() - self.e3_start_time)

        if int(e3_remaining_time) == 300:
            self.exam_three_remaining_time.configure(fg='#FF8C00')
            number_of_exams_that_need_five_min_sound += 1
        if int(e3_remaining_time) == 0:
            if allow_three:
                allow_three = False
                if three_has_extra_time:
                    self.exam_three_remaining_time.configure(bg='#0000FF', fg=self.EXTRA_TIME_LABEL_BACKGROUND_C,
                                                             text="00:00:00")
                    allow_extra_three = True
                    three_has_finished = True
                else:
                    self.exam_three_remaining_time.configure(text="00:00:00")
                    continue_count_three = True
                    three_has_finished = True
                number_of_exams_that_need_end_sound += 1
            elif allow_extra_three:
                self.exam_three_remaining_time.configure(text="00:00:00")
                three_has_finished = True
                allow_extra_three = False
                continue_count_three = True
                number_of_exams_that_need_end_sound += 1
            else:
                three_has_finished = True
                if continue_count_three:
                    if red_flash_three:
                        self.exam_three_remaining_time.configure(bg='#FFFFFF', fg='#FF0000')
                        red_flash_three = False
                        red_flash_three_t += 1
                        if red_flash_three_t >= int(120/2):
                            self.exam_three_remaining_time.configure(text="COMPLETED")
                            number_of_completed_exams += 1
                            continue_count_three = False
                    else:
                        self.exam_three_remaining_time.configure(bg='#FF0000', fg='#FFFFFF')
                        red_flash_three = True

        new_time = self.get_formatted_time(e3_remaining_time)

        if allow_three or allow_extra_three:
            self.exam_three_remaining_time.configure(text=new_time)

    # Exam 4
    def e4_update(self):
        global allow_four, allow_extra_four, four_has_finished
        global red_flash_four, red_flash_four_t, continue_count_four, number_of_completed_exams
        global number_of_exams_that_need_five_min_sound, number_of_exams_that_need_end_sound

        e4_remaining_time = 0

        if not four_has_finished and allow_four:
            e4_remaining_time = e4_allowed_time - (self.get_current_time() - self.e4_start_time)
        elif not allow_four and allow_extra_four and four_has_finished and four_has_extra_time:
            e4_remaining_time = e4_allowed_extra_time - (self.get_current_time() - self.e4_start_time)

        if int(e4_remaining_time) == 300:
            self.exam_four_remaining_time.configure(fg='#FF8C00')
            number_of_exams_that_need_five_min_sound += 1
        if int(e4_remaining_time) == 0:
            if allow_four:
                allow_four = False
                if four_has_extra_time:
                    self.exam_four_remaining_time.configure(bg='#0000FF', fg=self.EXTRA_TIME_LABEL_BACKGROUND_C,
                                                            text="00:00:00")
                    allow_extra_four = True
                    four_has_finished = True
                else:
                    self.exam_four_remaining_time.configure(text="00:00:00")
                    continue_count_four = True
                    four_has_finished = True
                number_of_exams_that_need_end_sound += 1
            elif allow_extra_four:
                self.exam_four_remaining_time.configure(text="00:00:00")
                four_has_finished = True
                allow_extra_four = False
                continue_count_four = True
                number_of_exams_that_need_end_sound += 1
            else:
                four_has_finished = True
                if continue_count_four:
                    if red_flash_four:
                        self.exam_four_remaining_time.configure(bg='#FFFFFF', fg='#FF0000')
                        red_flash_four = False
                        red_flash_four_t += 1
                        if red_flash_four_t >= int(120/2):
                            self.exam_four_remaining_time.configure(text="COMPLETED")
                            number_of_completed_exams += 1
                            continue_count_four = False
                    else:
                        self.exam_four_remaining_time.configure(bg='#FF0000', fg='#FFFFFF')
                        red_flash_four = True

        new_time = self.get_formatted_time(e4_remaining_time)

        if allow_four or allow_extra_four:
            self.exam_four_remaining_time.configure(text=new_time)

    # Return the current time in seconds
    @staticmethod
    def get_current_time():
        return SecondScreen.get_seconds(datetime.now().hour, datetime.now().minute, datetime.now().second)

    @staticmethod
    def get_seconds(h, m, s):
        return (h * (60 ** 2)) + (m * (60 ** 1)) + (s * (60 ** 0))

    # Return a time (seconds) to the current time (seconds)
    @staticmethod
    def change_time(time_in_seconds):
        changed_time_in_seconds = time.time() + time_in_seconds
        return changed_time_in_seconds

    # Return a formatted version of a time (from seconds to HH:MM:SS)
    @staticmethod
    def get_formatted_time(seconds):
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    # Internal function to handle restarting the program
    def restart(self):
        global allow_update, all_paused
        if __DEBUG__:
            print("Restart Called.")
        allow_update = False
        self.exam_one_time.configure(text="")
        self.exam_one_remaining_time.configure(text="")
        self.exam_one_start_time.configure(text="")
        self.exam_one_end_time.configure(text="")
        self.exam_one_extra_end_time.configure(text="")
        self.exam_one_name.configure(text="")
        self.exam_two_time.configure(text="")
        self.exam_two_remaining_time.configure(text="")
        self.exam_two_start_time.configure(text="")
        self.exam_two_end_time.configure(text="")
        self.exam_two_extra_end_time.configure(text="")
        self.exam_two_name.configure(text="")
        self.exam_three_time.configure(text="")
        self.exam_three_remaining_time.configure(text="")
        self.exam_three_start_time.configure(text="")
        self.exam_three_end_time.configure(text="")
        self.exam_three_extra_end_time.configure(text="")
        self.exam_three_name.configure(text="")
        self.exam_four_time.configure(text="")
        self.exam_four_remaining_time.configure(text="")
        self.exam_four_start_time.configure(text="")
        self.exam_four_end_time.configure(text="")
        self.exam_four_extra_end_time.configure(text="")
        self.exam_four_name.configure(text="")
        self.pause_all_button.configure(text="Pause All")
        all_paused = False
        self.exit_button.grid_remove()
        self.restart_button.grid_remove()
        self.frame.grid_remove()
        Restart()


def set_reg_info(text_variable):
        entered_reg_key = text_variable.get()
        response = registry.set_reg_value(registry.HKEY_CURRENT_USER, REG_DIR, "reg_key", entered_reg_key)
        if response:
            messagebox.showinfo("Key Entry Successful",
                                "The key has been successfully entered into registry.\n"
                                "Please re-start the program.")

if __DEBUG__:
    print("Done!")

if __DEBUG__:
    print("Starting Program...")

# Handle the starting of the program: start program if verification is successful, else display error message
if __name__ == '__main__':
    if allow_launch:
        if active_licence_index is not 1:
            update_config()

        # Set the program icon
        root.iconbitmap(bitmap="icon.ico")

        # Make logo frame
        logo_frame = Frame(root, bg=main_bg)
        # Add it do the root window
        logo_frame.grid()

        # Licence holder label
        Label(logo_frame, bg=main_bg, text=str(LICENCE_HOLDER_LONG)).grid(row=0)

        if __DEBUG__:
            print("Trying to Add Logo...")
        try:
            # Try make image file variable
            logo_image = PhotoImage(file=LOGO_FILE_DIRECTORY)

            # Try make image Label
            logo_label = Label(logo_frame, bg=main_bg, image=logo_image)
            logo_label.grid(row=1)
        except TclError:
            if __DEBUG__:
                print("TclError: Logo does not exist or is broken! Trying to use backup logo.")
            try:
                # Try make image file variable
                logo_image = PhotoImage(file='logo_default.png')

                # Try make default image Label
                logo_label = Label(logo_frame, bg=main_bg, image=logo_image)
                logo_label.grid(row=1)
            except TclError:
                if __DEBUG__:
                    print("TclError: Backup Logo does not exist or is broken! Ignoring it.")

        # Author Label
        Label(logo_frame, bg=main_bg, text=format("© %s GCN Software" % __author__)).grid(row=2)

        if __DEBUG__:
            print("Creating and Configuring First and Second Frame...")
        # First Frame Configuration and Creation
        first_frame = Frame(root, background=main_bg)

        for x in range(10):
            Grid.columnconfigure(first_frame, x, weight=1)

        for y in range(5):
            Grid.rowconfigure(first_frame, y, weight=1)

        # Second Screen Frame
        second_frame = Frame(root, background=main_bg)

        for x in range(10):
            Grid.columnconfigure(second_frame, x, weight=1)

        for y in range(5):
            Grid.rowconfigure(second_frame, y, weight=1)

        if __DEBUG__:
            print("Done!")

        # Input Screen Class Initialization
        if __DEBUG__:
            print("Preparation Complete! Starting First Window Creation...")
        input_screen = Input(first_frame)
        input_screen.start()
        # SecondScreen Class Initialization
        main_screen = SecondScreen(second_frame)
    elif not allow_launch:
        import ctypes
        import sys
        message_box = ctypes.windll.user32.MessageBoxW
        auth_error_message = "There is a problem with the authentication code entered in the registry (%s).\n" \
                             "Make sure it is in the format: 'XXXX-XXXX-XXXX' (without quotes)\nCase sensitive." \
                             % current_reg_key
        message_box(None, auth_error_message, "Authentication Error", 0)
        root.title("Enter Serial (Reg) Key")
        entry_key_holder = StringVar()
        Label(root, text="Enter Key Here:").grid()
        Entry(root, textvariable=entry_key_holder).grid()
        ttk.Button(root, text="Submit", command=lambda: sys.exit(set_reg_info(entry_key_holder))).grid()
        if __DEBUG__:
            print("Authentication Error, Exiting.")

# Enter mainloop
if __DEBUG__:
    print("Entering Mainloop...")
mainloop()
if __DEBUG__:
    print("Exited Mainloop, Program Terminating.")
