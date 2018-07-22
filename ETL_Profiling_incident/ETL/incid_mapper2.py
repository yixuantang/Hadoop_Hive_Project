#!/usr/bin/env python

import re
import string
import sys
import datetime

def read_input(file):
    for line in file:
        if not line[0].isdigit():
            continue
        process(line.split('\t'))

def process(line):
    data = line
    subject = data[4]
    station = data[3]

    type = get_incident_type(subject)
    station_name = station_reference()
    sta_id = get_station_id(station, station_name)

    dt_format = "%Y-%m-%d %H:%M:%S"
    start_time = datetime.datetime.strptime(data[2], dt_format)
    end_time = datetime.datetime.strptime(data[0], dt_format)
    start_date = start_time.date()
    day_of_week = start_time.weekday()
    start_hour = start_time.hour
    end_hour = end_time.hour

    replace_rule = {0:0, 1:0, 2:0, 3:0, 4:1, 5:1, 6:1,
                         7:1, 8:2, 9:2, 10:2, 11:2, 12:3,
                         13:3, 14:3, 15:3, 16:4, 17:4, 18:4,
                         19:4, 20:5, 21:5, 22:5, 23:5}
    time_of_day_start = replace_rule[start_hour]
    time_of_day_end = replace_rule[end_hour]

    if sta_id == -1:
        return

    if time_of_day_start == time_of_day_end:
        start_date = start_date.strftime("%m%d%Y")
        print("{0}\t{1}\t{2}\t{3}\t{4}".format(sta_id, day_of_week, type, time_of_day_start, start_date))
    if time_of_day_start < time_of_day_end:
        start_date = start_date.strftime("%m%d%Y")
        for i in range(int(time_of_day_end - time_of_day_start) + 1):
            print("{0}\t{1}\t{2}\t{3}\t{4}".format(sta_id, day_of_week, type, time_of_day_start+i, start_date))
    if time_of_day_start > time_of_day_end:
        next_date = start_date + datetime.timedelta(days = 1)
        for i in range(int(time_of_day_start), 6):
            print("{0}\t{1}\t{2}\t{3}\t{4}".format(sta_id, day_of_week, type, i, start_date.strftime("%m%d%Y")))
        for i in range(0, int(time_of_day_end)+1):
            if day_of_week == 6:
                print("{0}\t{1}\t{2}\t{3}\t{4}".format(sta_id, 0, type, i, next_date.strftime("%m%d%Y")))
            else:
                print("{0}\t{1}\t{2}\t{3}\t{4}".format(sta_id, day_of_week+1, type, i, next_date.strftime("%m%d%Y")))


def get_incident_type(subject):

    # passenger
    inci_list_cust = ['customer', 'cusotmer', 'passenger', 'passengers',
                     'person', 'assenger', 'passsenger', 'medical',
                     'medial', 'employee', 'passenger)', 'customeer',
                      'persons', 'animal', 'injury', 'operator',
                      'passneger', 'customer.', 'customers', 'passneger',
                      'passeger', 'passneger', 'passenter', 'pasenger',
                      'passenger.', 'pssenger', 'passener', 'passenger.']
    for i in inci_list_cust:
        if i in subject.split():
            return "passenger"

    # government
    inci_list_gove = ['nypd', 'police', 'fdny', 'nyp', 'tnvestigation'
                     'fd?ny', 'investigation', 'fdnny', 'investigatiion',
                     'investigation.', 'invesitigation', 'tnvestigation',
                      'incident/investigation', 'incident-fdny']
    for i in inci_list_gove:
        if i in subject.split():
            return "government"

    # mechanical
    inci_list_mech = ['mechanical', 'track', 'rail', 'tracks', 'tracks.',
                     'roadbed', 'mechaniccal', 'canopy', 'wires', '(track',
                      'derailment', 'structural', 'structure', 'power', 'debris',
                      'gap', 'tree', 'smoke', 'structual', 'incident-mechanical',
                      'station', 'cables', 'water', 'concrete', 'elevator',
                      'mechaniical', 'obstruction', 'branches', 'mecvhanical'
                      'trrack', 'mechanica', 'incident/mechanical', 'mechancial',
                      'mecvhanical', 'mechaincal', 'mechainical', 'mechanicla',
                      'traick', 'collapse', 'gap-filler', 'mechancal',
                      'mechanicall', 'rails', 'trrack', 'incident/power',
                      'mehanical', 'mechancal']
    for i in inci_list_mech:
        if i in subject.split():
            return "mechanical"

    # operation
    inci_list_oper = ['signal', 'switch', 'swtch', 'swith', 'operation/mechanical',
                      'delays', 'operation', 'planned', 'nyu', 'sgnal', 'swtich',
                      'crowd', 'switch/signal', 'signal/switch', 'safety',
                      'communication', 'signals']
    for i in inci_list_oper:
        if i in subject.split():
            return "operation"

    return "else"

