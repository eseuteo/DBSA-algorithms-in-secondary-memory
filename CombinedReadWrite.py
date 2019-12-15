from ReadWriteByMmap import getNewMapRegion, writeln_mmap
from ReadWriteByLine import readln_line, writeln_line
from ReadWriteByBuffer import readln_buffer
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