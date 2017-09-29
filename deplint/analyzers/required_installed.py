from deplint.model.advice import Advice
from deplint.model.advice_list import AdviceList


class RequiredInstalledAnalyzer(object):
    '''
    Reports packages that are required and installed.
    '''

    def __init__(self, requirements_txt, installed_packages):
        self.requirements_txt = requirements_txt
        self.installed_packages = installed_packages

    def analyze(self):
        pkgs_required = self.requirements_txt.packages
        advice_list = []

        for pkg_req in pkgs_required:
            pkg_installed = self.installed_packages.get_by_name(pkg_req.name)

            if pkg_installed and pkg_req.is_satisfied_by(pkg_installed):
                advice = Advice(
                    analyzer=self,
                    severity='debug',
                    message="Required dependency '%s' is satisfied by installed '%s'" % (
                        pkg_req.as_display_name(),
                        pkg_installed.as_display_name(),
                    ),
                )
                advice_list.append(advice)

        return AdviceList(advice_list=advice_list)
