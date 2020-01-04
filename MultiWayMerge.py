from ReadWriteByLine import readln_line, writeln_line
from ReadWriteByBuffer import readln_buffer
from ReadWriteByMmap import writeln_mmap, getNewMapRegion
from csv import reader
from pathlib import Path
import os
# importing "heapq" to implement heap queue
import heapq
# importing natsort to sort dictionary in natural order
import natsort
import numpy as np

def writeSortedFile(arrLines, k, outputFile, bufferSize):
    sort_index = k - 1 # To sort on the 2nd column, arrLines[1] should be selected
    linesList = []

    # Use csv.reader to split each line by comma
    # The input for reader is a string (not bytes), so the line must be decoded first
    # The normal "split" function should not be used to prevent wrong splits
    # Example:
    #   If the line contains '1,"ABC,DEF",540'
    #   Using the split(",") function would result in 4 splits: ['1','"ABC','DEF"','540']
    #   The correct output should have 3 splits: ['1','"ABC,DEF"','540']
    #   csv.reader generates the correct output
    for bline in arrLines:
        strline = [bline.decode("utf-8")]
        for lineColumns in reader(strline, delimiter=','):
            sortColValue = lineColumns[sort_index]
        linesList.append([sortColValue,bline])
    
    linesList = natsort.natsorted(linesList)

    file_to_write = open(str(Path.cwd()) + str(outputFile), 'w+b')
    # Fill the file with \0
    totalSize = 0
    for line in linesList:
        totalSize += len(line[1])
    file_to_write.write(totalSize * b'\0')

    writePosition = 0

    mapping, actualFilePosition, actualBufferSize = getNewMapRegion(writePosition, bufferSize, totalSize, file_to_write, 1)
    for lineToWrite in linesList:
        mapping, writePosition, actualFilePosition = writeln_mmap(mapping, writePosition, actualFilePosition, actualBufferSize, totalSize, file_to_write, lineToWrite[1])
    file_to_write.close()

def generateSortedFiles(f, k, M, bufferSize):
    rFile = open(f, 'r+b')
    fileName = os.path.basename(rFile.name).split(".")[0]
    sortedFiles = []
    linesToWrite = []

    current_position = 0
    mFileSize = 0
    currentFileIndex = 0

    # File name format for generated files:
    # [ORIGINAL_FILE_NAME]_0.csv
    # (e.g. info_type_0.csv)
    outputFile = "/output/" + fileName + "_" + str(currentFileIndex) + ".csv"

    while True:
        line, current_position = readln_line(rFile, current_position)
        if not line:
            # Write in a file the remaining content and add it to the queue
            writeSortedFile(linesToWrite, k, outputFile, bufferSize)
            heapq.heappush(sortedFiles, (currentFileIndex, outputFile, mFileSize))
            break
        # Add lines to an array
        linesToWrite.append(line)
        mFileSize += len(line)
        if mFileSize > M: # Max file size reached
            # Write lines to file and add it to the queue
            writeSortedFile(linesToWrite, k, outputFile, bufferSize)
            heapq.heappush(sortedFiles, (currentFileIndex, outputFile, mFileSize))
            # Reset variables for next file to be written
            mFileSize = 0
            linesToWrite = []
            currentFileIndex += 1
            outputFile = "/output/" + fileName + "_" + str(currentFileIndex) + ".csv"

    rFile.close()

    return sortedFiles

