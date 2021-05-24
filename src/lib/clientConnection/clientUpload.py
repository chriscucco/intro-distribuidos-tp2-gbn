import os

from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.logger.logger import Logger


class ClientUpload:

    def __sendFile(sckt, host, port, file, fName, verbose, quiet):

        bytesAlreadySent = 0
        Logger.logIfNotQuiet(quiet, "Sending file to server...")

        while True:
            file.seek(bytesAlreadySent, os.SEEK_SET)
            message = file.read(Constants.getMaxReadSize())

            if len(message) == 0:
                Logger.logIfVerbose(verbose, "Sending End of file to server: "
                                    + str(host) + ", " + str(port))
                CommonConnection.sendEndFile(sckt, host, port, fName,
                                             bytesAlreadySent)

                data, addr = sckt.recvfrom(Constants.bytesChunk())
                msg = data.decode()

                if msg[0] == Constants.ackProtocol():
                    break

            CommonConnection.sendMessage(sckt, host, port, fName, message,
                                         bytesAlreadySent)

            data, addr = sckt.recvfrom(Constants.bytesChunk())
            msg = data.decode()

            if msg[0] == Constants.errorProtocol():
                Logger.log("Server cant process the file transfer")
                Logger.logIfVerbose(verbose, "Sending ACK to server: " +
                                    str(host) + ", " + str(port))
                CommonConnection.sendACK(sckt, host, port, 'F', fName,
                                         bytesAlreadySent)
                file.close()
                return False

            if msg[0] == Constants.ackProtocol():
                splittedMsg = msg.split(';')
                bytesAlreadySent = int(splittedMsg[1])

        return True

    def upload(self, sckt, host, port, file, fName, verbose, quiet):

        Logger.logIfVerbose(verbose, "Sending upload code to server:" +
                            str(host) + ", " + str(port))
        message = Constants.uploadProtocol() + fName
        sckt.sendto(message.encode(), (host, port))

        data, addr = sckt.recvfrom(Constants.bytesChunk())
        msg = data.decode()

        transferOk = False

        if msg[0] == Constants.ackProtocol():
            transferOk = ClientUpload.__sendFile(sckt, host, port, file, fName,
                                                 verbose, quiet)
        elif msg[0] == Constants.errorProtocol():
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
