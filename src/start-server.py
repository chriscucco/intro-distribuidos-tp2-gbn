from lib.params.serverParamsValidation import ServerParams
from lib.logger.logger import Logger


def main():
    host, port, sPath, verbose, quiet, helpParam = ServerParams.validate()

    if helpParam:
        return printHelp()
    
    

    Logger.log("Not implemented")
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
