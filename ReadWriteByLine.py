def readln_line(inputFile, filePosition):
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
    line = bline.decode("utf-8", errors='ignore')
    currPosition = filePosition + len(line)
    return line, currPosition


def writeln_line(outputFile, line):
    """
    Takes a File Object outputFile and a str line containing a text
    line to be written to the outputFile. Then writes line to
    outputFile.
    
    This function assumes that the outputFile parameter is an already 
    opened file with mode "a+b" and without specifying the buffering
    parameter
    """
    outputFile.write(line.encode("utf-8"))