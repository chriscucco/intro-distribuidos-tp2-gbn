import sys
from lib.params.paramsValidation import Params
from lib.logger.logger import Logger


class DownloadClientParams(Params):
    def validate():
        host, port, verbose, quiet, helpParam = Params.validate()
        fName, fDest = DownloadClientParams.getDestinationPathAndFilename()
        Logger.logIfVerbose(verbose, "Params parsed")
        return host, port, fName, fDest, verbose, quiet, helpParam

    def getDestinationPathAndFilename():
        fName = ''
        fDest = ''
        i = 0
        while i < len(sys.argv):
            if sys.argv[i] == '-d' or sys.argv[i] == '--dst':
                if len(sys.argv) > i+1:
                    fDest = sys.argv[i+1]
                    i += 1
            if sys.argv[i] == '-n' or sys.argv[i] == '--name':
                if len(sys.argv) > i+1:
                    fName = sys.argv[i+1]
                    i += 1
            i += 1
        if fName == '':
            fName = 'test.txt'
        if fDest == '':
            fDest = './'
        return fName, fDest