def station_reference():
    namelist = ['59 ST', '5 AV/59 ST', '57 ST-7 AV', '49 ST', 'TIMES SQ-42 ST',
           '34 ST-HERALD SQ', '28 ST', '23 ST', '14 ST-UNION SQ', '8 ST-NYU',
           'PRINCE ST', 'CANAL ST', 'CITY HALL', 'CORTLANDT ST', 'RECTOR ST',
           'WHITEHALL S-FRY', 'DELANCEY/ESSEX', 'BOWERY', 'CHAMBERS ST',
           'FULTON ST', 'BROAD ST', '7 AV', 'PARK PLACE', 'BOTANIC GARDEN',
           'PROSPECT PARK', 'PARKSIDE AV', 'CHURCH AV', 'BEVERLEY ROAD',
           'CORTELYOU RD', 'NEWKIRK PLAZA', 'AVENUE H', 'AVENUE J',
           'AVENUE M', 'KINGS HWY', 'AVENUE U', 'NECK RD', 'SHEEPSHEAD BAY',
           'BRIGHTON BEACH', 'OCEAN PKWY', 'BOROUGH HALL', 'JAY ST-METROTEC',
           'DEKALB AV', 'ATL AV-BARCLAY', 'UNION ST', '4AV-9 ST',
           'PROSPECT AV', '25 ST', '36 ST', '45 ST', '53 ST', 'BAY RIDGE AV',
           '77 ST', '86 ST', 'BAY RIDGE-95 ST', '8 AV', 'FT HAMILTON PKY',
           'NEW UTRECHT AV', '18 AV', '20 AV', 'BAY PKWY', '9 AV', '50 ST',
           '55 ST', '71 ST', '79 ST', '25 AV', 'BAY 50 ST', 'CONEY IS-STILLW',
           'W 8 ST-AQUARIUM', '6 AV', '3 AV', '1 AV', 'BEDFORD AV',
           'LORIMER ST', 'GRAHAM AV', 'GRAND ST', 'MONTROSE AV', 'MORGAN AV',
           'JEFFERSON ST', 'MYRTLE-WYCKOFF', 'HALSEY ST', 'WILSON AV',
           'BUSHWICK AV', 'ATLANTIC AV', 'SUTTER AV', 'LIVONIA AV',
           'NEW LOTS', 'EAST 105 ST', 'CANARSIE-ROCKAW', 'HOWARD BCH JFK',
           'JFK JAMAICA CT1', 'MARCY AV', 'HEWES ST', 'FLUSHING AV',
           'MYRTLE AV', 'KOSCIUSZKO ST', 'GATES AV', 'CHAUNCEY ST',
           'ALABAMA AV', 'VAN SICLEN AV', 'CLEVELAND ST', 'NORWOOD AV',
           'CRESCENT ST', 'CYPRESS HILLS', '75 ST-ELDERTS', '85 ST-FOREST PK',
           'WOODHAVEN BLVD', '104 ST', '111 ST', '121 ST', 'CENTRAL AV',
           'KNICKERBOCKER', 'SENECA AVE', 'FOREST AVE', 'FRESH POND RD',
           'METROPOLITAN AV', 'INWOOD-207 ST', 'DYCKMAN ST', '190 ST',
           '181 ST', '175 ST', '168 ST', '163 ST-AMSTERDM', '155 ST',
           '145 ST', '135 ST', '125 ST', '116 ST', 'CATHEDRAL PKWY', '103 ST',
           '96 ST', '81 ST-MUSEUM', '72 ST', '59 ST COLUMBUS',
           '42 ST-PORT AUTH', '34 ST-PENN STA', '14 ST', 'W 4 ST-WASH SQ',
           'SPRING ST', 'WORLD TRADE CTR', 'HIGH ST', 'HOYT-SCHER',
           'LAFAYETTE AV', 'CLINTON-WASH AV', 'FRANKLIN AV', 'NOSTRAND AV',
           'KINGSTON-THROOP', 'UTICA AV', 'RALPH AV', 'ROCKAWAY AV',
           'BROADWAY JCT', 'LIBERTY AV', 'VAN SICLEN AVE', 'SHEPHERD AV',
           'EUCLID AV', 'GRANT AV', '80 ST', '88 ST', 'ROCKAWAY BLVD',
           'OZONE PK LEFFRT', 'AQUEDUCT N.COND', 'AQUEDUCT RACETR',
           'BROAD CHANNEL', 'BEACH 90 ST', 'BEACH 98 ST', 'BEACH 105 ST',
           'ROCKAWAY PARK B', 'BEACH 67 ST', 'BEACH 60 ST', 'BEACH 44 ST',
           'BEACH 36 ST', 'BEACH 25 ST', 'FAR ROCKAWAY', '161/YANKEE STAD',
           '167 ST', '170 ST', '174-175 STS', 'TREMONT AV', '182-183 STS',
           'FORDHAM RD', 'KINGSBRIDGE RD', 'BEDFORD PK BLVD',
           'NORWOOD 205 ST', '5 AV/53 ST', 'LEXINGTON AV/53',
           'COURT SQ-23 ST', 'QUEENS PLAZA', 'STEINWAY ST', '46 ST',
           'NORTHERN BLVD', '65 ST', 'JKSN HT-ROOSVLT', 'ELMHURST AV',
           'GRAND-NEWTOWN', '63 DR-REGO PARK', '67 AV', 'FOREST HILLS 71',
           '75 AV', 'KEW GARDENS', 'BRIARWOOD', 'SUTPHIN BLVD',
           'PARSONS BLVD', '169 ST', 'JAMAICA 179 ST', 'COURT SQ', '21 ST',
           'GREENPOINT AV', 'NASSAU ST', 'BROADWAY', 'MYRTLE-WILLOUGH',
           'BEDFORD-NOSTRAN', 'CLASSON AV', '47-50 STS ROCK',
           '42 ST-BRYANT PK', "B'WAY-LAFAYETTE", '2 AV', 'EAST BROADWAY',
           'YORK ST', 'BERGEN ST', 'CARROLL ST', 'SMITH-9 ST', '4 AV-9 ST',
           '15 ST-PROSPECT', 'DITMAS AV', 'AVENUE I', 'AVENUE N', 'AVENUE P',
           'AVENUE X', 'NEPTUNE AV', '57 ST', 'LEXINGTON AV/63',
           'ROOSEVELT ISLND', '21 ST-QNSBRIDGE', 'JAMAICA VAN WK',
           'SUTPHIN-ARCHER', 'JAMAICA CENTER', 'NEWARK HW BMEBE', 'HARRISON',
           'JOURNAL SQUARE', 'GROVE STREET', 'EXCHANGE PLACE',
           'PAVONIA/NEWPORT', 'CITY / BUS', 'CHRISTOPHER ST', '9TH STREET',
           '14TH STREET', 'TWENTY THIRD ST', 'THIRTY ST', 'LACKAWANNA',
           'THIRTY THIRD ST', 'NEWARK BM BW', 'NEWARK C', 'NEWARK HM HE',
           'SOUTH FERRY', 'WALL ST', 'FRANKLIN ST', 'HOUSTON ST', '18 ST',
           '66 ST-LINCOLN', '116 ST-COLUMBIA', '137 ST CITY COL', '157 ST',
           '191 ST', '207 ST', '215 ST', 'MARBLE HILL-225', '231 ST',
           '238 ST', 'V.CORTLANDT PK', 'BOWLING GREEN', 'BROOKLYN BRIDGE',
           'BLEECKER ST', 'ASTOR PL', '33 ST', 'GRD CNTRL-42 ST', '51 ST',
           '68ST-HUNTER CO', '110 ST', '138/GRAND CONC', '149/GRAND CONC',
           'MT EDEN AV', '176 ST', 'BURNSIDE AV', '183 ST', 'MOSHOLU PKWY',
           'WOODLAWN', 'CENTRAL PK N110', 'HARLEM 148 ST', '3 AV-149 ST',
           'JACKSON AV', 'INTERVALE AV', 'SIMPSON ST', 'FREEMAN ST', '174 ST',
           'WEST FARMS SQ', 'E 180 ST', 'BRONX PARK EAST', 'PELHAM PKWY',
           'ALLERTON AV', 'BURKE AV', 'GUN HILL RD', '219 ST', '225 ST',
           '233 ST', 'NEREID AV', 'WAKEFIELD/241', '3 AV 138 ST', 'BROOK AV',
           'CYPRESS AV', "E 143/ST MARY'S", 'E 149 ST', 'LONGWOOD AV',
           'HUNTS POINT AV', 'WHITLOCK AV', 'ELDER AV', 'MORISN AV/SNDVW',
           'ST LAWRENCE AV', 'PARKCHESTER', 'CASTLE HILL AV', 'ZEREGA AV',
           'WESTCHESTER SQ', 'MIDDLETOWN RD', 'BUHRE AV', 'PELHAM BAY PARK',
           '5 AVE', 'VERNON-JACKSON', 'HUNTERS PT AV', 'QUEENSBORO PLZ',
           '39 AV', '36 AV', '30 AV', 'ASTORIA BLVD', 'ASTORIA DITMARS',
           '33 ST-RAWSON ST', '40 ST LOWERY ST', '46 ST BLISS ST', '52 ST',
           '61 ST WOODSIDE', '69 ST', '74 ST-BROADWAY', '82 ST-JACKSON H',
           '90 ST-ELMHURST', 'JUNCTION BLVD', '103 ST-CORONA',
           'METS-WILLETS PT', 'FLUSHING-MAIN', '34 ST-HUDSON YD', 'CLARK ST',
           'HOYT ST', 'NEVINS ST', 'GRAND ARMY PLAZ', 'EASTN PKWY-MUSM',
           'KINGSTON AV', 'CROWN HTS-UTICA', 'SARATOGA AV', 'NEW LOTS AV',
           'PRESIDENT ST', 'STERLING ST', 'WINTHROP ST', 'BEVERLY RD',
           'NEWKIRK AV', 'FLATBUSH AV-B.C', 'MORRIS PARK', 'BAYCHESTER AV',
           'EASTCHSTER/DYRE', 'ST. GEORGE', 'TOMPKINSVILLE', 'RIT-MANHATTAN',
           'RIT-ROOSEVELT', 'PATH NEW WTC', 'PENNSYLVANIA AV',
           'SUTTER AV-RUTLD', 'JUNIUS ST', 'ORCHARD BEACH', 'PATH WTC',
           'PATH WTC 2']

    namelist = [re.sub('['+string.punctuation+']', ' ', name).lower().split() for name in namelist]
    return namelist

def get_station_id(query_input, station_name):
    query_list = query_input.split()
    ref_list = station_name

    largest = 0
    match_id = -1

    for j,namej in enumerate(ref_list):
        curr = query_list
        ref_name = namej

        special = {'essex':16, '68':276, 'dyre':364, 'eastern':351,
                   'ditmars':332, 'eastchester':364, 'fort':55,
                   'w4': 137, 'lex': 184, 'time': 4, 'eastcher': 364,
                   'koscuiszko': 95, 'kosciusko':95, 'morrison': 362}

        if curr[0] in special.keys():
            match_id = special[curr[0]]
            break

        length = 0
        for k in range(min(len(curr), len(ref_name))):
            if curr[k] != ref_name[k]:
                break
            if curr[k] == ref_name[k]:
                length += 1

        if length > largest:
            largest = length
            match_id = j
    return match_id

if __name__ == "__main__":
    read_input(sys.stdin)
