#!/usr/bin/env python

import re
import string
import sys

def read_input(file):
    temp_cont = []
    # index = -1
    for line in file:
        if not line[0].isdigit():
            continue
        process(line.split('\t'), temp_cont)

def process(data, temp_cont):
    # print(index)
    if len(temp_cont) == 0:
        # print(data)
        # index = data[0]
        temp_cont.append(data)
        return
    if (len(temp_cont) == 1) and (temp_cont[0][0] == data[0]):
        temp1 = temp_cont.pop(0)[1:]
        temp2 = data[1:]
        # print(temp1)

        if (temp1[0] == "incident_start") and (temp2[0] == "incident_end"):
            end_time = temp2[3].strip()
            message = temp1[-1].strip()
            start_time = temp1[3].strip()

            # print(temp1[2])
            # print(temp2[2])

            temp1[2] = temp1[2].split()
            temp2[2] = temp2[2].split()

            station = " ".join([item for item in temp1[2] if item in temp2[2]])
            subject = temp1[1].strip()
            res_list = [end_time, message, start_time, station, subject]
            # print(res_list)
            print("{0}\t{1}\t{2}\t{3}\t{4}".format(end_time, message, start_time, station, subject))


if __name__ == "__main__":
    read_input(sys.stdin)
