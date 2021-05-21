from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.helpers.fileHelper import FileHelper


class ClientUpload:

    def upload(self, sckt, host, port, file, fName, verbose, quiet):

        msg = ""

        message = Constants.uploadProtocol() + fName
        sckt.sendto(message.encode(), (host, port))

        data, addr = sckt.recvfrom(Constants.bytesChunk())
        msg = data.decode()

        if msg[0] == Constants.ackProtocol():
            file.close()
            return

        bytesAlreadySent = 0
        fileSize = FileHelper.getFileSize(file)

        while bytesAlreadySent < fileSize:

            message = file.read(Constants.getMaxReadSize())
            CommonConnection.sendMessage(sckt, host, port, fName, message,
                                         bytesAlreadySent)

            data, addr = sckt.recvfrom(Constants.bytesChunk())
            msg = data.decode()

            if msg[0] == Constants.ackProtocol():
                splittedMsg = msg.split(';')
                bytesAlreadySent += int(splittedMsg[1])

            '''Logger.logIfVerbose(verbose, "Sending upload code to server")
        sckt.send(Constants.uploadProtocol().encode())
        data = sckt.recv(Constants.bytesChunk())
        confirmation = data.decode()

        if (confirmation != Constants.okProtocol()):
            Logger.log("Server cant process upload work")
            return

        Logger.logIfVerbose(verbose, "Sending name of file to server")
        sckt.send(fName.encode())
        data = sckt.recv(Constants.bytesChunk())

        confirmation = data.decode()

        validation = self.__validateConfirmation(file, confirmation,
                                                 "Server cant work with file: "
                                                 + fName)

        if (validation is False):
            return

        Logger.logIfVerbose(verbose, "Sending size of file")
        FileTransfer.sendFileSize(sckt, file, verbose, quiet)
        data = sckt.recv(Constants.bytesChunk())
        confirmation = data.decode()

        validation = self.__validateConfirmation(file, confirmation,
                                                 "Server cant process file" +
                                                 " size")

        if (validation is False):
            return

        Logger.logIfNotQuiet(quiet, "Sending file to server...")
        FileTransfer.sendFile(sckt, file, Constants.bytesChunk())

        data = sckt.recv(Constants.bytesChunk())
        confirmation = data.decode()

        if (confirmation != Constants.okProtocol()):
            Logger.log("Server cant save file.")'''

        file.close()

        return
