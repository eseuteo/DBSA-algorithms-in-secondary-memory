import os
import json
import csv
from pathlib import Path
from time import time
from CombinedReadWrite import rrmerge_Line_Char, rrmerge_Line_Line, rrmerge_line_mmap, rrmerge_line_buffer, rrmerge_Buffer_Char, rrmerge_Buffer_Line, rrmerge_buffer_buffer, rrmerge_buffer_mmap


with open(str(Path.cwd())+'/input/Experiment1_3_parameters.json') as parametersFile:
    parameters = json.load(parametersFile)
    csv_folder = parameters['csv_folder']
    output_filename = 'output/' + parameters['output_filename']

output_file_times = open(str('output/Experiment1_3_times') + '.csv', 'w', newline='')
field_names = ['implementation', 'running_time', 'buffer_size']
writer = csv.DictWriter(output_file_times, fieldnames=field_names) 
writer.writeheader()

filenames = []
for filename in os.listdir(csv_folder):
    filenames.append(csv_folder + '/' + filename)

bufferSize = 100
writePosition = 0

#--------------------------------------------------
# Merge Read_Line with Write_Char
start = time()
rrmerge_Line_Char(filenames, output_filename)
end = time()
writer.writerow({'implementation':"Read by Line, Write by Char", 'running_time': str(end - start), 'buffer_size':'-'})

#--------------------------------------------------
# Merge Read_Line with Write_Line
start = time()
rrmerge_Line_Line(filenames, output_filename)
end = time()
writer.writerow({'implementation':"Read by Line, Write by Line", 'running_time': str(end - start), 'buffer_size':'-'})

#--------------------------------------------------
# Merge Read_Line with Write_Buffer
start = time()
rrmerge_line_buffer(filenames, output_filename, bufferSize)
end = time()
writer.writerow({'implementation':"Read by Line, Write by Buffer", 'running_time': str(end - start), 'buffer_size':'-'})

#--------------------------------------------------
# Merge Read_Line with Write_Map
start = time()
rrmerge_line_mmap(filenames, output_filename, bufferSize, writePosition)
end = time()
writer.writerow({'implementation':"Read by Line, Write by Map", 'running_time': str(end - start), 'buffer_size':'-'})

#--------------------------------------------------
# Merge Read_Buffer with Write_Char
start = time()
rrmerge_Buffer_Char(filenames, output_filename, bufferSize)
end = time()
writer.writerow({'implementation':"Read by Buffer, Write by Char", 'running_time': str(end - start), 'buffer_size':'-'})

#--------------------------------------------------
# Merge Read_Buffer with Write_Line
start = time()
rrmerge_Buffer_Line(filenames, output_filename, bufferSize)
end = time()
writer.writerow({'implementation':"Read by Buffer, Write by Line", 'running_time': str(end - start), 'buffer_size':'-'})

#--------------------------------------------------
# Merge Read_Buffer with Write_Buffer
start = time()
rrmerge_buffer_buffer(filenames, output_filename, bufferSize)
end = time()
writer.writerow({'implementation':"Read by Buffer, Write by Buffer", 'running_time': str(end - start), 'buffer_size':'-'})

#--------------------------------------------------
# Merge Read_Buffer with Write_Map
start = time()
rrmerge_buffer_mmap(filenames, output_filename, bufferSize, writePosition)
end = time()
writer.writerow({'implementation':"Read by Buffer, Write by Map", 'running_time': str(end - start), 'buffer_size':'-'})
