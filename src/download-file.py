from lib.params.downloadClientParamsValidation import DownloadClientParams
from lib.logger.logger import Logger
from lib.clientConnection.clientDownload import ClientDownload
from lib.serverConnection.queueHandler import QueueHandler
import socket
import queue
from threading import Thread


def main():
    host, port, fName, fDest, v, q, h, lr = DownloadClientParams.validate()
    if h:
        return printHelp()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Logger.logIfVerbose(v, "Download-client socket successfully created")

    msgQ = queue.Queue()
    recvMsg = {}
    queueThread = Thread(target=runQueue, args=(s, msgQ, recvMsg, v))
    queueThread.start()

    clientDownload = ClientDownload()
    clientDownload.download(s, host, port, fName, fDest, msgQ, recvMsg, v, q, lr)
    # Se cierra cliente
    msgQ.put('exit')
    s.close()
    queueThread.join()
    Logger.log("Client closed")
    return


def printHelp():
    print('usage: download-file.py [-h] [-v | -q] [-H ADDR] [-p PORT]')
    print('[-d FILEPATH] [-n FILENAME] [-lr LOSSRATE]')
    print('')
    print('<command description>')
    print('')
    print('optional arguments:')
    print('-h, --help           show this help message and exit')
    print('-v, --verbose        increase output verbosity')
    print('-q, --quiet          decrease output verbosity')
    print('-H, --host           service IP address')
    print('-p, --port           service port')
    print('-d, --dst            destination file path')
    print('-n, --name           file name')
    print('-lr, --loss-rate     loss messages rate')


def runQueue(skt, msgQueue, recvMsg, v):
    QueueHandler.handleQueue(skt, msgQueue, recvMsg, v)
    return


if __name__ == "__main__":
    main()
