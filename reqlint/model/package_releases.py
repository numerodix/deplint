class PackageReleases(object):
    '''
    Represents released versions of a package, like: six-1.0, six-1.1.
    '''

    def __init__(self, name, versions):
        self.name = name
        self.versions = set(versions)

    def __repr__(self):
        return '<%s name=%r, versions=%r>' % (
            self.__class__.__name__,
            self.name,
            self.versions,
        )

    def __eq__(self, other):
        if not type(other) == self.__class__:
            return False

        return all((
            self.name == other.name,
            self.versions == other.versions,
        ))

    def __ne__(self, other):
        return not self.__eq__(other)
