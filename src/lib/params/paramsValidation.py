import sys
from lib.exceptions.paramException import ParamException
from lib.constants import Constants


class Params():
    def initialize():
        return '', '', False, False, False, 0.0

    def processParams(host, port):
        if host == '':
            host = '127.0.0.1'
        if port == '':
            port = 8090
        return host, port

    def validate():
        host, port, verbose, quietParam, helpParam, lr = Params.initialize()
        i = 0
        while i < len(sys.argv):
            if sys.argv[i] == '-h' or sys.argv[i] == '--help':
                helpParam = True
            elif sys.argv[i] == '-v' or sys.argv[i] == '--verbose':
                verbose = True
                if quietParam:
                    quietParam = False
            elif sys.argv[i] == '-q' or sys.argv[i] == '--quiet':
                if not verbose:
                    quietParam = True
            elif sys.argv[i] == '-H' or sys.argv[i] == '--host':
                if len(sys.argv) > i+1:
                    host = sys.argv[i+1]
                    i += 1
            elif sys.argv[i] == '-p' or sys.argv[i] == '--port':
                if len(sys.argv) > i+1:
                    port = int(sys.argv[i+1])
                    i += 1
            elif sys.argv[i] == '-lr' or sys.argv[i] == '--loss-rate':
                try:
                    lr = float(sys.argv[i+1])
                    if lr >= 1.0 or lr < 0:
                        raise ParamException(sys.argv[i]
                                             + ' ' + sys.argv[i+1])
                except Exception:
                    raise ParamException(sys.argv[i]
                                         + ' ' + sys.argv[i+1])
                i += 1
            i += 1
        host, port = Params.processParams(host, port)
        if verbose:
            quietParam = False
        return host, port, verbose, quietParam, helpParam, lr

    def validateCommand(commandsList, previousArgIsCommand, argPos):
        if (argPos > 0 and previousArgIsCommand is False
                and sys.argv[argPos] not in commandsList):
            raise ParamException(sys.argv[argPos])

    def commandHasValue(argPos):
        return (argPos > 0 and sys.argv[argPos][0] == '-' and
                sys.argv[argPos] not in Constants.noValueCommands())
