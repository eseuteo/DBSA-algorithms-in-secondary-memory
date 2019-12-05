import mmap
import os
from time import time
from ReadWriteByChar import readln_char
from ReadWriteByLine import readln_line
from ReadWriteByBuffer import readln_buffer
from ReadWriteByMmap import readln_mmap

#------------------------------------
# Sequential Reading function - Character
def length_char(f):
  sum = 0
  seekPos = 0

  # Open file for reading in binary mode switching buffering off
  file = open(f, "r+b", 0)

  # Read all lines in a file. readln_char returns the line that was read and the position of the next line to be read
  # When the end of the file is reached, seekPos will be -1, ending the loop
  while seekPos != -1:
    line, seekPos = readln_char(file,seekPos)
    sum += len(line)

  file.close()

  return sum
#------------------------------------

def length_line(fileName):
    file = open(fileName, 'r+b')
    sum = 0
    current_position = 0

    while True:
        line, current_position = readln_line(file, current_position)
        if not line:
            break
        sum += len(line)

    file.close()
    return sum

def length_buffer(fileName, bufferSize):
    file = open(fileName, 'r+b', bufferSize)
    sum = 0
    current_position = 0
    while True:
        line, current_position = readln_buffer(file, current_position, bufferSize)
        if not line or line == "b''":
            break
        sum += len(line)
    file.close()
    return sum

def length_mmap(fileName, bufferSize):
    file = open(fileName, 'r+b', bufferSize)
    sum = 0
    current_position = 0

    # Obtaining values to be used in mapping, based on the input parameters
    actualFilePosition = current_position // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY
    actualBufferSize = (bufferSize // mmap.ALLOCATIONGRANULARITY + 1) * mmap.ALLOCATIONGRANULARITY
    fileSize = os.fstat(file.fileno()).st_size

    # Ensure legal mapping (not larger than the file)
    if fileSize < actualFilePosition + actualBufferSize:
        actualBufferSize = fileSize - actualFilePosition

    mapping = mmap.mmap(file.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)

    incompleteLine = False

    while sum < fileSize:
        line, current_position = readln_mmap(mapping, current_position, actualFilePosition, bufferSize, actualBufferSize)
        if not line or line == "b''":
            break
        if '\n' not in line:
            incompleteLine = True
        # Check if outside mapped portion
        if current_position >= actualFilePosition + actualBufferSize:
            # print("remapping")
            actualFilePosition = current_position // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY
            # Ensure legal portion is mapped (not too big)
            if fileSize < actualFilePosition + actualBufferSize:
                actualBufferSize = fileSize - actualFilePosition
            mapping = mmap.mmap(file.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)
            if incompleteLine:
                line_part, current_position = readln_mmap(mapping, current_position, actualFilePosition, bufferSize, actualBufferSize)
                line += line_part
                incompleteLine = False
        sum += len(line)
        actualFilePosition = current_position // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY
        actualBufferSize = (bufferSize // mmap.ALLOCATIONGRANULARITY + 1) * mmap.ALLOCATIONGRANULARITY

    file.close()
    return sum
