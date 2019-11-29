import random
import os
import mmap
from time import time

def readln(inputFile, filePosition):
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
    line = bline.decode("utf-8")
    currPosition = filePosition + len(line)
    return line, currPosition


def writeln(outputFile, line):
    """
    Takes a File Object outputFile and a str line containing a text
    line to be written to the outputFile. Then writes line to
    outputFile.
    
    This function assumes that the outputFile parameter is an already 
    opened file with mode "a+b" and without specifying the buffering
    parameter
    """
    outputFile.write(line.encode("utf-8"))


def readln_buffer(inputFile, filePosition, bufferSize):
    """
    Takes a File Object inputFile, an int filePosition that indicates
    a position in a file and an int bufferSize that indicates the 
    size of the buffer to read from the file. Returns the str 
    existing from the position indicated until the next newline, as 
    well as the position the File Object indicates now.
    
    This function assumes that the inputFile parameter is an already 
    opened file with mode "r+b" and specifying a certain buffering
    parameter
    """
    inputFile.seek(filePosition)
    chunk = inputFile.read(bufferSize)
    if not chunk:
        return None, filePosition
    bline = chunk
    while not b'\n' in bline:
        newChunk = inputFile.read(bufferSize)
        if not newChunk:
            break
        bline += newChunk
    line = bline.decode("utf-8", errors='ignore').split('\n')[0] + '\n'
    current_position = filePosition + len(line)
    return line, current_position

def writeln_buffer(outputFile, line, bufferSize):
    """
    Takes a File Object outputFile, a str line containing a text line
    to be written to the outputFile and a bufferSize. Then writes
    line to the outputFile by decomposing it into chunks of size
    bufferSize.
    
    This function assumes that the outputFile parameter is an already 
    opened file with mode "a+b" and specifying a certain buffering
    parameter (bufferSize)
    """
    chunkList = [line[i:i+bufferSize] for i in range(0, len(line), bufferSize)]
    for chunk in chunkList:
        outputFile.write(chunk.encode("utf-8"))

