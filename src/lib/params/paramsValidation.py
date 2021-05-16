import sys


class Params():
    def initialize():
        return '', '', False, False, False

    def processParams(host, port):
        if host == '':
            host = '127.0.0.1'
        if port == '':
            port = 8080
        return host, port

    def validate():
        host, port, verboseParam, quietParam, helpParam = Params.initialize()
        i = 0
        while i < len(sys.argv):
            if sys.argv[i] == '-h' or sys.argv[i] == '--help':
                helpParam = True
            elif sys.argv[i] == '-v' or sys.argv[i] == '--verbose':
                verboseParam = True
            elif sys.argv[i] == '-q' or sys.argv[i] == '--quiet':
                quietParam = True
            elif sys.argv[i] == '-H' or sys.argv[i] == '--host':
                if len(sys.argv) > i+1:
                    host = sys.argv[i+1]
                    i += 1
            elif sys.argv[i] == '-p' or sys.argv[i] == '--port':
                if len(sys.argv) > i+1:
                    port = int(sys.argv[i+1])
                    i += 1
            i += 1
        host, port = Params.processParams(host, port)
        if verboseParam:
            quietParam = False
        return host, port, verboseParam, quietParam, helpParam
