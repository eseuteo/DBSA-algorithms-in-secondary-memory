import datetime
from random import randint
import os

#------------------------------------
# readln_char 
# This function assumes that the inputFile parameter is an already opened file.
# To open file for reading in binary mode switching buffering off:
# file = open(outputFile, "r+b", 0)
def readln_char(inputFile, filePosition):
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
#------------------------------------

#------------------------------------
# writeln_char 
# This function assumes that the outputFile parameter is an already opened file.
# To open file for writing (appending) in binary mode switching buffering off:
# file = open(outputFile, "a+b", 0)
def writeln_char(outputFile, line):
  lineLength = len(line)

  for n in range(0, lineLength-1):
    c = line[n]
    outputFile.write(c.encode("utf-8"))
  
  outputFile.write(b"\n")
  # Command file.close() is done by the calling function
#------------------------------------

#------------------------------------
# Sequential Reading function - Character
def length_char(f):
  sum = 0
  seekPos = 0
  # line = ""

  # Open file for reading in binary mode switching buffering off
  file = open(f, "r+b", 0)

  # Read all lines in a file. readln_char returns the line that was read and the position of the next line to be read
  # When the end of the file is reached, seekPos will be -1, ending the loop
  while seekPos != -1:
    bline, seekPos = readln_char(file,seekPos)
    sum += len(bline)
    # line = bline.decode("utf-8")

  file.close()

  print("Length: " + str(sum))
#------------------------------------

#------------------------------------
# Random  Reading function - Character
def randjump(f, j):
  sum = 0
  count = 0

  fileSize = os.stat(f).st_size
  # print("File size = " + str(fileSize))

  # Open file for reading in binary mode switching buffering off
  file = open(f, "r+b", 0)

  while count < j:
    randPos = randint(0, fileSize)
    # print("Pos: " + str(randPos))
    bline, finalReadPos = readln_char(file,randPos)
    # print("Result: " + str(randPos) + "|" + bline.decode("utf-8") + "|" + str(finalReadPos))
    sum += len(bline)

    count += 1

  file.close()

  print("Length: " + str(sum))
#------------------------------------

# Main
filePath = "C:/tmp_DSA/imdb/"
fileName = "name.csv"

inputFile = filePath + fileName
randomJumps = 100000

#+++
# Sequential reading
start = datetime.datetime.now()
length_char(inputFile) # Sequential Reading
end = datetime.datetime.now()
executionTime = end - start
time_ms = int(executionTime.total_seconds() * 1000) # milliseconds
print("Sequential Reading (By Character) Time: " + str(time_ms) + "ms")
#+++

#+++
# Random reading
# start = datetime.datetime.now()
# randjump(inputFile,randomJumps)
# end = datetime.datetime.now()
# executionTime = end - start
# time_ms = int(executionTime.total_seconds() * 1000) # milliseconds
# print("Random Reading (By Character) Time: " + str(time_ms) + "ms")
#+++

# Write line by character
# fileName = "demoWrite.txt"
# outputFile = filePath + fileName
# lineToWrite = "Write line into a TXT file."
# file = open(outputFile, "a+b", 0)
# writeln_char(file, lineToWrite)
# file.close()