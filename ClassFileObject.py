class FileObject:
    """
    Class created for the experiment 1.3.
    """
    fileObject = None
    readPos = 0
    isClosed = False
    readBuffer = None
    bufferInitPos = None
    bufferPos = None

    # parameterized constructor
    def __init__(self, fileObject, readPos, isClosed, readBuffer = None, bufferInitPos = None, bufferPos = None):
        self.fileObject = fileObject
        self.readPos = readPos
        self.isClosed = isClosed
        self.readBuffer = readBuffer
        self.bufferInitPos = bufferInitPos
        self.bufferPos = bufferPos
    
