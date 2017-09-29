from deplint.model.advice import Advice
from deplint.model.advice_list import AdviceList


class IsTransitiveDepAnalyzer(object):
    '''
    Reports packages that are transitive dependencies (ie. dependencies of
    other packages).
    '''

    # These are known "virtual" dependencies - do not report these as missing
    # from requirements.txt
    VIRTUAL_DEPENDENCIES = frozenset((
        'pkg-resources',
        'setuptools',
    ))

    def __init__(self, requirements_txt, installed_packages, site_packages):
        self.requirements_txt = requirements_txt
        self.installed_packages = installed_packages
        self.site_packages = site_packages

    def analyze(self):
        advice_list = []

        pkgs_installed = self.installed_packages.packages

        for pkg_ins in pkgs_installed:

            pkg_req = self.requirements_txt.get_by_name(pkg_ins.name)
            dependents = self.site_packages.get_package_dependents(pkg_ins.name)

            # The installed dependency is not a transitive dependency
            if not dependents:

                # Check if it's a required dependency
                if not pkg_req and pkg_ins.name not in self.VIRTUAL_DEPENDENCIES:
                    advice = Advice(
                        analyzer=self,
                        severity='warn',
                        message=(
                            "Installed non-transitive dependency '%s' is not required"
                        ) % (
                            pkg_ins.as_display_name(),
                        ),
                    )
                    advice_list.append(advice)

            # The installed dependency is a transitive dependency
            elif dependents:

                # Check if it's a required dependency
                if pkg_req:
                    # TODO: Here we should pick a dependent which is also a
                    # requirement, rather than (possibly) getting an untracked
                    # top level package (which will be reported in the case
                    # above anyway)
                    first_dependent = dependents[0]
                    dependent_req = self.requirements_txt.get_by_name(
                        first_dependent,
                        ignore_case=True,
                    )

                    # This is displayed as:
                    #   requests==2.18.4' is a transitive dependency of 'datadog==0.16.0'
                    # and is a bit misleading, because we know it's the package
                    # by name that is a transitive dependency, not by exact
                    # version...
                    advice = Advice(
                        analyzer=self,
                        severity='info',
                        message=(
                            "Required dependency '%s' is a transitive dependency of '%s'"
                        ) % (
                            pkg_req.as_display_name(),
                            (dependent_req.as_display_name() if dependent_req
                             else first_dependent),
                        ),
                    )
                    advice_list.append(advice)

        return AdviceList(advice_list=advice_list)
