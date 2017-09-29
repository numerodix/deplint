class InstalledPackage(object):
    '''
    Represents a package that is installed.
    '''

    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __repr__(self):
        return '<%s name=%r, version=%r>' % (
            self.__class__.__name__,
            self.name,
            self.version,
        )

    def __eq__(self, other):
        if not type(other) == self.__class__:
            return False

        return all((
            self.name == other.name,
            self.version == other.version,
        ))

    def __ne__(self, other):
        return not self.__eq__(other)

    def as_display_name(self):
        return '%s-%s' % (self.name, self.version)
