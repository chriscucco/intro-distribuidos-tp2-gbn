import socket
import queue
from threading import Thread
from lib.params.uploadClientParamsValidation import UploadClientParams
from lib.logger.logger import Logger
from lib.clientConnection.clientUpload import ClientUpload
from lib.serverConnection.queueHandler import QueueHandler


def main():
    host, port, fName, fSource, v, quiet, h, lr = UploadClientParams.validate()

    if h:
        return printHelp()

    try:
        Logger.logIfVerbose(v, 'Opening file: ' + fName)
        file = open(fSource + fName, "rb")
    except OSError:
        Logger.log("Error opening file " + fSource + fName)
        return

    sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Logger.logIfVerbose(v, "Creating socket...")

    msgQueue = queue.Queue()
    recvMsg = {}
    queueThread = Thread(target=runQueue, args=(sckt, msgQueue, recvMsg, v))
    queueThread.start()

    clientUpload = ClientUpload()

    clientUpload.upload(sckt, host, port, file, fName, msgQueue, recvMsg,
                        v, quiet, lr)

    # Se cierra cliente
    msgQueue.put('exit')
    sckt.close()
    queueThread.join()
    Logger.logIfNotQuiet(quiet, "Client closed")
    return


def printHelp():
    print('usage: upload-file.py [-h] [-v|-q] [-H ADDR] [-p PORT]')
    print('[-s FILEPATH] [-n FILENAME] [-lr LOSSRATE]')
    print('')
    print('<command description>')
    print('')
    print('optional arguments:')
    print('-h, --help           show this help message and exit')
    print('-v, --verbose        increase output verbosity')
    print('-q, --quiet          decrease output verbosity')
    print('-H, --host           server IP address')
    print('-p, --port           server port')
    print('-s, --src            source file path')
    print('-n, --name           file name')
    print('-lr, --loss-rate     loss messages rate')


def runQueue(skt, msgQueue, recvMsg, v):
    QueueHandler.handleQueue(skt, msgQueue, recvMsg, v)
    return


if __name__ == "__main__":
    main()
