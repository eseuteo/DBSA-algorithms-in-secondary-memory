import os
import json
import csv
from pathlib import Path
from time import time
from SequentialReading import length_char, length_line, length_buffer, length_mmap

with open(str(Path.cwd())+'/Experiment1_1_parameters.json') as parametersFile:
    parameters = json.load(parametersFile)
    csv_folder = parameters['csv_folder']
    output_filename = parameters['output_filename']

output_file = open(str(output_filename) + '.csv', 'w', newline='')
field_names = ['implementation', 'file', 'length', 'running_time', 'buffer_size']
writer = csv.DictWriter(output_file, fieldnames=field_names) 
writer.writeheader()

# for filename in os.listdir(csv_folder):
#     print("Reading file " + filename + " with readln_char")
#     start = time()
#     result = length_char(csv_folder + '/' + filename)
#     end = time()
#     writer.writerow({'implementation':"Read by char", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'buffer_size':'-'})

# for filename in os.listdir(csv_folder):
#     print("Reading file " + filename + " with readln_line")
#     start = time()
#     result = length_line(csv_folder + '/' + filename)
#     end = time()
#     writer.writerow({'implementation':"Read by line", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'buffer_size':'-'})

# for filename in os.listdir(csv_folder):
#     print("Reading file " + filename + " with readln_buffer")
#     for buffer_size in [2 ** x for x in range(12)]:
#         print("\tbuffer size " + str(buffer_size))
#         start = time()
#         result = length_buffer(csv_folder + '/' + filename, buffer_size)
#         end = time()
#         writer.writerow({'implementation':"Read by buffer", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'buffer_size': str(buffer_size)})

for filename in os.listdir(csv_folder):
    print("Reading file " + filename + " with readln_mmap")
    for buffer_size in [2 ** x for x in range(0, 15)]:
        print("\tbuffer size " + str(buffer_size))
        start = time()
        result = length_mmap(csv_folder + '/' + filename, buffer_size)
        end = time()
        writer.writerow({'implementation':"Read by buffer", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'buffer_size': str(buffer_size)})