#!/usr/bin/env python
import sys
import re
import string

for line in sys.stdin:
    data = line.split('\t')
    # station_id = data[0]
    # day_of_week = data[1]
    # type = data[2]
    time_of_day = data[3].strip()

    print("{0}\t{1}".format(time_of_day, 1))
