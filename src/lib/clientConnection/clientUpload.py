import os
from lib.helpers.fileHelper import FileHelper
from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.logger.logger import Logger
from lib.serverConnection.queueHandler import QueueHandler
import random
import time


class ClientUpload:

    def __sendFile(s, host, port, file, fName, msgQueue, recvMsg,
                   verbose, quiet, lr):

        bytesSent = 0
        addr = (host, port)
        Logger.logIfNotQuiet(quiet, "Sending file to server...")

        i = Constants.getWin()
        endFile = False
        endRecv = False
        while i > 0:
            previousPos = file.tell()
            data = file.read(Constants.getMaxReadSize())
            if len(data) == 0:
                size = FileHelper.getFileSize(file)
                Logger.logIfVerbose(verbose, "Sending EndFile to client: " + str(addr))
                msg = CommonConnection.sendEndFile(s, addr[0], addr[1], fName, size)
                msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr, size))
                endFile = True
                break
            Logger.logIfVerbose(verbose, "Sending message to client: " + str(addr))
            msg = CommonConnection.sendMessage(s, addr[0], addr[1], fName, data, previousPos)
            msgQueue.put(QueueHandler.makeMessageExpected(msg, addr))
            i -= 1
        while not endFile:
            msgRcvd = CommonConnection.receiveMessageFromServer(s, addr)
            r = random.random()
            if r >= lr:
                recvMsg[msgRcvd+'-'+str(addr[0])+'-'+str(addr[1])] = True
                if msgRcvd[0] == Constants.errorProtocol():
                    Logger.log("Server cant process the file transfer")
                    Logger.logIfVerbose(verbose, "Sending ACK to server: " +
                                        str(host) + ", " + str(port))
                    CommonConnection.sendACK(s, host, port, 'F', fName,
                                             bytesSent)
                    file.close()
                    return False

                splittedMsg = msgRcvd.split(';')
                bytesSent = int(splittedMsg[1])
                file.seek(bytesSent, os.SEEK_SET)
                mustSendEnd = False
                i = Constants.getWin() - 1
                while i > 0:
                    data = file.read(Constants.getMaxReadSize())
                    if len(data) == 0 and i == (Constants.getWin() - 1):
                        mustSendEnd = True
                        i = 0
                    else:
                        i -= 1
                posBeforeRead = file.tell()
                data = file.read(Constants.getMaxReadSize())
                if len(data) == 0:
                    if mustSendEnd:
                        size = FileHelper.getFileSize(file)
                        Logger.logIfVerbose(verbose, "Sending EOF to server: " + str(addr))
                        msg = CommonConnection.sendEndFile(s, addr[0], addr[1], fName, size)
                        msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr, size))
                        endFile = True
                else:
                    h = addr[0]
                    port = addr[1]
                    Logger.logIfVerbose(verbose, "Sending message to server" + str(addr))
                    msg = CommonConnection.sendMessage(s, h, port, fName, data, posBeforeRead)
                    msgQueue.put(QueueHandler.makeMessageExpected(msg, addr))
        while not endRecv:
            msgRcvd = CommonConnection.receiveMessageFromServer(s, addr)
            r = random.random()
            if r >= lr:
                recvMsg[msgRcvd+'-'+str(addr[0])+'-'+str(addr[1])] = True
                if msgRcvd[0] == Constants.ackProtocol() and msgRcvd[1] == Constants.endProtocol():
                    endRecv = True
        return True

    def upload(self, sckt, host, port, file, fName, msgQueue, recvMsg,
               verbose, quiet, lr):

        Logger.logIfVerbose(verbose, "Sending upload code to server:" +
                            str(host) + ", " + str(port))
        message = Constants.uploadProtocol() + fName + ';0'
        addr = (host, port)
        sckt.sendto(message.encode(), addr)
        msgQueue.put(QueueHandler.makeSimpleExpected(message.encode(), addr, 0))

        message = CommonConnection.receiveMessageFromServer(sckt, addr)
        recvMsg[message+'-'+str(addr[0])+'-'+str(addr[1])] = True

        transferOk = False

        if message[0] == Constants.ackProtocol():
            transferOk = ClientUpload.__sendFile(sckt, host, port, file, fName,
                                                 msgQueue, recvMsg, verbose,
                                                 quiet, lr)
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
