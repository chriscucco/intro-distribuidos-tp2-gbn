from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.logger.logger import Logger
from lib.helpers.fileHelper import FileHelper
from lib.serverConnection.queueHandler import QueueHandler
import os


class ServerConnection:
    def startCommunicating(s, files, sPath, msgQueue, recvMsg, v, q):
        try:
            while True:
                data, addr = s.recvfrom(Constants.bytesChunk())
                print('received message')
                msg = data.decode()
                queuedMessage = msg + '-' + addr[0] + '-' + str(addr[1])
                recvMsg[queuedMessage] = True
                ServerConnection.process(s, files, msg, addr, sPath, msgQueue, v, q)
            return
        except Exception:
            return

    def process(s, files, msg, addr, sPath, msgQueue, v, q):
        mode = msg[0]
        data = msg[1:]
        if mode == Constants.uploadProtocol():
            ServerConnection.startUpload(s, files, data, addr, sPath, msgQueue, v, q)
        elif mode == Constants.downloadProtocol():
            ServerConnection.startDownload(s, files, data, addr, sPath, msgQueue, v, q)
        elif mode == Constants.errorProtocol():
            ServerConnection.processError(s, files, data, addr, v, q)
        elif mode == Constants.endProtocol():
            ServerConnection.processEnd(s, files, data, addr, v, q)
        elif mode == Constants.ackProtocol():
            ServerConnection.processAck(s, files, data, addr, msgQueue, v, q)
        elif mode == Constants.fileTransferProtocol():
            ServerConnection.processTransfer(s, files, data, addr, msgQueue, v, q)
        return

    def startUpload(s, files, message, addr, sPath, msgQueue, verbose, quiet):
        try:
            file = open(sPath+message, "wb")
            files[message] = file
            CommonConnection.sendACK(s, addr[0], addr[1], 'U', message, 0)
        except Exception:
            Logger.logIfNotQuiet(quiet, "Error opening file " + message)
            msg = CommonConnection.sendError(s, message, addr[0], addr[1])
            msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr))
            return
        return

    def processTransfer(s, files, data, addr, msgQueue, v, q):
        separatorPossition = data.find(';')
        fname = data[0:separatorPossition]
        processedData = data[separatorPossition+1:]
        separatorPossition = processedData.find(';')
        bytesRecv = int(processedData[0:separatorPossition])
        msg = processedData[separatorPossition+1:]
        try:
            f = files[fname]
            ServerConnection.upload(s, f, fname, bytesRecv, msg, addr, v, q)
        except Exception:
            msg = CommonConnection.sendError(s, fname, addr[0], addr[1])
            msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr))
        return

    def startDownload(s, files, filename, addr, sPath, msgQueue, verbose, quiet):
        try:
            file = open(sPath+filename, "rb")
            files[filename] = file
            data = file.read(Constants.getMaxReadSize())
            host = addr[0]
            port = addr[1]
            msg = CommonConnection.sendMessage(s, host, port, filename, data, 0)
            msgQueue.put(QueueHandler.makeMessageExpected(msg, addr))
        except Exception:
            Logger.logIfNotQuiet("Error opening file " + filename)
            msg = CommonConnection.sendError(s, filename, addr[0], addr[1])
            msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr))
            return
        return

    def processError(s, files, filename, addr, verbose, quiet):
        try:
            files[filename].close()
            CommonConnection.sendACK(s, addr[0], addr[1], 'F', filename, 0)
        except Exception:
            return
        return

    def processEnd(s, files, filename, addr, verbose, quiet):
        try:
            files[filename].close()
            CommonConnection.sendACK(s, addr[0], addr[1], 'E', filename, 0)
        except Exception:
            return
        return

    def processAck(s, files, data, addr, msgQueue, v, q):
        mode = data[0]
        processedData = data[1:]
        if mode == Constants.endProtocol() or mode == Constants.errorProtocol():
            return
        elif mode == Constants.fileTransferProtocol():
            separatorPossition = processedData.find(';')
            fname = processedData[0:separatorPossition]
            bRecv = int(processedData[separatorPossition+1:])
            f = files[fname]
            return ServerConnection.download(s, f, fname, bRecv, addr, msgQueue, v, q)
        return

    def download(s, f, fname, br, addr, msgQueue, v, q):
        f.seek(br, os.SEEK_SET)
        data = f.read(Constants.getMaxReadSize())
        if len(data) == 0:
            msg = CommonConnection.sendEndFile(s, addr[0], addr[1], fname, 0)
            msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr))
        else:
            msg = CommonConnection.sendMessage(s, addr[0], addr[1], fname, data, br)
            msgQueue.put(QueueHandler.makeMessageExpected(msg, addr))
        return

    def upload(s, f, fname, bytesRecv, msg, addr, v, q):
        f.seek(bytesRecv, os.SEEK_SET)
        f.write(msg.encode())
        filesize = FileHelper.getFileSize(f)
        CommonConnection.sendACK(s, addr[0], addr[1], 'T', fname, filesize)
        return
