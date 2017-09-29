class RequirementsTxt(object):
    '''
    Represents the contents of a requirements.txt file.
    '''

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

    def get_by_name(self, package_name, ignore_case=False):
        for pkg in self.packages:
            if ignore_case:
                if pkg.name.lower() == package_name.lower():
                    return pkg

            else:
                if pkg.name == package_name:
                    return pkg
