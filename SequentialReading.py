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

    while True:
        line, current_position = readln_mmap(file, current_position, bufferSize)
        if not line or line == "b''":
            break
        sum += len(line)

    file.close()
    return sum
