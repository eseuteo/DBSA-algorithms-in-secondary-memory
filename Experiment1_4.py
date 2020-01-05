import os
import json
import csv
from pathlib import Path
from time import time
from MultiWayMerge import extsort_Line_Mmap

with open(str(Path.cwd()) + '/input/Experiment1_4_parameters.json') as parametersFile:
    parameters = json.load(parametersFile)
    csv_folder = parameters['csv_folder']
    output_filename = '/output/' + parameters['output_filename']

output_file = open(str(Path.cwd()) + str(output_filename), 'w', newline='')
field_names = ['implementation', 'file', 'length', 'running_time', 'Memory_size', 'streams', 'buffer_size']
writer = csv.DictWriter(output_file, fieldnames=field_names) 
writer.writeheader()

#--------------------------------------------------
# Multi-way Merge with Read_Line and Write_Mmap
for filename in os.listdir(csv_folder):
    for b in [2 ** x for x in range(16, 22, 2)]:
      for M in [2 ** y for y in range(19, 25, 2)]:
        for d in [x for x in range(3,9, 2)]:
          print("Merge-sort file " + filename + " with readln_line and writeln_mmap with bufferSize " + str(b) + " with d = " + str(d) + " with M = " + str(M))
          f = csv_folder + '/' + filename # File to sort
          k = 2 # Sort on kth column
          start = time()
          result = extsort_Line_Mmap(f, k, M, d, b)
          end = time()
          writer.writerow({'implementation':"Merge_Read_Line_Write_Line", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'Memory_size': M, 'streams': d, 'buffer_size':str(b)})