import os
import json
import csv
from pathlib import Path
from time import time
from CombinedReadWrite import rrmerge_Line_Line, read_length_line_write_mmap, rrmerge_line_buffer

with open(str(Path.cwd())+'/Experiment1_3_parameters.json') as parametersFile:
    parameters = json.load(parametersFile)
    csv_folder = parameters['csv_folder']
    output_filename = parameters['output_filename']

filenames = []
for filename in os.listdir(csv_folder):
    filenames.append(csv_folder + '/' + filename)

# #--------------------------------------------------
# # Merge Read_Line with Write_Line
rrmerge_Line_Line(filenames, output_filename)

# #--------------------------------------------------
# # Merge Read_Line with Write_Buffer
# bufferSize = 100
# rrmerge_line_buffer(filenames, outputFilePath, bufferSize)
