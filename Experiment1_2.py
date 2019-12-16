import os
import json
import csv
from pathlib import Path
from time import time
from RandomReading import randjump_char, randjump_readln, randjump_buffer, randjump_mmap

with open(str(Path.cwd())+'/input/Experiment1_2_parameters.json') as parametersFile:
    parameters = json.load(parametersFile)
    csv_folder = parameters['csv_folder']
    output_filename = 'output/' + parameters['output_filename']

output_file = open(str(output_filename) + '.csv', 'w', newline='')
field_names = ['implementation', 'file', 'length', 'running_time', 'buffer_size']
writer = csv.DictWriter(output_file, fieldnames=field_names) 
writer.writeheader()

j = 1000000

for filename in os.listdir(csv_folder):
    print("Reading file " + filename + " with readln_char")
    start = time()
    result = randjump_char(csv_folder + '/' + filename, j)
    end = time()
    writer.writerow({'implementation':"Read by char", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'buffer_size':'-'})

for filename in os.listdir(csv_folder):
    print("Reading file " + filename + " with readln_line")
    start = time()
    result = randjump_readln(csv_folder + '/' + filename, j)
    end = time()
    writer.writerow({'implementation':"Read by line", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'buffer_size':'-'})

for filename in os.listdir(csv_folder):
    print("Reading file " + filename + " with readln_buffer")
    for buffer_size in [2 ** x for x in range(16)]:
        print("\tbuffer size " + str(buffer_size))
        start = time()
        result = randjump_buffer(csv_folder + '/' + filename, j, buffer_size)
        end = time()
        writer.writerow({'implementation':"Read by buffer", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'buffer_size': str(buffer_size)})

for filename in os.listdir(csv_folder):
    print("Reading file " + filename + " with readln_mmap")
    for buffer_size in [2 ** x for x in range(16)]:
        print("\tbuffer size " + str(buffer_size))
        start = time()
        result = randjump_mmap(csv_folder + '/' + filename, j, buffer_size)
        end = time()
        writer.writerow({'implementation':"Read by mmap", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'buffer_size': str(buffer_size)})