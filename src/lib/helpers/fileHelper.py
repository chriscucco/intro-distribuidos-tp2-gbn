import os


class FileHelper:

    def getFileSize(file):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0, os.SEEK_SET)
        return size
