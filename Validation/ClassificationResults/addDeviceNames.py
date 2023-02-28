from numpy.lib.function_base import diff
from datetime import datetime
import csv
import pandas as pd
import numpy as np
from itertools import tee
from statistics import mean
import pprint

# Replace to the right filenames
list_devices_filename = "csv/list_devices.csv"
trace_filename = "csv/16-09-23.csv"

# list storing device name and corresponding mac address
list_devices = []

# temporary new list containing previous trace file with device name appended
temp_trace_list = []


# file containing device name and mac address. Putting them into a list
with open(list_devices_filename) as device_list_csv:
    csv_reader = csv.reader(device_list_csv, delimiter=',')

    for row in csv_reader:
        entry = {row[1]:row[0]}
        list_devices.append(entry)

# file containing the trace, joining it with device name
with open(trace_filename) as trace_list_csv:
    csv_reader = csv.reader(trace_list_csv, delimiter=',')

    # add the string "device name" to first row
    row1 = next(csv_reader)
    row1.append("device_name")

    for row in csv_reader:
        device_name = ""

        # if source mac address corresponds to device name, append it to row
        for device in list_devices:
            if row[3] in device:
                device_name = device[row[3]]
        row.append(device_name)

        # store it into the temp_trace_list
        temp_trace_list.append(row)

# transforming the temp trace list into a pandas dataframe
df = pd.DataFrame(temp_trace_list, columns = ['Packet ID','TIME','Size','eth.src','eth.dst','IP.src','IP.dst','IP.proto','port.src','port.dst', 'device name'])

df.to_csv('csv/labeledDataset.csv')
df.head()
