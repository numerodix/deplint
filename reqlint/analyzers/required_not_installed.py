from reqlint.model.advice import Advice


class RequiredNotInstalledAnalyzer(object):
    '''
    Reports packages that are required but not installed.
    '''

    def __init__(self, requirements_txt, installed_packages):
        self.requirements_txt = requirements_txt
        self.installed_packages = installed_packages

    def analyze(self):
        pkgs_required = self.requirements_txt.packages
        advice_list = []

        for pkg_req in pkgs_required:
            pkg_installed = self.installed_packages.get_by_name(pkg_req.name)
            if not pkg_installed:
                advice = Advice(
                    analyzer=self,
                    severity='error',
                    message="Dependency '%s' is not installed" % pkg_req.as_display_name(),
                )
                advice_list.append(advice)

        return advice_list
