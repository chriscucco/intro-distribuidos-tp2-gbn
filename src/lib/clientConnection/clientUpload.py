import os

from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection


class ClientUpload:

    def upload(self, sckt, host, port, file, fName, verbose, quiet):

        # hacer while hasta que recibe ack, y ahi continuar
        msg = ""

        message = Constants.uploadProtocol() + fName
        sckt.sendto(message.encode(), (host, port))

        data, addr = sckt.recvfrom(Constants.bytesChunk())
        msg = data.decode()
        print("recibio ack" + msg)

        if msg[0] == Constants.errorProtocol():
            CommonConnection.sendACK(sckt, host, port, 'F', fName, 0)
            file.close()
            return

        bytesAlreadySent = 0

        while True:
            file.seek(bytesAlreadySent, os.SEEK_SET)
            message = file.read(Constants.getMaxReadSize())

            if len(message) == 0:
                CommonConnection.sendEndFile(sckt, host, port, fName,
                                             bytesAlreadySent)
                # hacer while hasta q recibe ack
                data, addr = sckt.recvfrom(Constants.bytesChunk())
                msg = data.decode()

                if msg[0] == Constants.ackProtocol():
                    break

            CommonConnection.sendMessage(sckt, host, port, fName, message,
                                         bytesAlreadySent)

            data, addr = sckt.recvfrom(Constants.bytesChunk())
            msg = data.decode()

            if msg[0] == Constants.errorProtocol():
                CommonConnection.sendACK(sckt, host, port, 'F', fName,
                                         bytesAlreadySent)
                file.close()
                return

            if msg[0] == Constants.ackProtocol():
                splittedMsg = msg.split(';')
                bytesAlreadySent = int(splittedMsg[1])

        file.close()

        return
