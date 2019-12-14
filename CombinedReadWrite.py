from ReadWriteByMmap import getNewMapRegion, writeln_mmap
from ReadWriteByLine import readln_line
import os

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