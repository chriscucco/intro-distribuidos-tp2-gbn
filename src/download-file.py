from lib.params.downloadClientParamsValidation import DownloadClientParams
from lib.logger.logger import Logger
from lib.clientConnection.clientDownload import ClientDownload
from lib.serverConnection.queueHandler import QueueHandler
import socket
import queue
from threading import Thread


def main():
    host, port, fName, fDest, verb, quiet, h = DownloadClientParams.validate()
    if h:
        return printHelp()

    downSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Logger.logIfVerbose(verb, "Download-client socket successfully created")

    msgQueue = queue.Queue()
    recvMsg = {}
    queueThread = Thread(target=runQueue, args=(downSock, msgQueue, recvMsg, verb))
    queueThread.start()

    clientDownload = ClientDownload()
    clientDownload.download(downSock, host, port, fName, fDest, msgQueue, recvMsg, verb, quiet)
 
    # Se cierra cliente
    msgQueue.put('exit')
    downSock.close()
    queueThread.join()
    Logger.log("Client closed")
    return


def printHelp():
    print('usage: download-file.py [-h] [-v | -q] [-H ADDR] [-p PORT]')
    print('[-d FILEPATH] [-n FILENAME]')
    print('')
    print('<command description>')
    print('')
    print('optional arguments:')
    print('-h, --help       show this help message and exit')
    print('-v, --verbose    increase output verbosity')
    print('-q, --quiet      decrease output verbosity')
    print('-H, --host       service IP address')
    print('-p, --port       service port')
    print('-d, --dst        destination file path')
    print('-n, --name       file name')


def runQueue(skt, msgQueue, recvMsg, v):
    QueueHandler.handleQueue(skt, msgQueue, recvMsg, v)
    return


if __name__ == "__main__":
    main()
