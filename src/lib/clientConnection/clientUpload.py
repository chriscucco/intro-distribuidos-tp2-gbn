import os
from lib.helpers.fileHelper import FileHelper
from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.logger.logger import Logger
from lib.serverConnection.queueHandler import QueueHandler
import random


class ClientUpload:

    def __sendFile(s, h, p, file, fName, msgQueue, recvMsg,
                   v, quiet, lr):

        bytesSent = 0
        addr = (h, p)
        Logger.logIfNotQuiet(quiet, "Sending file to server...")

        i = Constants.getWin()
        endFile = False
        endRecv = False
        while i > 0:
            prevPos = file.tell()
            data = file.read(Constants.getMaxReadSize())
            if len(data) == 0:
                size = FileHelper.getFileSize(file)
                Logger.logIfVerbose(v, "Sending EOF to client: " + str(addr))
                msg = CommonConnection.sendEndFile(s, h, p, fName, size)
                msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr, size))
                endFile = True
                break
            Logger.logIfVerbose(v, "Sending " + str(bytesSent) +
                                " bytes to server: " + str(h) + ", " + str(p))
            msg = CommonConnection.sendMessage(s, h, p, fName, data, prevPos)
            msgQueue.put(QueueHandler.makeMessageExpected(msg, addr))
            i -= 1
        while not endFile:
            msgRcvd = CommonConnection.receiveMessageFromServer(s, addr)
            r = random.random()
            if r >= lr:
                recvMsg[msgRcvd+'-'+str(h)+'-'+str(p)] = True
                if msgRcvd[0] == Constants.errorProtocol():
                    Logger.log("Server cant process the file transfer")
                    CommonConnection.sendACK(s, h, p, 'F', fName,
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
                        Logger.logIfVerbose(v, "Sending EOF to server: " +
                                            str(addr))
                        m = CommonConnection.sendEndFile(s, h, p, fName, size)
                        msgQueue.put(QueueHandler.makeSimpleExpected(m, addr,
                                                                     size))
                        endFile = True
                else:
                    msg = CommonConnection.sendMessage(s, h, p, fName, data,
                                                       posBeforeRead)
                    msgQueue.put(QueueHandler.makeMessageExpected(msg, addr))
        while not endRecv:
            msgRcvd = CommonConnection.receiveMessageFromServer(s, addr)
            r = random.random()
            if r >= lr:
                recvMsg[msgRcvd+'-'+str(h)+'-'+str(p)] = True
                if msgRcvd[0] == 'A' and msgRcvd[1] == 'E':
                    endRecv = True
        return True

    def upload(self, sckt, h, p, file, fName, msgQueue, recvMsg,
               v, quiet, lr):

        Logger.logIfVerbose(v, "Sending upload code to server:" +
                            str(h) + ", " + str(p))
        message = Constants.uploadProtocol() + fName + ';0'
        addr = (h, p)
        sckt.sendto(message.encode(), addr)
        msgQueue.put(QueueHandler.makeSimpleExpected(message.encode(), addr,
                                                     0))

        message = CommonConnection.receiveMessageFromServer(sckt, addr)
        recvMsg[message+'-'+str(h)+'-'+str(p)] = True

        transferOk = False

        if message[0] == Constants.ackProtocol():
            transferOk = ClientUpload.__sendFile(sckt, h, p, file, fName,
                                                 msgQueue, recvMsg, v,
                                                 quiet, lr)
        elif message[0] == Constants.errorProtocol():
            Logger.log("Server cant process upload work")
            CommonConnection.sendACK(sckt, h, p, 'F', fName, 0)
            file.close()
            return

        if transferOk:
            Logger.log("The transaction ended correctly")
            file.close()

        return
