import mmap
import os
import random
from time import time
from ReadWriteByChar import readln_char
from ReadWriteByLine import readln_line
from ReadWriteByBuffer import readln_buffer
from ReadWriteByMmap import read_bline_mmap

def randjump_char(f, j):
    """
    Given a file and an integer j, performs j jumps inside the file
    and reads (char approach) j lines. Returns the amount of bytes read.
    """
    sum = 0
    count = 0

    fileSize = os.stat(f).st_size - 1
    file = open(f, "r+b", 0)

    while count < j:
        randPosition = random.randint(0, fileSize)
        bline, _ = readln_char(file,randPosition)
        sum += len(bline)
        count += 1

    file.close()
    return sum

def randjump_readln(f, j):
    """
    Given a file and an integer j, performs j jumps inside the file
    and reads (line approach) j lines. Returns the amount of bytes read.
    """
    sum = 0
    count = 0

    fileSize = os.stat(f).st_size - 1
    file = open(f, "r+b")

    while count < j:
        randPosition = random.randint(0, fileSize)
        line, _ = readln_line(file, randPosition)
        sum += len(line)
        count += 1

    file.close()
    return sum

def cannotUseLastBuffer(bufferStart, newPosition, bufferSize):
    """
    Auxiliary function for assessing if the previous jump buffer can
    be reused.
    """
    return not bufferStart <= newPosition < bufferStart + bufferSize

def usedWholeBuffer(currentPosition, bufferSize):
    """
    Auxiliary function for assessing if the current buffer has been
    completely used.
    """
    return currentPosition == bufferSize

def randjump_buffer(f, j, bufferSize):
    """
    Given a file, an integer j and a bufferSize, performs j jumps 
    inside the file and reads (buffered approach) j lines. Returns 
    the amount of bytes read.
    """
    sum = 0
    count = 0

    fileSize = os.stat(f).st_size - 1
    file = open(f, "r+b")

    prevBufferStartingPoint = -1
    buffer = None

    while count < j:
        randPosition = random.randint(0, fileSize)
        overallPosition = randPosition
        currentPositionInBuffer = 0

        line = b''
        while b'\n' not in line:
            if not buffer or cannotUseLastBuffer(prevBufferStartingPoint, randPosition, bufferSize) or usedWholeBuffer(currentPositionInBuffer, bufferSize):
                overallPosition += currentPositionInBuffer
                file.seek(overallPosition)
                buffer = file.read(bufferSize)
                currentPositionInBuffer = 0
                prevBufferStartingPoint = overallPosition
            tempLine, currentPositionInBuffer = readln_buffer(buffer, currentPositionInBuffer)
            line += tempLine

        sum += len(line)
        count += 1
    
    file.close()
    return sum

def randjump_mmap(f, j, bufferSize):
    """
    Given a file, an integer j and a bufferSize, performs j jumps 
    inside the file and reads (mapped approach) j lines. Returns 
    the amount of bytes read.
    """
    sum = 0
    count = 0

    fileSize = os.stat(f).st_size
    file = open(f, "r+b")

    # Obtaining values to be used in mapping, based on the input parameters
    actualBufferSize = (bufferSize // mmap.ALLOCATIONGRANULARITY + 1) * mmap.ALLOCATIONGRANULARITY

    prevMappingStartingPoint = -1
    mapping = None

    # Declare actualFilePosition variable
    actualFilePosition = 0

    while count < j:
        randPosition = random.randint(0, fileSize - 1)
        currentPositionInMapping = randPosition
        
        bline = b''
        # While we dont get a complete line
        while not b'\n' in bline:
            # If we need to remap or create the first mapped portion
            if not mapping or cannotUseLastBuffer(prevMappingStartingPoint, randPosition, bufferSize) or usedWholeBuffer(currentPositionInMapping - actualFilePosition, actualBufferSize):
                # Determine the offset
                actualFilePosition = currentPositionInMapping // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY
                # Trim the size of the buffer if it excedes the size of the file
                if fileSize < actualFilePosition + actualBufferSize:
                    actualBufferSize = fileSize - actualFilePosition
                # Create the mapping
                mapping = mmap.mmap(file.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)
                # Store the starting point of mapping (so it is used if next randPosition is in the same mapped portion)
                prevMappingStartingPoint = actualFilePosition
                actualBufferSize = (bufferSize // mmap.ALLOCATIONGRANULARITY + 1) * mmap.ALLOCATIONGRANULARITY
            # Read bline to tempLine, update currentPositionInMapping
            tempLine, currentPositionInMapping = read_bline_mmap(mapping, currentPositionInMapping, actualFilePosition, bufferSize, actualBufferSize)
            bline += tempLine
        
        line = bline.decode("utf-8", errors="ignore")
        sum += len(line)
        count += 1

    file.close()
    return sum