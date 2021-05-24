import os
from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.helpers.fileHelper import FileHelper
from lib.logger.logger import Logger


class ClientDownload:
    def download(self, downSock, host, port, fName, fDest, verb, quiet):
        message = Constants.downloadProtocol() + fName
        Logger.logIfVerbose(verb, "Sending download request to server")
        downSock.sendto(message.encode(), (host, port))

        data, addr = downSock.recvfrom(Constants.bytesChunk())
        dataDecode = data.decode()
        mode = dataDecode[0]
        file = self.processInitialMsg(downSock, fName, fDest, mode, dataDecode, addr, verb, quiet)
        if file is None:
            return

        while True:
            if mode == Constants.fileTransferProtocol():
                separatorIndex = dataDecode.find(';')
                fname = dataDecode[1:separatorIndex]
                processedData = dataDecode[separatorIndex+1:]
                separatorIndex = processedData.find(';')
                bRecv = int(processedData[:separatorIndex])
                msg = processedData[separatorIndex+1:]
                Logger.logIfVerbose(verb, "Recieved " + str(bRecv) + " bytes from server: " + str(addr))
                file.seek(bRecv, os.SEEK_SET)
                file.write(msg.encode())
                fileSize = FileHelper.getFileSize(file)
                Logger.logIfVerbose(verb, "Sending ACK-T to server: " + str(addr))
                CommonConnection.sendACK(downSock, host, port, 'T', fname, fileSize)
            elif mode == Constants.endProtocol():
                Logger.logIfVerbose(verb, "Sending ACK-E to server: " + str(addr))
                CommonConnection.sendACK(downSock, host, port, 'E', fname, 0)
                Logger.log("File downloaded successfully in: " + fDest + fname)
                file.close()
                return
            data, addr = downSock.recvfrom(Constants.bytesChunk())
            dataDecode = data.decode()
            mode = dataDecode[0]
        return

    def processInitialMsg(self, downSock, fName, fDest, mode, data, addr, verb, quiet):
        if mode == Constants.errorProtocol():
            Logger.log("The file does not exist on the server")
            Logger.logIfVerbose(verb, "Sending ACK-F to server: " + addr)
            CommonConnection.sendACK(downSock, addr[0], addr[1], 'F', fName, 0)
            return None
        elif mode == Constants.fileTransferProtocol():
            try:
                file = open(fDest + fName, "wb")
                Logger.logIfVerbose(verb, "File created on client")
                return file
            except OSError:
                Logger.log("Client could not create the file on: " + fDest + fName)
                return None