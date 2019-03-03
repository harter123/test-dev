class MyException(Exception):
    def __init__(self, message='参数错误'):
        self.message = message

    def __str__(self):
        return self.message
