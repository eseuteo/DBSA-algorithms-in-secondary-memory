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

def read_bline_mmap(mapping, filePosition, actualFilePosition, bufferSize, actualBufferSize):
    """
    Takes a Memory-mapped file object (mapping), an int 
    (filePosition), an int (actualFilePosition), an int (bufferSize) 
    and an int (actualBufferSize).
    Returns the byte string existing in mapping from (filePosition - 
    actualFilePosition), by chunks of size bufferSize until the next 
    newline, as well as the position the next line starts.
    """
    bline = read_bline(mapping, (filePosition - actualFilePosition), bufferSize)

    if not bline:
        return None, filePosition

    trailingNewLine = b'\n'

    while not b'\n' in bline:
        chunk = bline
        newFilePosition = filePosition + len(chunk)
        if newFilePosition + bufferSize > actualFilePosition + actualBufferSize:
            trailingNewLine = b''
            break
        chunk = read_bline(mapping, newFilePosition - actualFilePosition, bufferSize)
        bline += chunk

    line = bline.split(b'\n')[0] + trailingNewLine
    current_position = filePosition + len(line)
    return line, current_position