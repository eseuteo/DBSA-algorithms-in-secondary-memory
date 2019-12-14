from ReadWriteByMmap import getNewMapRegion, writeln_mmap
from ReadWriteByLine import readln_line, writeln_line
from ClassFileObject import FileObject
import os

def rrmerge_Line_Line(file_list):
    files_to_read = []
    file_to_write = open('output', 'r+b')
    for file in file_list:
        files_to_read.append(FileObject(open(file, 'r+b'), 0, False))
    while not all([x.isClosed for x in files_to_read]):
        for file in files_to_read:
            if not file.isClosed:
                line, file.readPos = readln_line(file.fileObject, file.readPos)
                if not line:
                    file.isClosed = True
                writeln_line(file_to_write, line)

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