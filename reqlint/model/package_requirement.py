from packaging.specifiers import SpecifierSet
from packaging.version import Version


class PackageRequirement(object):
    '''
    Represents a dependency declaration like: simplejson==1.2.
    '''

    # shorter operators last to prevent greedy matching from incorrect parsing
    VALID_OPERATORS = ('===', '!=', '~=', '<=', '==', '>=', '<', '>')

    def __init__(self, name, operator, version):
        if operator is not None and operator not in self.VALID_OPERATORS:
            raise ValueError("Invalid operator: %s" % operator)

        self.name = name
        self._operator = operator or None
        self._version = version or None

    def has_operator(self):
        return self._operator is not None

    def has_version(self):
        return self._version is not None

    @property
    def operator(self):
        if not self._operator:
            raise RuntimeError("Cannot access unset operator")

        return self._operator

    @property
    def version(self):
        if not self._version:
            raise RuntimeError("Cannot access unset version")

        return self._version

    def __repr__(self):
        return '<%s name=%r, operator=%r, version=%r>' % (
            self.__class__.__name__,
            self.name,
            self._operator,
            self._version,
        )

    def __eq__(self, other):
        if not type(other) == self.__class__:
            return False

        return all((
            self.name == other.name,
            self._operator == other._operator,
            self._version == other._version,
        ))

    def __ne__(self, other):
        return not self.__eq__(other)

    def as_display_name(self):
        if not self.has_version():
            return self.name

        return '%s%s%s' % (self.name, self.operator, self.version)

    def is_satisfied_by(self, installed_package):
        if not self.name == installed_package.name:
            return False

        # Any version matches
        if not self.has_version():
            return True

        specifier_str = '%s%s' % (self.operator, self.version)
        specifier = SpecifierSet(specifier_str)
        version = Version(installed_package.version)

        return specifier.contains(version)
