import mmap
import os
from time import time
import random
from ReadWriteByChar import readln_char
from ReadWriteByLine import readln_line
from ReadWriteByBuffer import readln_buffer
from ReadWriteByMmap import read_bline_mmap

#------------------------------------
# Random Reading function - Character

#------------------------------------
# Random Reading function - Buffer Not Defined

#------------------------------------
# Random Reading function - Buffer Defined
def length_buffer_rand(fileName, randJumps, bufferSize):
    inputFile = open(fileName, 'r+b', bufferSize)
    # sumChunk = 0
    sum = 0
    fileSize = os.fstat(inputFile.fileno()).st_size

    numlst = []
    while len(numlst) < randJumps:
        rnd = random.randint(0,fileSize)
        if rnd in numlst:
            continue
        else:
            numlst += [rnd]
    
    print(numlst)

    bufferFilePosition = 0
    bufferPosition = 0
    inputFile.seek(bufferFilePosition)
    chunk = inputFile.read(bufferSize)
    print(chunk)

    for n in numlst:
        isLineComplete = 1
        bLineTemp = b""
        print("Reading position: " + str(n))
        end = 0

        if n < bufferFilePosition or n > (bufferFilePosition + bufferSize):
            inputFile.seek(n)
            chunk = inputFile.read(bufferSize)
            bufferFilePosition = n
            bufferPosition = 0
            print(chunk)
        else:
            bufferPosition += (n - bufferFilePosition)
    
        while True:
            bline, bufferPosition = readln_buffer(chunk, bufferPosition)

            # Line (or part of a line) has already been read, so values are updated
            lineLength = len(bline)
            sum += lineLength
            # sumChunk += lineLength

            if bline.find(b"\n") == -1: # End of line was not found in latest line read
                isLineComplete = 0
                bLineTemp += bline # Since line is incomplete, the part of the line already read is stored in a temporary variable
            elif isLineComplete == 0: # Char '\n' is found but there is an incomplete line pending
                bline = bLineTemp + bline
                isLineComplete = 1

            if isLineComplete == 1:
                print(bline.decode("utf-8")) # This is where something can be done with lines read
                bLineTemp = b""
                break

            # If we read the last line of the file, we need to let know the system the file has ended and can't read further
            if bufferFilePosition + bufferPosition >= fileSize:
                end = 1
            
            # Quite the loop if file ends
            if end == 1:
                break
            
            # If the code reaches this part, it means that the buffer was read entirely but the file still has more data
            bufferFilePosition += bufferPosition
            inputFile.seek(bufferFilePosition)
            chunk = inputFile.read(bufferSize)
            bufferPosition = 0
            
    inputFile.close()
    return sum