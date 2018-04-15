class A0(object):
    def __init__(self, *args, **kwargs):
        super(A0, self).__init__()
        self.args = args
        self.kwargs = kwargs

class A(A0):
    def __init__(self, myarg, *args, **kwargs):
        super(A, self).__init__(*args, **kwargs)
        self.myarg = myarg
