from ReadWriteByLine import readln_line, writeln_line
from csv import reader
import os
# importing "heapq" to implement heap queue
import heapq
# importing natsort to sort dictionary in natural order
import natsort

def writeSortedFile(arrLines, k, outputFile):
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

    file_to_write = open(outputFile, 'w+b')
    for lineToWrite in linesList:
        writeln_line(file_to_write, lineToWrite[1])
    file_to_write.close()

def generateSortedFiles(f, k, M):
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
    outputFile = "output/" + fileName + "_" + str(currentFileIndex) + ".csv"

    while True:
        line, current_position = readln_line(rFile, current_position)
        if not line:
            # Write in a file the remaining content and add it to the queue
            writeSortedFile(linesToWrite, k, outputFile)
            heapq.heappush(sortedFiles, (currentFileIndex, outputFile, mFileSize))
            break
        # Add lines to an array
        linesToWrite.append(line)
        mFileSize += len(line)
        if mFileSize > M: # Max file size reached
            # Write lines to file and add it to the queue
            writeSortedFile(linesToWrite, k, outputFile)
            heapq.heappush(sortedFiles, (currentFileIndex, outputFile, mFileSize))
            # Reset variables for next file to be written
            mFileSize = 0
            linesToWrite = []
            currentFileIndex += 1
            outputFile = "output/" + fileName + "_" + str(currentFileIndex) + ".csv"

    rFile.close()

    return sortedFiles

def extsort_Line_Line(f, k, M, d):
    sortedFilesQueue = generateSortedFiles(f, k, M)

    # Print complete list
    print(list(sortedFilesQueue))

    currentFileIndex = len(sortedFilesQueue)
    while len(sortedFilesQueue) > 1:
        # Take d files from heap
        filesToSort = [heapq.heappop(sortedFilesQueue) for x in range(d)]
        count = len(filesToSort)
        # Create bufferList (as a dictionary with two elements: filePosition (int) and buffer (list of str))
        bufferList = [{'filePosition': 0, 'buffer': []} for x in range(d)]

        # Open output file
        rFile = open(f, 'r+b')
        fileName = os.path.basename(rFile.name).split(".")[0]
        outputFileName = "output/" + fileName + "_" + str(currentFileIndex) + ".csv"
        outputFile = open(outputFileName, 'w+b')
        currentFileIndex += 1

        # While still reading at least one file
        while count > 0:
            # Check each buffer
            for i in range(d):
                # If already empty
                if bufferList[i]['buffer'] == []:
                    bufferList[i] = loadBuffer(bufferList[i], filesToSort[i][1], M, count)
                # If read all the file
                if bufferList[i]['filePosition'] == filesToSort[i][2]:
                    count -= 1
                    os.remove(filesToSort[i][1])
            ### Aquí se llama a tu función, Jesús ###
            # bufferList es una lista de diccionarios:
                # la key "buffer" (se accede como bufferList[índice]['buffer'] contiene una lista de byte strings)
                # la key "filePosition" contiene el índice del buffer dentro del archivo (creo que esto no lo necesitas para nada)
            # outputFile es un fileObject abierto con 'w+b'
            # k es la columna con respecto a la que hay que ordenar (no sé si es necesario, creo que sí)
            ##########################################
            takeMinLine(bufferList, outputFile, k)        

    # Print filePath and fileSize from first file in queue
    fileTuple = heapq.heappop(sortedFilesQueue)

    filePath = fileTuple[1]
    fileSize = fileTuple[2]
    print("File: " + str(filePath) + " Size: " + str(fileSize))

    return 0

def loadBuffer(buffer, f, M, d):
    """
    Takes a dictionary (buffer), an int (filePosition), a str (f),
    an int (M) and an int (d). Then opens the file f and fills buffer
    with lines from f (starting from filePosition (element in the dictionary)) 
    until the size of buffer (in bytes) is greater than M / d.
    """
    file = open(f, 'r+b')
    maxBufferSize = M / d
    bufferSize = 0

    while bufferSize < maxBufferSize:
        nextLine, buffer['filePosition'] = readln_line(file, buffer['filePosition'])
        buffer['buffer'].append(nextLine)
        bufferSize += len(nextLine)
    file.close()

    return buffer

def takeMinLine(bufferList, outputFile, k):
    """
    Funcion de Jesus
    """
    return 0