import mmap
import os
from time import time

def readln_line(inputFile, filePosition):
    """
    Takes a File Object inputFile and an int that indicates a
    position in a file and returns the str existing from the
    position indicated until the next newline, as well as the
    position the File Object indicates now.

    This function assumes that the inputFile parameter is an already 
    opened file with mode "r+b" and without specifying the buffering
    parameter
    """
    
    bline = b""

    inputFile.seek(filePosition)
    currPosition = inputFile.tell()

    bline = inputFile.readline()
    # line = bline.decode("utf-8", errors='ignore')
    currPosition = filePosition + len(bline)
    return bline, currPosition

def getNewMapRegion(currentPosition, bufferSize, fileSize, fileToMap, readWriteFlag):
    # Obtaining values to be used in mapping, based on the input parameters
    actualFilePosition = currentPosition // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY

    if (bufferSize % mmap.ALLOCATIONGRANULARITY) == 0:
        actualBufferSize = bufferSize
    else:
        actualBufferSize = (bufferSize // mmap.ALLOCATIONGRANULARITY + 1) * mmap.ALLOCATIONGRANULARITY

    # Ensure legal mapping (not larger than the file)
    if fileSize < actualFilePosition + actualBufferSize:
        actualBufferSize = fileSize - actualFilePosition
    
    if(readWriteFlag == 0): # Read
        mapping = mmap.mmap(fileToMap.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)
    else: # Write
        mapping = mmap.mmap(fileToMap.fileno(), actualBufferSize, access=mmap.ACCESS_WRITE, offset=actualFilePosition)

    return mapping, actualFilePosition, actualBufferSize

def writeln_mmap(mapping, writePos, actualFilePos, mapSize, rFileSize, wFile, blineToWrite):
    # Calculate write position relative to the start of the mapped region
    mapPos = writePos - actualFilePos
    # print("Write Pos: " + str(writePos) + " ActualPos: " + str(actualFilePos))
    # print("Map Pos: " + str(mapPos) + " Map Size: " + str(mapSize) + " Line: " + blineToWrite.decode("utf-8") + " Line length: " + str(len(blineToWrite)))
    mapping.seek(mapPos)

    lenLine = len(blineToWrite)
    # Check if line can fit in remaining space mapped
    if((mapPos + lenLine) > mapSize):
        # If line cannot fit, write only the segment of the line that fits on the remaining space of the mapped region
        lineSegmentSize = mapSize - mapPos
        lineSegment = blineToWrite[:lineSegmentSize]
        # print("Line: " + blineToWrite.decode("utf-8") + " Length: " +  str(lenLine) + " Map Pos: " + str(mapPos) + " Map Size: " + str(mapSize) + " Segment: " + lineSegment.decode("utf-8"))
        mapping.write(lineSegment)

        writePos += len(lineSegment) # Should be equivalent to actualFilePos + mapSize

        # Map a new region of the file to write the remaining line segment
        mapping, actualFilePos, _ = getNewMapRegion(writePos, mapSize, rFileSize, wFile, 1)

        lineSegment = blineToWrite[lineSegmentSize:]
        mapping.write(lineSegment)

        writePos += len(lineSegment)
    else:
        # If line fits, write the complete line into the mapped region
        mapping.write(blineToWrite)
        writePos += len(blineToWrite)
    
    return mapping, writePos, actualFilePos

# Based on length_line
def read_length_line_write_mmap(inputFile, outputFile, bufferSize, writePosition):
    rFile = open(inputFile, 'r+b')
    currentReadPosition = 0

    rFileSize = os.fstat(rFile.fileno()).st_size

    wFile = open(outputFile, 'r+b')

    mapping, actualFilePosition, actualBufferSize = getNewMapRegion(writePosition, bufferSize, rFileSize, wFile, 1)

    while True:
        bline, currentReadPosition = readln_line(rFile, currentReadPosition)
        if not bline:
            break
        mapping, writePosition, actualFilePosition = writeln_mmap(mapping, writePosition, actualFilePosition, actualBufferSize, rFileSize, wFile, bline)
    
    mapping.close
    wFile.close()
    rFile.close()

# # Main
filePath = "C:/tmp_DSA/test/"
inputFileName = "aka_name.csv"
outputFileName = "mmap_test.csv"

inputFile = filePath + inputFileName
outputFile = filePath + outputFileName
bufferSize = 100
writePosition = 0

read_length_line_write_mmap(inputFile, outputFile, bufferSize, writePosition)