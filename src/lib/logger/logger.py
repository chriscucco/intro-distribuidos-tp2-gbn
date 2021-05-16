class Logger:
    def logIfVerbose(verbose, message):
        if verbose:
            print(message)

    def logIfNotQuiet(quiet, message):
        if not quiet:
            print(message)

    def log(message):
        print(message)
