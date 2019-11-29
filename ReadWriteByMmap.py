import mmap
import os

def readln_mmap(inputFile, filePosition, bufferSize):
    # Obtaining values to be used in mapping, based on the input parameters
    actualFilePosition = filePosition // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY
    actualBufferSize = (bufferSize // mmap.ALLOCATIONGRANULARITY + 1) * mmap.ALLOCATIONGRANULARITY
    fileSize = os.fstat(inputFile.fileno()).st_size

    # Ensure legal mapping (not larger than the file)
    if fileSize < actualFilePosition + actualBufferSize:
        actualBufferSize = fileSize - actualFilePosition

    mapping = mmap.mmap(inputFile.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)
    mapping.seek(filePosition - actualFilePosition)
    chunk = mapping.read(bufferSize)
    if not chunk:
        return None, filePosition
    bline = chunk
    newFilePosition = filePosition + len(bline)
    while not b'\n' in bline:
        actualFilePosition = newFilePosition // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY
        if fileSize < actualFilePosition + actualBufferSize:
            actualBufferSize = fileSize - actualFilePosition
        mapping = mmap.mmap(inputFile.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)
        mapping.seek(newFilePosition - actualFilePosition)
        newChunk = mapping.read(bufferSize)
        if not newChunk:
            break
        bline += newChunk
        newFilePosition = newFilePosition + len(newChunk)
    line = bline.decode("utf-8", errors='ignore').split('\n')[0] + '\n'
    current_position = filePosition + len(line)
    return line, current_position