import mmap
import os
import random
from time import time
from ReadWriteByChar import readln_char
from ReadWriteByLine import readln_line
from ReadWriteByBuffer import readln_buffer
from ReadWriteByMmap import read_bline_mmap

def randjump_char(f, j):
    sum = 0
    count = 0

    fileSize = os.stat(f).st_size
    file = open(f, "r+b", 0)

    while count < j:
        randPosition = random.randint(0, fileSize)
        bline, _ = readln_char(file,randPosition)
        sum += len(bline)
        count += 1

    file.close()
    return sum

def randjump_readln(f, j):
    sum = 0
    count = 0

    fileSize = os.stat(f).st_size
    file = open(f, "r+b")

    while count < j:
        randPosition = random.randint(0, fileSize)
        line, _ = readln_line(file, randPosition)
        sum += len(line)
        print(sum)
        count += 1

    file.close()
    return sum

def randjump_buffer(f, j, bufferSize):
    

def randjump_mmap(f, j, bufferSize):
    sum = 0
    count = 0

    fileSize = os.stat(f).st_size
    file = open(f, "r+b")

    # Obtaining values to be used in mapping, based on the input parameters
    actualBufferSize = (bufferSize // mmap.ALLOCATIONGRANULARITY + 1) * mmap.ALLOCATIONGRANULARITY
    fileSize = os.fstat(file.fileno()).st_size

    prev_current_position = -1

    while count < j:
        randPosition = random.randint(0, fileSize)
        actualFilePosition = randPosition // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY
        
        if fileSize < actualFilePosition + actualBufferSize:
            actualBufferSize = fileSize - actualFilePosition

        if not actualFilePosition <= prev_current_position < actualFilePosition + bufferSize:
            mapping = mmap.mmap(file.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)
        bline, currentPosition = read_bline_mmap(mapping, randPosition, actualFilePosition, bufferSize, actualBufferSize)

        if not b'\n' in bline:
            actualFilePosition = currentPosition // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY

            if fileSize < actualFilePosition + actualBufferSize:
                actualBufferSize = fileSize - actualFilePosition

            mapping = mmap.mmap(file.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)

            line_part, currentPosition = read_bline_mmap(mapping, currentPosition, actualFilePosition, bufferSize, actualBufferSize)
            bline += line_part
        
        line = bline.decode("utf-8")
        prev_current_position = currentPosition
        sum += len(line)
        print(sum)
        count += 1

    file.close()
    return sum