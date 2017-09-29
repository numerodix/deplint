class AdviceList(object):
    '''
    Represents a list of Advice objects.
    '''

    def __init__(self, advice_list):
        self.advice_list = advice_list

    def __repr__(self):
        return '<%s num_advice=%s>' % (
            self.__class__.__name__,
            len(self.advice_list),
        )

    def __eq__(self, other):
        if not type(other) == self.__class__:
            return False

        return all((
            self.advice_list == other.advice_list,
        ))

    def __ne__(self, other):
        return not self.__eq__(other)

    def has_problems(self):
        # XXX this is a bit over specific
        for advice in self.advice_list:
            if advice.severity in ('warn', 'error'):
                return True

        return False
