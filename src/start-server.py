from lib.params.serverParamsValidation import ServerParams
from lib.serverConnection.serverConnection import ServerConnection
from lib.serverConnection.queueHandler import QueueHandler
from lib.logger.logger import Logger
from threading import Thread
import socket
import queue


def main():
    host, port, sPath, verbose, quiet, helpParam = ServerParams.validate()

    if helpParam:
        return printHelp()

    Logger.log("Server started in host: " + host + " and port: " + str(port))

    srvSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Logger.logIfNotQuiet(quiet, "Server socket successfully created")

    try:
        srvSock.bind((host, port))
        Logger.logIfVerbose(verbose, "Server socket binded")
    except socket.error:
        Logger.log("Error binding socket")
        return

    files = {}

    msgQueue = queue.Queue()
    recvMsg = {}
    queueThread = Thread(target=runQueue, args=(srvSock, msgQueue, recvMsg, verbose))
    t = Thread(target=start, args=(srvSock, files, sPath, msgQueue, recvMsg, verbose, quiet))
    t.start()
    queueThread.start()
    serverOn = True
    while serverOn:
        value = input()
        if value == 'exit':
            serverOn = False

    enabled = False
    msgQueue.put('exit')
    srvSock.close()
    t.join()
    queueThread.join()
    for key, f in files.items():
        try:
            f.close
            Logger.logIfVerbose(verbose, "File " + key + " closed")
        except Exception:
            Logger.logIfVerbose(verbose, "Error closing file: " + key)
    Logger.log('Server closed')
    return


def start(socket, files, sPath, msgQueue, recvMsg, verbose, quiet):
    ServerConnection.startCommunicating(socket, files, sPath, msgQueue, recvMsg, verbose, quiet)
    return

def runQueue(srvSock, msgQueue, recvMsg, v):
    QueueHandler.handleQueue(srvSock, msgQueue, recvMsg, v)
    return


def printHelp():
    print('usage: start-server.py [-h] [-v|-q] [-H ADDR] [-p PORT]')
    print(' [-s DIRPATH]')
    print('')
    print('<command description>')
    print('')
    print('optional arguments:')
    print('-h, --help       show this help message and exit')
    print('-v, --verbose    increase output verbosity')
    print('-q, --quiet      decrease output verbosity')
    print('-H, --host       service IP address')
    print('-p, --port       service port')
    print('-s, --storage    storage dir path')


if __name__ == "__main__":
    main()
