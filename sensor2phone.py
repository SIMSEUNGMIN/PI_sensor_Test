# pexpect API
from pexpect import *

# Standard API
import os, threading
import datetime
import time, sys

# Save Advertise Data
# Global Variable
# global ad_data
# number, hour, minute, second, millisecond
ad_data = ""


# Reset hci0
def reset_hci():
    os.system("sudo hciconfig hci0 down")
    os.system("sudo hciconfig hci0 up")


# Set Interval
def set_advertise_interval():
    # interval = input("Advertise Interval(sec) is ") 1 Sec
    # HCI_LE_Set_Advertising_Parameters
    run("sudo hcitool -i hci0 cmd 0x08 0x0006 40 06 40 06 03 00 00 00 00 00 00 00 00 07 00")


def make_data(count):
    time_milli = current_milli_time()

    list_time_milli = list(str(time_milli))

    # get all length
    all_length = 3 + len(list_time_milli)

    str_list = ""

    for i in range(len(list_time_milli)):
        if i != len(list_time_milli) - 1:
            str_list += hex(int(list_time_milli[i])) + " "
        else:
            str_list += hex(int(list_time_milli[i]))

    data = hex(all_length) + " " + hex((all_length - 1)) + " FF " + hex(count) + " " \
           + str_list

    print(data)

    return data


# get millisecond
def current_milli_time():
    return int(round(time.time() * 1000))


# Init Advertise Data
def init_advertise_data():
    # Global Variable
    global ad_data

    ad_data = make_data(0)

    # HCI_LE_Set_Advertising_Data
    run("sudo hcitool -i hci0 cmd 0x08 0x0008 " + ad_data)

    time.sleep(1)


# Set Advertise Data
def set_advertise_data():
    # https://stackoverflow.com/questions/44404093/timeout-for-10-seconds-while-loop-in-python
    # start time
    count = 1
    while count < 100:  # 1sec
        # Global Variable
        global ad_data

        ad_data = make_data(count)

        # HCI_LE_Set_Advertising_Data
        run("sudo hcitool -i hci0 cmd 0x08 0x0008 " + ad_data)

        count += 1

        time.sleep(1)


# Enable Advertise Mode
def advertise_enable():
    # HCI_LE_Set_Advertise_Enable
    run("sudo hcitool -i hci0 cmd 0x08 0x000A 01")


def Advertising():
    print("Advertise")
    reset_hci()
    set_advertise_interval()
    init_advertise_data()
    advertise_enable()
    set_advertise_data()
    os.system("sudo hciconfig hci0 down")


def Main():
    Advertising()


Main()