import mmap
import os
from time import time
from ReadWriteByChar import readln_char
from ReadWriteByLine import readln_line
from ReadWriteByBuffer import readln_buffer
from ReadWriteByMmap import read_bline_mmap

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
    inputFile = open(fileName, 'r+b', bufferSize)
    sumChunk = 0
    sum = 0
    filePosition = 0
    isLineComplete = 1
    bufferPosition = 0
    bLineTemp = b""
    end = 0

    fileSize = os.fstat(inputFile.fileno()).st_size
    if fileSize < filePosition + bufferSize:
        bufferSize = fileSize - filePosition

    inputFile.seek(filePosition)
    chunk = inputFile.read(bufferSize)
    
    while True:
        while sumChunk < bufferSize:
            bline, bufferPosition = readln_buffer(chunk, bufferPosition)

            # Line (or part of a line) has already been read, so values are updated
            lineLength = len(bline)
            sum += lineLength
            sumChunk += lineLength

            if bline.find(b"\n") == -1: # End of line was not found in latest line read
                isLineComplete = 0
                bLineTemp += bline # Since line is incomplete, the part of the line already read is stored in a temporary variable
            elif isLineComplete == 0: # Char '\n' is found but there is an incomplete line pending
                bline = bLineTemp + bline
                isLineComplete = 1

            if isLineComplete == 1:
                # print(bline.decode("utf-8")) # This is where something can be done with lines read
                bLineTemp = b""
            
            if sum >= fileSize: # When the number of bytes read matches the size of the file, the loop should break
                # if bline.find(b"\n") == -1: # If the last line in the file does not end in '\n', it can be retrieved from here
                #     print(bline.decode("utf-8"))
                end = 1
                break
        
        if end == 1:
            break
        
        # If the code reaches this part, it means that the buffer was read entirely but the file still has more data
        filePosition += bufferPosition
        inputFile.seek(filePosition)
        chunk = inputFile.read(bufferSize)
        sumChunk = 0
        bufferPosition = 0
    
    inputFile.close()
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
    prev_current_position = 0

    while True:
        prev_current_position = current_position
        line, current_position = read_bline_mmap(mapping, current_position, actualFilePosition, bufferSize, actualBufferSize)
        if not line:
            break
        # If line exceedes mapping
        if b'\n' not in line:
            incompleteLine = True
        # If remapping needed
        if current_position >= actualFilePosition + actualBufferSize and current_position < fileSize:
            actualFilePosition = current_position // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY

            if fileSize < actualFilePosition + actualBufferSize:
                actualBufferSize = fileSize - actualFilePosition

            mapping = mmap.mmap(file.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)

            if incompleteLine:
                line_part, current_position = read_bline_mmap(mapping, current_position, actualFilePosition, bufferSize, actualBufferSize)
                line += line_part
                incompleteLine = False
        sum += current_position - prev_current_position

    file.close()
    return sum