def readln_mmap(inputFile, filePosition, bufferSize):
    # Obtaining values to be used in mapping, based on the input parameters
    actualFilePosition = filePosition // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY
    actualBufferSize = (bufferSize // mmap.ALLOCATIONGRANULARITY + 1) * mmap.ALLOCATIONGRANULARITY
    fileSize = os.fstat(inputFile.fileno()).st_size

    # Ensure legal mapping (not larger than the file)
    if fileSize < actualFilePosition + actualBufferSize:
        actualBufferSize = fileSize - actualFilePosition

    mapping = mmap.mmap(inputFile.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)
    mapping.seek(filePosition - actualFilePosition)
    chunk = mapping.read(bufferSize)
    if not chunk:
        return None, filePosition
    bline = chunk
    newFilePosition = filePosition + len(bline)
    while not b'\n' in bline:
        actualFilePosition = newFilePosition // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY
        # print('New position: ' + str(newFilePosition))
        # print('Actual position: ' + str(actualFilePosition))
        if fileSize < actualFilePosition + actualBufferSize:
            actualBufferSize = fileSize - actualFilePosition
        mapping = mmap.mmap(inputFile.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)
        # print(mapping.tell())
        mapping.seek(newFilePosition - actualFilePosition)
        # print(mapping.tell())
        newChunk = mapping.read(bufferSize)
        if not newChunk:
            break
        bline += newChunk
        newFilePosition = newFilePosition + len(newChunk)
    line = bline.decode("utf-8", errors='ignore').split('\n')[0] + '\n'
    current_position = filePosition + len(line)
    return line, current_position



    # if fileSize < (actualFilePosition + mmap.ALLOCATIONGRANULARITY):
    #     mapping = mmap.mmap(inputFile.fileno(), fileSize - mmap.ALLOCATIONGRANULARITY * actualFilePosition, access=mmap.ACCESS_READ, offset=(actualFilePosition * mmap.ALLOCATIONGRANULARITY))
    # else:    
    #     mapping = mmap.mmap(inputFile.fileno(), mmap.ALLOCATIONGRANULARITY, access=mmap.ACCESS_READ, offset=(actualFilePosition * mmap.ALLOCATIONGRANULARITY))
    # mapping.seek(filePosition - (actualFilePosition * mmap.ALLOCATIONGRANULARITY))
    # bline = mapping.read(bufferSize)
    # newFilePosition = filePosition + len(bline)
    # while not '\\n' in str(bline):
    #     actualFilePosition = newFilePosition // mmap.ALLOCATIONGRANULARITY
    #     if fileSize < mmap.ALLOCATIONGRANULARITY * (actualFilePosition + 1):
    #         mapping = mmap.mmap(inputFile.fileno(), fileSize - mmap.ALLOCATIONGRANULARITY * actualFilePosition, access=mmap.ACCESS_READ, offset=(actualFilePosition * mmap.ALLOCATIONGRANULARITY))
    #     else:
    #         mapping = mmap.mmap(inputFile.fileno(), mmap.ALLOCATIONGRANULARITY, access=mmap.ACCESS_READ, offset=(actualFilePosition * mmap.ALLOCATIONGRANULARITY))
    #     mapping.seek(newFilePosition - (actualFilePosition * mmap.ALLOCATIONGRANULARITY))
    #     newChunk = mapping.read(bufferSize)
    #     if not newChunk:
    #         break
    #     bline += newChunk
    #     newFilePosition += len(newChunk)
    # line = bline.decode("utf-8", errors='replace').split('\n')[0] + '\n'
    # current_position = filePosition + len(line)
    # return line, current_position


def length_readln(fileName):
    file = open(fileName, 'r+b')
    sum = 0
    current_position = 0

    while True:
        line, current_position = readln(file, current_position)
        if not line:
            break
        sum += len(line)

    file.close()
    return sum

def length_readln_buffer(fileName, bufferSize):
    file = open(fileName, 'r+b', bufferSize)
    sum = 0
    current_position = 0
    while True:
        line, current_position = readln_buffer(file, current_position, bufferSize)
        # print(line)
        # print(current_position)
        if not line or line == "b''":
            break
        sum += len(line)
    file.close()
    return sum

def length_readln_mmap(fileName, bufferSize):
    file = open(fileName, 'r+b', bufferSize)
    sum = 0
    current_position = 0

    while True:
        line, current_position = readln_mmap(file, current_position, bufferSize)
        # print(current_position)
        if not line or line == "b''":
            break
        sum += len(line)

    file.close()
    return sum

def randomJump_readln(fileName, j):
    file = open(fileName, "r+b")
    
    fileSize = os.fstat(file.fileno()).st_size - 1
    sum = 0
    i = 0
    while i < j:
        filePosition = random.randint(0, fileSize)
        line = readln(file, filePosition)
        sum += len(line)
        print(sum)
        i += 1

    file.close()
    return sum

def randomJump_readln_buffer(fileName, j, bufferSize):
    file = open(fileName, "r+b")
    
    fileSize = os.fstat(file.fileno()).st_size - 1
    sum = 0
    i = 0
    while i < j:
        filePosition = random.randint(0, fileSize)
        line = readln_buffer(file, filePosition, bufferSize)
        sum += len(line)
        print(sum)
        i += 1

    file.close()
    return sum

# Main

# read_file = open('test2.txt', mode = 'r+b')
# print(readln(read_file, 4090))
# read_file = open('test2.txt', mode = 'r+b')
# print(readln_buffer(read_file, 4090, 24))
# read_file = open('test2.txt', mode = 'r+b')
# print(readln_mmap(read_file, 4090, 24))

start = time()
result = length_readln('/home/ricardohb/Documents/development/dbsa_project/aka_name.csv')
end = time()
print(result)
print(end - start)

start = time()
result = length_readln_buffer('/home/ricardohb/Documents/development/dbsa_project/aka_name.csv', 100)
end = time()
print(result)
print(end - start)

start = time()
result = length_readln_mmap('/home/ricardohb/Documents/development/dbsa_project/aka_name.csv', 100)
end = time()
print(result)
print(end - start)


# Testing functions

# buffering_file = open('output_writeln_buffer.txt', mode='a+b', buffering=3)
# writeln_buffer(buffering_file, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, ", 3)
# buffering_file.close()

# file = open('output_writeln.txt', mode='a+b')
# writeln(file, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, ")
# file.close()

# read_file = open('test.txt', mode='r+b')
# print(readln(read_file, 10))
# read_file.close()

# buffering_read_file = open('test.txt', mode='r+b', buffering=3)
# print(readln_buffer(buffering_read_file, 10, 3))
# buffering_read_file.close()

# file = open('test_writing.txt', mode='r+')
# print(readln(file))
# print(readln(file, 100))
# print(readln_buffer(file, 14, 200))
# print(readln_buffer(file, 14))

# writeln('test.txt', 'Ut enim ad minim veniam, quis nostrud exercitation')

# write_buffer('test.txt', 'Ut enim ad minim veniam, quis nostrud exercitation', 10)
