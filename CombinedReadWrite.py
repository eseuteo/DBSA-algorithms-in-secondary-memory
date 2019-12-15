from ReadWriteByMmap import getNewMapRegion, writeln_mmap
from ReadWriteByLine import readln_line, writeln_line
from ReadWriteByBuffer import readln_buffer, writeln_buffer
from ReadWriteByChar import writeln_char
from RandomReading import cannotUseLastBuffer, usedWholeBuffer
from ClassFileObject import FileObject
import os

def initializeFileObjects(file_list):
    files_to_read = []
    for file in file_list:
        files_to_read.append(FileObject(open(file, 'r+b'), 0, False))
    return files_to_read

def initializeFileObjectsBuffer(file_list, bufferSize):
    files_to_read = []
    for file in file_list:
        fileObject = open(file, 'r+b', bufferSize)
        buffer = fileObject.read(bufferSize)
        files_to_read.append(FileObject(fileObject, 0, False, buffer, 0, 0))
    return files_to_read

def rrmerge_Line_Line(file_list, outputFile):
    files_to_read = initializeFileObjects(file_list)
    file_to_write = open(outputFile, 'w+b')
    while not all([x.isClosed for x in files_to_read]):
        for file in files_to_read:
            if not file.isClosed:
                line, file.readPos = readln_line(file.fileObject, file.readPos)
                if not line:
                    file.isClosed = True
                    file.fileObject.close()
                else:
                    writeln_line(file_to_write, line)

def rrmerge_Line_Char(file_list, outputFile):
    files_to_read = initializeFileObjects(file_list)
    file_to_write = open(outputFile, 'w+b')
    while not all([x.isClosed for x in files_to_read]):
        for file in files_to_read:
            if not file.isClosed:
                line, file.readPos = readln_line(file.fileObject, file.readPos)
                if not line:
                    file.isClosed = True
                    file.fileObject.close()
                else:
                    writeln_char(file_to_write, line)

def rrmerge_Buffer_Char(file_list, outputFile, bufferSize):
    files_to_read = initializeFileObjectsBuffer(file_list, bufferSize)
    file_to_write = open(outputFile, 'w+b')
    while not all([x.isClosed for x in files_to_read]):
        for file in files_to_read:
            if not file.isClosed:
                line = b''
                while line is not None and b'\n' not in line:
                    if cannotUseLastBuffer(file.bufferInitPos, file.readPos, bufferSize) or usedWholeBuffer(file.bufferPos, bufferSize):
                        file.readPos += file.bufferPos
                        file.readBuffer = file.fileObject.read(bufferSize)
                        file.bufferInitPos = file.readPos
                        file.bufferPos = 0
                    tempLine, file.bufferPos = readln_buffer(file.readBuffer, file.bufferPos)
                    if tempLine == b'':
                        line = None
                    else:
                        line += tempLine
                        file.readPos += len(tempLine)
                if not line:
                    file.isClosed = True
                    file.fileObject.close()
                else:
                    writeln_char(file_to_write, line)

def rrmerge_Buffer_Line(file_list, outputFile, bufferSize):
    files_to_read = initializeFileObjectsBuffer(file_list, bufferSize)
    file_to_write = open(outputFile, 'w+b')
    while not all([x.isClosed for x in files_to_read]):
        for file in files_to_read:
            if not file.isClosed:
                line = b''
                while line is not None and b'\n' not in line:
                    if cannotUseLastBuffer(file.bufferInitPos, file.readPos, bufferSize) or usedWholeBuffer(file.bufferPos, bufferSize):
                        file.readPos += file.bufferPos
                        file.readBuffer = file.fileObject.read(bufferSize)
                        file.bufferInitPos = file.readPos
                        file.bufferPos = 0
                    tempLine, file.bufferPos = readln_buffer(file.readBuffer, file.bufferPos)
                    if tempLine == b'':
                        line = None
                    else:
                        line += tempLine
                        file.readPos += len(tempLine)
                if not line:
                    file.isClosed = True
                    file.fileObject.close()
                else:
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
