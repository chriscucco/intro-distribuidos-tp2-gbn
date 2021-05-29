import sys
from lib.params.paramsValidation import Params
from lib.logger.logger import Logger
from lib.exceptions.paramException import ParamException
from lib.constants import Constants

UPLOAD_CLIENT_PARAMS = Constants.noValueCommands() + ['-H', '--host', '-p',
                                                      '--port', '-lr',
                                                      '--loss-rate', '-s',
                                                      '--src', '-n', '--name']


class UploadClientParams(Params):
    def validate():
        host, port, verbose, quiet, helpParam, lossRate = Params.validate()
        fName, fSourcePath = UploadClientParams.getSourcePathAndFilename()
        Logger.logIfVerbose(verbose, "Params parsed")
        return host, port, fName, fSourcePath, verbose, quiet, helpParam, lossRate

    def getSourcePathAndFilename():
        fName = ''
        fSourcePath = ''
        i = 0
        commandWithValue = False

        while i < len(sys.argv):

            if (i > 0 and commandWithValue is False
                    and sys.argv[i] not in UPLOAD_CLIENT_PARAMS):
                raise ParamException(sys.argv[i])

            if sys.argv[i] == '-s' or sys.argv[i] == '--src':
                if len(sys.argv) > i+1:
                    fSourcePath = sys.argv[i+1]
                    i += 1

            if sys.argv[i] == '-n' or sys.argv[i] == '--name':
                if len(sys.argv) > i+1:
                    fName = sys.argv[i+1]
                    i += 1

            if (i > 0 and sys.argv[i][0] == '-'
                    and sys.argv[i] not in Constants.noValueCommands()):
                commandWithValue = True
            else:
                commandWithValue = False

            i += 1
        if fName == '':
            fName = 'test.txt'
        if fSourcePath == '':
            fSourcePath = './'
        if fSourcePath[-1] != '/':
            fSourcePath += '/'
        return fName, fSourcePath
