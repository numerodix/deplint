from deplint.model.advice import Advice
from deplint.model.advice_list import AdviceList


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
            pkg_release = pkg_releases.get_more_recent_than_requirement(pkg_req)

            if pkg_release:
                advice = Advice(
                    analyzer=self,
                    severity='info',
                    message="Required dependency '%s' can be upgraded to '%s'" % (
                        pkg_req.as_display_name(),
                        pkg_release.as_display_name_single(),
                    ),
                )
                advice_list.append(advice)

            # Check if the installed version can be updated
            pkg_installed = self.installed_packages.get_by_name(pkg_req.name)
            if pkg_installed:
                pkg_release = pkg_releases.update_installed(pkg_req, pkg_installed)

                if pkg_release:
                    advice = Advice(
                        analyzer=self,
                        severity='info',
                        message="Installed dependency '%s' can be updated to '%s'" % (
                            pkg_installed.as_display_name(),
                            pkg_release.as_display_name_single(),
                        ),
                    )
                    advice_list.append(advice)

        return AdviceList(advice_list=advice_list)
