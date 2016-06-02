class PE(Exception):
    '''
      Custom exception class to raise exceptions in the
      parameters generators for the synthetic CMD module
    '''

    def __init__(self, msg, val):
        self.msg = msg
        self.val = val
