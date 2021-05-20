
DATA_CHUNK = 1024
MAX_READ_SIZE = 950
DOWNLOAD = "download"
UPLOAD = "upload"
OK = "OK"


class Constants:
    def bytesChunk():
        return DATA_CHUNK

    def getMaxReadSize():
        return MAX_READ_SIZE

    def uploadProtocol():
        return UPLOAD

    def downloadProtocol():
        return DOWNLOAD

    def okProtocol():
        return OK
