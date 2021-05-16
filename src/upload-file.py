from lib.params.uploadClientParamsValidation import UploadClientParams
from lib.logger.logger import Logger


def main():
    host, port, fName, fSource, verb, quiet, h = UploadClientParams.validate()

    if h:
        return printHelp()

    Logger.log("Not implemented")
    return


def printHelp():
    print('usage: upload-file.py [-h] [-v|-q] [-H ADDR] [-p PORT]')
    print('[-s FILEPATH] [-n FILENAME]')
    print('')
    print('<command description>')
    print('')
    print('optional arguments:')
    print('-h, --help       show this help message and exit')
    print('-v, --verbose    increase output verbosity')
    print('-q, --quiet      decrease output verbosity')
    print('-H, --host       server IP address')
    print('-p, --port       server port')
    print('-s, --src        source file path')
    print('-n, --name       file name')


if __name__ == "__main__":
    main()
