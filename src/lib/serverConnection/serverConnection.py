from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.logger.logger import Logger


class ServerConnection:
    def startCommunicating(s, files, sPath, v, q):
        try:
            while True:
                data, addr = s.recvfrom(Constants.bytesChunk())
                print('received message')
                msg = data.decode()
                ServerConnection.process(s, files, msg, addr, sPath, v, q)
            return
        except Exception:
            print("Error")
            return

    def process(s, files, msg, addr, sPath, v, q):
        mode = msg[0]
        data = msg[1:]
        if mode == Constants.uploadProtocol():
            ServerConnection.startUpload(s, files, data, addr, sPath, v, q)
        elif mode == Constants.downloadProtocol():
            ServerConnection.startDownload(s, files, data, addr, sPath, v, q)
        elif mode == Constants.errorProtocol():
            ServerConnection.processError(s, files, data, addr, v, q)
        elif mode == Constants.endProtocol():
            ServerConnection.processEnd(s, files, data, addr, v, q)
        return

    def startUpload(s, files, message, addr, sPath, verbose, quiet):
        try:
            file = open(sPath+message, "wb")
            files[message] = file
            CommonConnection.sendACK(s, addr[0], addr[1], 'U', message, 0)
        except Exception:
            Logger.logIfNotQuiet(quiet, "Error opening file " + message)
            CommonConnection.sendError(s, addr[0], addr[1])
            return
        return

    def startDownload(s, files, filename, addr, sPath, verbose, quiet):
        try:
            file = open(sPath+filename, "rb")
            files[filename] = file
            data = file.read(Constants.getMaxReadSize())
            host = addr[0]
            port = addr[1]
            CommonConnection.sendMessage(s, host, port, filename, data, 0)
        except Exception:
            Logger.logIfNotQuiet("Error opening file " + filename)
            CommonConnection.sendError(s, addr[0], addr[1])
            return
        return

    def processError(s, files, filename, addr, sPath, verbose, quiet):
        try:
            files[filename].close()
            CommonConnection.sendACK(s, addr[0], addr[1], 'F', filename, 0)
        except Exception:
            return
        return

    def processEnd(s, files, filename, addr, sPath, verbose, quiet):
        try:
            files[filename].close()
            CommonConnection.sendACK(s, addr[0], addr[1], 'E', filename, 0)
        except Exception:
            return
        return
