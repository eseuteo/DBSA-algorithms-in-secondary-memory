from ReadWriteByMmap import getNewMapRegion, writeln_mmap
from ReadWriteByLine import readln_line, writeln_line
from ReadWriteByBuffer import readln_buffer, writeln_buffer
from ClassFileObject import FileObject
import os

def rrmerge_Line_Line(file_list, outputFile):
    files_to_read = []
    file_to_write = open(outputFile, 'r+b')
    for file in file_list:
        files_to_read.append(FileObject(open(file, 'r+b'), 0, False))
    while not all([x.isClosed for x in files_to_read]):
        for file in files_to_read:
            if not file.isClosed:
                line, file.readPos = readln_line(file.fileObject, file.readPos)
                if not line:
                    file.isClosed = True
                writeln_line(file_to_write, line)

# Read/Write with defined buffer size
# Based on length_line
def rrmerge_line_buffer(fileListArray, outputFilePath, bufferSize):
    fileObjectArray = []
    outputFile = open(outputFilePath, 'w+b')
    for file in fileListArray:
        fileObjectArray.append(FileObject(open(file, 'r+b'), 0, False))
    while not all([x.isClosed for x in fileObjectArray]):
        for file in fileObjectArray:
            if not file.isClosed:
                line, file.readPos = readln_line(file.fileObject, file.readPos)
                if not line:
                    file.isClosed = True
                else:
                    writeln_buffer(outputFile, line, bufferSize)

def rrmerge_line_mmap(inputFiles, outputFile, bufferSize, writePosition):
    files_to_read = []
    totalSize = 0

    for inputFile in inputFiles:
        rFile = open(inputFile, 'r+b')

        rFileSize = os.fstat(rFile.fileno()).st_size
        totalSize += rFileSize

        files_to_read.append(FileObject(rFile, 0, False, None))
    
    wFile = open(outputFile, 'w+b')

    mapping, actualFilePosition, actualBufferSize = getNewMapRegion(writePosition, bufferSize, totalSize, wFile, 1)
    
    while not all([x.isClosed for x in files_to_read]):
        for file in files_to_read:
            if not file.isClosed:
                bline, file.readPos = readln_line(file.fileObject, file.readPos)
                if not bline:
                    file.fileObject.close()
                    file.isClosed = True
                else:
                    mapping, writePosition, actualFilePosition = writeln_mmap(mapping, writePosition, actualFilePosition, actualBufferSize, totalSize, wFile, bline)
    mapping.close
    wFile.close()
