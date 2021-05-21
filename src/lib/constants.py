
DATA_CHUNK = 1024
MAX_READ_SIZE = 950
DOWNLOAD = "D"
UPLOAD = "U"
TRANSFER = "T"
ACK = "A"
ERROR = "F"


class Constants:

    def bytesChunk():
        return DATA_CHUNK

    def getMaxReadSize():
        return MAX_READ_SIZE

    def uploadProtocol():
        return UPLOAD

    def downloadProtocol():
        return DOWNLOAD

    def fileTransferProtocol():
        return TRANSFER

    def ackProtocol():
        return ACK

    def errorProtocol():
        return ERROR
