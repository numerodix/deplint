class PackageRequirement(object):
    def __init__(self, name, operator, version):
        self.name = name
        self.operator = operator
        self.version = version

    def __repr__(self):
        return '<%s name=%r, operator=%r, version=%r>' % (
            self.__class__.__name__,
            self.name,
            self.operator,
            self.version,
        )

    def __eq__(self, other):
        if not type(other) == self.__class__:
            return False

        return all((
            self.name == other.name,
            self.operator == other.operator,
            self.version == other.version,
        ))

    def __ne__(self, other):
        return not self.__eq__(other)
