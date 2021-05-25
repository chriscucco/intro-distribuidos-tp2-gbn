import os

from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.logger.logger import Logger
from lib.serverConnection.queueHandler import QueueHandler


class ClientUpload:

    def __sendFile(sckt, host, port, file, fName, msgQueue, recvMsg,
                   verbose, quiet):

        bytesAlreadySent = 0
        addr = (host, port)
        Logger.logIfNotQuiet(quiet, "Sending file to server...")

        while True:
            file.seek(bytesAlreadySent, os.SEEK_SET)
            data = file.read(Constants.getMaxReadSize())

            if len(data) == 0:
                Logger.logIfVerbose(verbose, "Sending End of file to server: "
                                    + str(host) + ", " + str(port))
                message = CommonConnection.sendEndFile(sckt, host, port, fName,
                                                       bytesAlreadySent)
                msgQueue.put(QueueHandler.makeSimpleExpected(message, addr))

                msgRcvd = CommonConnection.receiveMessageFromServer(sckt, addr,
                                                                    recvMsg)

                if msgRcvd[0] == Constants.ackProtocol():
                    break

            message = CommonConnection.sendMessage(sckt, host, port,
                                                   fName, data,
                                                   bytesAlreadySent)
            msgQueue.put(QueueHandler.makeMessageExpected(message, addr))

            msgRcvd = CommonConnection.receiveMessageFromServer(sckt, addr,
                                                                recvMsg)

            if msgRcvd[0] == Constants.errorProtocol():
                Logger.log("Server cant process the file transfer")
                Logger.logIfVerbose(verbose, "Sending ACK to server: " +
                                    str(host) + ", " + str(port))
                CommonConnection.sendACK(sckt, host, port, 'F', fName,
                                         bytesAlreadySent)
                file.close()
                return False

            if msgRcvd[0] == Constants.ackProtocol():
                splittedMsg = msgRcvd.split(';')
                bytesAlreadySent = int(splittedMsg[1])

        return True

    def upload(self, sckt, host, port, file, fName, msgQueue, recvMsg,
               verbose, quiet):

        Logger.logIfVerbose(verbose, "Sending upload code to server:" +
                            str(host) + ", " + str(port))
        message = Constants.uploadProtocol() + fName
        addr = (host, port)
        sckt.sendto(message.encode(), addr)
        msgQueue.put(QueueHandler.makeSimpleExpected(message, addr))

        message = CommonConnection.receiveMessageFromServer(sckt, addr,
                                                            recvMsg)

        transferOk = False

        if message[0] == Constants.ackProtocol():
            transferOk = ClientUpload.__sendFile(sckt, host, port, file, fName,
                                                 msgQueue, recvMsg, verbose,
                                                 quiet)
        elif message[0] == Constants.errorProtocol():
            Logger.log("Server cant process upload work")
            Logger.logIfVerbose(verbose, "Sending ACK to server: " +
                                str(host) + ", " + str(port))
            CommonConnection.sendACK(sckt, host, port, 'F', fName, 0)
            file.close()
            return

        if transferOk:
            Logger.log("The transaction ended correctly")
            file.close()

        return
