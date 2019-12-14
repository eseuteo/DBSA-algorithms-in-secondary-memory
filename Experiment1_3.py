import mmap
import os
from time import time
from CombinedReadWrite import read_length_line_write_mmap

# # Main
filePath = "C:/tmp_DSA/test/"
inputFileName = "aka_name.csv"
outputFileName = "mmap_test.csv"

inputFile = filePath + inputFileName
outputFile = filePath + outputFileName
bufferSize = 100
writePosition = 0

read_length_line_write_mmap(inputFile, outputFile, bufferSize, writePosition)