import os
import json
import csv
from pathlib import Path
from time import time
from MultiWayMerge import extsort_Line_Mmap

with open(str(Path.cwd()) + '/input/Experiment1_4_parameters.json') as parametersFile:
# with open('C:\\Users\\a0081\\Documents\\BDMA\\ULB\\DB Systems Archutecture INFOH417\\DBSA_all_files\\input\\Experiment1_4_parameters.json') as parametersFile:
    parameters = json.load(parametersFile)
    csv_folder = parameters['csv_folder']
    output_filename = '/output/' + parameters['output_filename']

output_file = open(str(Path.cwd()) + str(output_filename), 'w', newline='')
# output_file = open(str(output_filename) + '.csv', 'w', newline='')
field_names = ['implementation', 'file', 'length', 'running_time', 'Memory_size', 'streams']
writer = csv.DictWriter(output_file, fieldnames=field_names) 
writer.writeheader()

# #--------------------------------------------------
# # Multi-way Merge with Read_Line and Write_Line
# for filename in os.listdir(csv_folder):
#     print("Merge-sort file " + filename + " with readln_line and writeln_line")
#     f = csv_folder + '/' + filename # File to sort
#     k = 2 # Sort on kth column
#     M = 512000 # Number of bytes of available memory
#     d = 5 # Number of streams to merge
#     start = time()
#     result = extsort_Line_Line(f, k, M, d)
#     end = time()
#     writer.writerow({'implementation':"Read_Line_Write_Line", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'buffer_size':'-'})

#--------------------------------------------------
# Multi-way Merge with Read_Line and Write_Mmap
for filename in os.listdir(csv_folder):
    for b in [2 ** x for x in range(4, 16)]:
      for M in [2 ** y for y in range(19, 22)]:
        for d in [x for x in range(5,10)]:
          print("Merge-sort file " + filename + " with readln_line and writeln_mmap with bufferSize " + str(b))
          f = csv_folder + '/' + filename # File to sort
          k = 2 # Sort on kth column
          M = 512000 # Number of bytes of available memory
          d = 5 # Number of streams to merge
          b = 2 ** 16
          start = time()
          result = extsort_Line_Mmap(f, k, M, d, b)
          end = time()
          writer.writerow({'implementation':"Merge_Read_Line_Write_Line", 'file':filename, 'length': str(result), 'running_time': str(end - start), 'Memory_size': M, 'streams': d, 'buffer_size':str(b)})
