class RequirementsTxt(object):
    def __init__(self, packages):
        self.packages = packages

    def __repr__(self):
        return '<%s num_packages=%s>' % (
            self.__class__.__name__,
            len(self.packages),
        )

    def __eq__(self, other):
        if not type(other) == self.__class__:
            return False

        return all((
            self.packages == other.packages,
        ))

    def __ne__(self, other):
        return not self.__eq__(other)
