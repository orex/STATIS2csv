#!/usr/bin/env python
import re
import csv
import argparse

# columns > 27 are unknown when only considering the STATIS file
csv_header = ('md step','simulation time [ps]','total energy','system temperature','configurational energy','VdW energy','coulombic energy','bond energy','angle energy','dihedral energy','tethering energy','enthalpy','rotational temperature','total virial','VdW virial','coulombic virial','bond virial','angle virial','constraint virial','tethering virial','volume','core-shell temperature','core-shell potential energy','core-shell virial','cell angle alpha','cell angle beta','cell angle gamma','PMF constraint virial','pressure')

def read_STATIS(STATIS):
    # first two lines with configuration name
    cfgname = STATIS.readline()
    # and the energy unit are not used ATM
    energy_unit = STATIS.readline()

    # list to store record data
    records = []
    row = -1
    while True:
        # read information about current step
        step_info = STATIS.readline().split()
        # exit loop if line contains no values
        if len(step_info) == 0:
            break

        # start a new row
        row += 1
        records.append([])
        
        # append information about current timestep to records
        nstep = int(step_info[0])
        records[row].append(nstep)
        time = float(step_info[1])
        records[row].append(time)
        nument = int(step_info[2])
        nlines = nument / 5
        if nument % 5 > 0:
            nlines += 1

        # read next nlines and append them to records
        for line in xrange(nlines):
            records_in_line = STATIS.readline().split()
            for record in records_in_line:
                records[row].append(float(record))

    # return values
    return records

# initialize parser
parser = argparse.ArgumentParser(description='Converts a DL_POLY 4 STATIS file to CSV format.')
parser.add_argument('STATIS', nargs='?', type=str, help='STATIS file', default='STATIS')
parser.add_argument('CSV', nargs='?', type=str, help='CSV file', default='STATIS.csv')

# parse arguments
args = parser.parse_args()
 
# read records from STATIS file
with open(args.STATIS, 'r') as STATIS:
    records = read_STATIS(STATIS)

# write records to CSV file
with open(args.CSV, 'w') as CSV:
    writer = csv.writer(CSV)
    writer.writerow(csv_header)
    writer.writerows(records)
