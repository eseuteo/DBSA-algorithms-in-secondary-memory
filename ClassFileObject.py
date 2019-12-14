class FileObject:
    fileObject = None
    readPos = 0
    isClosed = False
    readBuffer = None

    # parameterized constructor
    def __init__(self, fileObject, readPos, isClosed, readBuffer):
        self.fileObject = fileObject
        self.readPos = readPos
        self.isClosed = isClosed
        self.readBuffer = readBuffer
    
