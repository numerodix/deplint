import sys


class UiWriter(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def inform(self, text):
        '''
        For informational messages.
        '''

        if self.verbose:
            sys.stderr.write(text + '\n')
            sys.stderr.flush()

    def output(self, text):
        '''
        For the core intended output of the program.
        '''

        print(text)
