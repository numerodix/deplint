from reqlint.model.advice import Advice
from reqlint.model.advice_list import AdviceList


class CanBeUpgradedAnalyzer(object):
    '''
    Reports packages that can be upgraded to a newer version available in the
    package index.
    '''

    def __init__(self, requirements_txt, installed_packages, available_packages):
        self.requirements_txt = requirements_txt
        self.installed_packages = installed_packages
        self.available_packages = available_packages

    def analyze(self):
        pkgs_required = self.requirements_txt.packages
        advice_list = []

        for pkg_req in pkgs_required:
            # Check if the requirement can be upgraded
            pkg_releases = self.available_packages.get_by_name(pkg_req.name)
            pkg_releases = pkg_releases.get_more_recent_than_requirement(pkg_req)

            if pkg_releases:
                advice = Advice(
                    analyzer=self,
                    severity='info',
                    message="Dependency '%s' can be upgraded to '%s'" % (
                        pkg_req.as_display_name(),
                        pkg_releases.as_display_name_single(),
                    ),
                )
                advice_list.append(advice)

        return AdviceList(advice_list=advice_list)
