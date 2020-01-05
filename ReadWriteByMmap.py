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
    newline (or until the end of the mapped portion), as well as the 
    position the next line starts.
    """
    bline = read_bline(mapping, (filePosition - actualFilePosition), bufferSize)

    if not bline:
        return None, filePosition + 1

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

def writeln_mmap(mapping, writePos, actualFilePos, mapSize, rFileSize, wFile, blineToWrite):
    """
    Takes a mapping, a position, an actual position (based on the
    ALLOCATION GRANULARITY), a mapped portion size, the size of
    the file read, a file to write and a line (byte string) and
    writes the line into the file to write starting from position
    writePos.
    If necessary, remaps the portion mapped.
    Returns the mapping, the new writePos and the new actualFilePos.
    """
    # Calculate write position relative to the start of the mapped region
    mapPos = writePos - actualFilePos
    mapping.seek(mapPos)

    lenLine = len(blineToWrite)
    # Check if line can fit in remaining space mapped
    if((mapPos + lenLine) > mapSize):
        # If line cannot fit, write only the segment of the line that fits on the remaining space of the mapped region
        lineSegmentSize = mapSize - mapPos
        lineSegment = blineToWrite[:lineSegmentSize]
        mapping.write(lineSegment)

        writePos += len(lineSegment) # Should be equivalent to actualFilePos + mapSize

        # Map a new region of the file to write the remaining line segment
        mapping, actualFilePos, _ = getNewMapRegion(writePos, mapSize, rFileSize, wFile, 1)

        lineSegment = blineToWrite[lineSegmentSize:]
        mapping.write(lineSegment)

        writePos += len(lineSegment)
    else:
        # If line fits, write the complete line into the mapped region
        mapping.write(blineToWrite)
        writePos += len(blineToWrite)
    
    return mapping, writePos, actualFilePos

def getNewMapRegion(currentPosition, bufferSize, fileSize, fileToMap, readWriteFlag):
    """
    Given a position, a mapSize, a fileSize, a file and a flag,
    creates a mapping for reading or writing (depending on the
    flag) and returns it together with the actualFilePosition
    and the actualBufferSize.
    This function aims to simplify the process of working with
    memory mapping.
    """
    # Obtaining values to be used in mapping, based on the input parameters
    actualFilePosition = currentPosition // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY

    if (bufferSize % mmap.ALLOCATIONGRANULARITY) == 0:
        actualBufferSize = bufferSize
    else:
        actualBufferSize = (bufferSize // mmap.ALLOCATIONGRANULARITY + 1) * mmap.ALLOCATIONGRANULARITY

    # Ensure legal mapping (not larger than the file)
    if fileSize < actualFilePosition + actualBufferSize:
        actualBufferSize = fileSize - actualFilePosition
    
    if(readWriteFlag == 0): # Read
        mapping = mmap.mmap(fileToMap.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)
    else: # Write
        mapping = mmap.mmap(fileToMap.fileno(), actualBufferSize, access=mmap.ACCESS_WRITE, offset=actualFilePosition)

    return mapping, actualFilePosition, actualBufferSize
