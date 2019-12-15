import datetime
from random import randint
import os

def readln_char(inputFile, filePosition):
  """
  This function assumes that the inputFile parameter is an already opened file.
  To open file for reading in binary mode switching buffering off:
  file = open(outputFile, "r+b", 0)
  """
  bline = b""

  inputFile.seek(filePosition)
  currPosition = filePosition

  while True:
    char = inputFile.read(1)
    if not char:
      # End of file
      currPosition = -1
      break
    # If it is not the end of file,
    # add the character to the current line being read
    bline += char
    if char == b"\n":
      # End of line
      currPosition = inputFile.tell() # Identifying current position
      break
  
  return bline, currPosition

def writeln_char(outputFile, line):
  """
  This function assumes that the outputFile parameter is an already opened file.
  To open file for writing (appending) in binary mode switching buffering off:
  file = open(outputFile, "a+b", 0)
  """
  lineLength = len(line)
  c = b''
  
  for n in range(0, lineLength):
    c = line[n]
    outputFile.write(chr(c).encode("utf-8"))