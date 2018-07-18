#!/usr/bin/env python

import re
import string
import sys

def read_input(file):
    start_room = []
    for line in file:
        if not line[0].isdigit():
            continue
        process(line.split('\t'), start_room)

def process(data, start_room):
    time = data[3][:19]
    subject = data[5].lower().strip()
    message = data[6].lower().strip()

    is_start = (subject[:7] != "updated")
    is_end = ((subject[:7] == "updated") and ("resumed" in message))

    if (not is_start) and (not is_end):
        return

    station = extract_station_elements(message)


    if is_start:
        start_room.append((subject, station, time, message))
        # print(len(start_room))
    if is_end:
        temp = (subject, station, time, message)
        for i, record in enumerate(start_room):
            if same_incident(record, temp):
                new_index = index_counter()

                sta_start = " ".join(record[1])
                sta_end = " ".join(temp[1])

                print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(new_index, "incident_start", record[0].strip(), sta_start.strip(), record[2].strip(), record[3].strip()))
                print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(new_index, "incident_end", temp[0].strip(), sta_end.strip(), temp[2].strip(), temp[3].strip()))
                # print("{0}\t{1}".format(new_index, ("incident_start", ) + record))
                # print("{0}\t{1}".format(new_index, ("incident_end", ) + temp))
                start_room.pop(i)
            else:
                continue



def same_incident(start_rec, end_rec):
    try:
        a = start_rec[1][0]
        b = end_rec[1][0]
        return (a == b) & ('updated: ' + start_rec[0] == end_rec[0])
    except IndexError:
        return False

def index_counter(i=[0]):
    i[0] += 1
    return i[0]

def extract_station_elements(message):
    keyword = "at"
    line = re.sub('['+string.punctuation+']', ' ', message)
    words = line.lower().split()
    if keyword in words:
        res = words[words.index(keyword)+1:words.index(keyword)+5]
    else:
        res = []
    return res





if __name__ == "__main__":
    read_input(sys.stdin)
