from reqlint.model.advice import Advice
from reqlint.model.advice_list import AdviceList


class IsTransitiveDepAnalyzer(object):
    '''
    Reports packages that are transitive dependencies (ie. dependencies of
    other packages).
    '''

    def __init__(self, requirements_txt, installed_packages, site_packages):
        self.requirements_txt = requirements_txt
        self.installed_packages = installed_packages
        self.site_packages = site_packages

    def analyze(self):
        advice_list = []

        # Of the required packages, find all the installed ones (we can only do
        # transitive dependency checking on installed packages)
        pkgs_pairs = [(pkg_req, self.installed_packages.get_by_name(pkg_req.name))
                      for pkg_req in self.requirements_txt.packages]
        pkgs_pairs = [(pkg_req, pkg_ins) for (pkg_req, pkg_ins) in pkgs_pairs
                      if pkg_ins]

        for pkg_req, pkg_ins in pkgs_pairs:

            dependents = self.site_packages.get_package_dependents(pkg_ins.name)
            if dependents:
                advice = Advice(
                    analyzer=self,
                    severity='info',
                    message=(
                        "Required dependency '%s' is a transitive dependency of '%s'"
                    ) % (
                        pkg_req.as_display_name(),
                        # TODO: trace this back to an item in self.requirements_txt
                        dependents[0],
                    ),
                )
                advice_list.append(advice)

        return AdviceList(advice_list=advice_list)