def extsort_Line_Mmap(f, k, M, d, bufferSize):
    sortedFilesQueue = generateSortedFiles(f, k, M, bufferSize)
    currentFileIndex = len(sortedFilesQueue)

    while len(sortedFilesQueue) > 1:
        # If amount of files is lower than d, then use that number 
        d = min(d, len(sortedFilesQueue))
        # Take d files from heap
        filesToSort = [heapq.heappop(sortedFilesQueue) for x in range(d)]
        count = len(filesToSort)
        fileSize = 0
        # Create bufferList (as a dictionary with two elements: filePosition (int) and buffer (list of str))
        bufferList = [{'filePosition': 0, 'buffer': []} for x in range(d)]

        # Open output file
        rFile = open(f, 'r+b')
        fileName = os.path.basename(rFile.name).split(".")[0]
        outputFileName = "/output/" + fileName + "_" + str(currentFileIndex) + ".csv"
        outputFile = open(str(Path.cwd()) + str(outputFileName), 'w+b')
        # outputFile = open(outputFileName), 'w+b')
        sort_index = k - 1 # To sort on the 2nd column, arrLines[1] should be selected
        #Create array for comparison of MIN line
        linesList = np.empty((d, 2), dtype=object)

        # Buffer and list load for the new D files
        for i in range(d):
            bufferList[i], fileSize = loadBuffer(bufferList[i], filesToSort[i][1], M, count, fileSize)
            linesList = firstLoad(bufferList, linesList, sort_index, i, d)

        # Fill the file with \0
        totalSize = 0
        for _file in filesToSort:
            totalSize += _file[2]
        outputFile.write(totalSize * b'\0')


        writePosition = 0

        mapping, actualFilePosition, actualBufferSize = getNewMapRegion(writePosition, bufferSize, totalSize, outputFile, 1)
        # While still reading at least one file
        while count > 0:
            # Take the minimum line (smallest) and print it on the new file
            bufferListIndex, mapping, writePosition, actualFilePosition = takeMinLineMmap(linesList, outputFile, mapping, writePosition, actualFilePosition, actualBufferSize, totalSize)

            # If read all the file and wrote all the buffer
            if bufferList[bufferListIndex]['buffer'] == [] and bufferList[bufferListIndex]['filePosition'] == -1 and any(value is None for  value in linesList[bufferListIndex]):
                linesList = np.delete(linesList, bufferListIndex, axis=0)
                del bufferList[bufferListIndex]
                count -= 1
                os.remove(str(Path.cwd()) + filesToSort[bufferListIndex][1])
                filesToSort.pop(bufferListIndex)
            else:
                linesList = firstLoad(bufferList, linesList, sort_index, bufferListIndex, d)
                # If already empty
                if bufferList[bufferListIndex]['buffer'] == [] and bufferList[bufferListIndex]['filePosition'] != -1:
                    bufferList[bufferListIndex], fileSize = loadBuffer(bufferList[bufferListIndex], filesToSort[bufferListIndex][1], M, count, fileSize)                
                # If read all the file
                if bufferList[bufferListIndex]['filePosition'] == filesToSort[bufferListIndex][2]:
                    bufferList[bufferListIndex]['filePosition'] = -1

            # linesList = firstLoad(bufferList, linesList, sort_index, bufferListIndex, d)
        
        heapq.heappush(sortedFilesQueue, (currentFileIndex, outputFileName, fileSize))
        currentFileIndex += 1
        outputFile.flush()
        outputFile.close()

    # Print filePath and fileSize from first file in queue
    fileTuple = heapq.heappop(sortedFilesQueue)

    filePath = fileTuple[1]
    fileSize = fileTuple[2]
    print("File: " + str(filePath) + " Size: " + str(fileSize))

    return fileSize

def loadBuffer(buffer, f, M, d, fileSize):
    """
    Takes a dictionary (buffer), an int (filePosition), a str (f),
    an int (M) and an int (d). Then opens the file f and fills buffer
    with lines from f (starting from filePosition (element in the dictionary)) 
    until the size of buffer (in bytes) is greater than M / d.
    """
    file = open(str(Path.cwd()) + str(f), 'r+b')
    # file = open(f, 'r+b')
    maxBufferSize = M / d
    bufferSize = 0

    while bufferSize < maxBufferSize:
        nextLine, buffer['filePosition'] = readln_line(file, buffer['filePosition'])
        if nextLine == b'':
            break
        buffer['buffer'].append(nextLine)
        bufferSize += len(nextLine)
        fileSize += len(nextLine)
    file.close()

    return buffer, fileSize

def firstLoad(bufferList, linesList, sort_index, i, d):
    """
    Funcion de Jesus
    """
    bline = bufferList[i]['buffer'].pop(0)
    strline = [bline.decode("utf-8")]
    for lineColumns in reader(strline, delimiter=','):
        minColValue = lineColumns[sort_index]
    # linesList = np.append(linesList, newLine, axis=0)
    newLine = [minColValue,strline[0]]
    linesList[i] = newLine


    return linesList

def takeMinLine(linesList, outputFile):
    """
    Funcion de Jesus
    """
    # minVal = np.amin(linesList, axis=0)
    # minRow = np.where(linesList == np.amin(linesList))
    minRow = natsort.index_natsorted(linesList, key=lambda x: (x is None, x))
    bufferListIndex = int(minRow[0])
    minLine = natsort.natsorted(linesList, key=lambda x: (x is None, x))
    minBytes = bytes(minLine[0][1], 'utf-8')
    # print(minBytes)
    writeln_line(outputFile, minBytes)
    linesList[bufferListIndex] = [None, None]

    return bufferListIndex

def takeMinLineMmap(linesList, outputFile, mapping, writePos, actualFilePos, mapSize, rFileSize):
    """
    Funcion de Jesus
    """
    minRow = natsort.index_natsorted(linesList, key=lambda x: (x is None, x))
    bufferListIndex = int(minRow[0])
    minLine = natsort.natsorted(linesList, key=lambda x: (x is None, x))
    minBytes = bytes(minLine[0][1], 'utf-8')

    mapping, writePos, actualFilePos = writeln_mmap(mapping, writePos, actualFilePos, mapSize, rFileSize, outputFile, minBytes)

    linesList[bufferListIndex] = [None, None]

    return bufferListIndex, mapping, writePos, actualFilePos
