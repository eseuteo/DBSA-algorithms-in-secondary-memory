import mmap
import os

def read_bline(mapping, filePosition, bufferSize):
    """
    Takes a Memory-mapped file object (mapping), an int 
    (filePosition) and an int (bufferSize).
    Returns a byte-list from mapping, starting in filePosition and of
    size bufferSize.
    """
    mapping.seek(filePosition)
    bline = mapping.read(bufferSize)
    return bline

def readln_mmap(mapping, filePosition, actualFilePosition, bufferSize, actualBufferSize):
    """
    Takes a Memory-mapped file object (mapping), an int 
    (filePosition), an int (actualFilePosition), an int (bufferSize) 
    and an int (actualBufferSize).
    Returns the str existing in mapping from (filePosition - 
    actualFilePosition), by chunks of size bufferSize until the next 
    newline, as well as the position the next line starts.
    """
    bline = read_bline(mapping, (filePosition - actualFilePosition), bufferSize)

    if not bline:
        return None, filePosition
        
    newFilePosition = filePosition + len(bline)
    while not b'\n' in bline:
        if newFilePosition + bufferSize > actualFilePosition + actualBufferSize:
            line = bline.decode("utf-8", errors='ignore').split('\n')[0]
            current_position = filePosition + len(line)
            return line, current_position
        newChunk = read_bline(mapping, newFilePosition - actualFilePosition, bufferSize)
        bline += newChunk
        newFilePosition = newFilePosition + len(newChunk)
    line = bline.decode("utf-8", errors='ignore').split('\n')[0] + '\n'
    current_position = filePosition + len(line)
    return line, current_position