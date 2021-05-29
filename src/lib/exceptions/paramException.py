
class ParamException(BaseException):

    def __init__(self, param):
        self.message = "Invalid parameter: " + param
