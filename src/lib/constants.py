
DATA_CHUNK = 1024
MAX_READ_SIZE = 950
TTL = 2
DOWNLOAD = "D"
UPLOAD = "U"
TRANSFER = "T"
ACK = "A"
END = "E"
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

    def endProtocol():
        return END

    def ttl():
        return TTL
