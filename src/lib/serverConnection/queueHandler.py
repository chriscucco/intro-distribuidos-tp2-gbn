import datetime
import time
from lib.logger.logger import Logger
from lib.constants import Constants


class QueueHandler:
    def handleQueue(srvSock, msgQueue, recvMsg, v):
        Logger.logIfVerbose(v, "Handler queue initialized")
        while True:
            item = msgQueue.get()
            if item == 'exit':
                break
            now = datetime.datetime.now()
            sleepTime = (item["ttl"] - now).total_seconds()
            if sleepTime > 0:
                time.sleep(sleepTime)
            expectedMsg = item['expected']
            messageRecv = recvMsg.get(expectedMsg, False)

            if not messageRecv:
                QueueHandler.retry(srvSock, item, msgQueue, v)
            msgQueue.task_done()
        return

    def makeSimpleExpected(currentMsg, addr, size):
        decodedMsg = currentMsg.decode()
        expected = 'A' + decodedMsg + '-' + addr[0] + '-' + str(addr[1])
        secs = Constants.ttl()
        ttl = datetime.datetime.now() + datetime.timedelta(seconds=secs)
        d = dict()
        d['expected'] = expected
        d['ttl'] = ttl
        d['msg'] = currentMsg
        d['addr'] = addr
        d['retrySize'] = 10
        return d

    def makeMessageExpected(currentMsg, addr):
        prefix = currentMsg[0:44].decode()
        fileData = currentMsg[44:]
        separatorPossition = prefix.find(';')
        fname = prefix[0:separatorPossition]
        processedData = prefix[separatorPossition+1:]
        separatorPossition = processedData.find(';')
        bytesRecv = int(processedData[0:separatorPossition])

        totalLenght = bytesRecv + len(fileData)
        processedMsg = fname + ';' + str(totalLenght)
        expected = 'A' + processedMsg + '-' + addr[0] + '-' + str(addr[1])
        ttl = datetime.datetime.now() + datetime.timedelta(
            seconds=Constants.ttl())
        d = dict()
        d['expected'] = expected
        d['ttl'] = ttl
        d['msg'] = currentMsg
        d['addr'] = addr
        d['retrySize'] = 20
        return d

    def retry(srvSock, item, msgQueue, v):
        addr = item['addr']
        message = item['msg']
        Logger.logIfVerbose(v, "Retrying package to: " + str(addr) +
                            ", remaining " + str(item['retrySize']) +
                            ' retries')
        try:

            srvSock.sendto(message, addr)
            item['ttl'] = datetime.datetime.now() + datetime.timedelta(
                seconds=Constants.ttl())
            if item['retrySize'] > 0:
                msgQueue.put(item)
                item['retrySize'] -= 1
            return
        except Exception:
            return
