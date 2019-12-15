import os
import json
import csv
from pathlib import Path
from time import time
from CombinedReadWrite import rrmerge_Line_Line, rrmerge_Buffer_Char, rrmerge_Buffer_Line

with open(str(Path.cwd())+'/Experiment1_3_parameters.json') as parametersFile:
    parameters = json.load(parametersFile)
    csv_folder = parameters['csv_folder']
    output_filename = parameters['output_filename']

filenames = []
for filename in os.listdir(csv_folder):
    filenames.append(csv_folder + '/' + filename)


# rrmerge_Line_Line(filenames, output_filename)
rrmerge_Buffer_Line(filenames, output_filename, 128)