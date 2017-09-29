import operator

from packaging.version import Version


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
            sorted(self.versions),
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

    def as_display_name_single(self):
        if len(self.versions) != 1:
            raise ValueError("Cannot display - need single version")

        return '%s-%s' % (self.name, list(self.versions)[0])

    def get_more_recent_than_requirement(self, package_requirement):
        '''
        Returns a clone of `self` that only includes one version more recent
        than the version of `package_requirement`. If no such versions exists
        it returns None.
        '''

        released_versions = [Version(ver) for ver in self.versions]
        released_versions.sort()

        # If the requirement has no version do not filter at all
        if not package_requirement.has_version():
            return

        # Otherwise filter on versions more recent than requirement
        requirement_version = Version(package_requirement.version)
        newer_versions = [ver for ver in released_versions
                          if ver > requirement_version]

        if newer_versions:
            newest_version = newer_versions[-1].base_version
            return self.__class__(
                name=self.name,
                versions=(newest_version,),
            )

    def update_installed(self, package_requirement, package_installed):
        '''
        Attempts to update `package_installed` such that it respects any
        restrictions specified in `package_requirement`. (Only relevant if
        `package_requirement` uses < or <= in its specifier.)

        If a newer version can be found it returns a clone of `self` that only
        includes one version more recent than the version of
        `package_installed`. If no such versions exists it returns None.
        '''

        released_versions = [Version(ver) for ver in self.versions]
        released_versions.sort()

        installed_version = Version(package_installed.version)

        # If the requirement has no version do not filter using requirement
        if not package_requirement.has_version():
            newer_versions = [ver for ver in released_versions
                              if ver > installed_version]

        # Otherwise apply upper bound filter using requirement version
        else:
            newer_versions = []
            requirement_version = Version(package_requirement.version)

            op = None
            if package_requirement.operator == '<':
                op = operator.lt
            elif package_requirement.operator == '<=':
                op = operator.le

            if op:
                newer_versions = [ver for ver in released_versions
                                  if ver > installed_version and
                                  op(ver, requirement_version)]

        if newer_versions:
            newest_version = newer_versions[-1].base_version
            return self.__class__(
                name=self.name,
                versions=(newest_version,),
            )
