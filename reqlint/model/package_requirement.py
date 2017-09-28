class PackageRequirement(object):
    '''
    Represents a dependency declaration like: simplejson==1.2.
    '''

    # shorter operators last to prevent greedy matching from incorrect parsing
    VALID_OPERATORS = ('===', '!=', '~=', '<=', '==', '>=', '<', '>')

    def __init__(self, name, operator, version):
        if operator not in self.VALID_OPERATORS:
            raise ValueError("Invalid operator: %s" % operator)

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

    def as_display_name(self):
        return '%s%s%s' % (self.name, self.operator, self.version)

    def is_satisfied_by(self, installed_package):
        if not self.name == installed_package.name:
            return False

        # XXX
