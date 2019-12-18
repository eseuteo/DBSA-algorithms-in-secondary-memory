import os
import json
import csv
from pathlib import Path
from time import time
from CombinedReadWrite import rrmerge_Line_Line, rrmerge_line_mmap, rrmerge_line_buffer, rrmerge_Buffer_Char, rrmerge_Buffer_Line, rrmerge_buffer_buffer, rrmerge_buffer_mmap


with open(str(Path.cwd())+'/input/Experiment1_3_parameters.json') as parametersFile:
    parameters = json.load(parametersFile)
    csv_folder = parameters['csv_folder']
    output_filename = 'output/' + parameters['output_filename']

filenames = []
for filename in os.listdir(csv_folder):
    filenames.append(csv_folder + '/' + filename)

# #--------------------------------------------------
# # Merge Read_Line with Write_Char
# rrmerge_Line_Char(filenames, output_filename)

# #--------------------------------------------------
# # Merge Read_Line with Write_Line
# rrmerge_Line_Line(filenames, output_filename)

# #--------------------------------------------------
# # Merge Read_Line with Write_Buffer
# bufferSize = 100
# rrmerge_line_buffer(filenames, output_filename, bufferSize)

# #--------------------------------------------------
# # Merge Read_Line with Write_Map
# bufferSize = 100
# writePosition = 0
# rrmerge_line_mmap(filenames, output_filename, bufferSize, writePosition)

# #--------------------------------------------------
# # Merge Read_Buffer with Write_Char
# bufferSize = 100
# rrmerge_Buffer_Char(filenames, output_filename, bufferSize)

# #--------------------------------------------------
# # Merge Read_Buffer with Write_Line
# rrmerge_Buffer_Line(filenames, output_filename, 128)

# #--------------------------------------------------
# # Merge Read_Buffer with Write_Buffer
# bufferSize = 100
# rrmerge_buffer_buffer(filenames, output_filename, bufferSize)

# #--------------------------------------------------
# # Merge Read_Buffer with Write_Map
bufferSize = 100
writePosition = 0
output_filename = "C:/tmp_DSA/" + output_filename
rrmerge_buffer_mmap(filenames, output_filename, bufferSize, writePosition)