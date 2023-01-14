import csv
import time


with open("sequences.csv", 'r' ) as file:
    csvreader = csv.reader(file)
    next(csvreader)

    for row in csvreader:
        print(row[:,2:3])
        time.sleep(2.4)
