from deplint.model.advice import Advice
from deplint.model.advice_list import AdviceList


class IsUnusedAnalyzer(object):
    '''
    Reports packages that are required but not used in the source code.
    '''

    def __init__(self, requirements_txt, installed_packages, site_packages,
                 grep):
        self.requirements_txt = requirements_txt
        self.installed_packages = installed_packages
        self.site_packages = site_packages
        self.grep = grep

    def analyze(self):
        advice_list = []

        pkgs_required = self.requirements_txt.packages

        for pkg_req in pkgs_required:

            # If the package is installed we can discover its top level
            # importable names
            pkg_ins = self.installed_packages.get_by_name(pkg_req.name)
            if pkg_ins:

                # If it have top level names we can see if they are ever
                # imported in the code
                top_levels = self.site_packages.get_package_top_levels(pkg_ins.name)
                if top_levels:

                    # Check every top level name
                    is_imported = False
                    for top_level in top_levels:
                        if self.grep.package_is_imported(top_level):
                            is_imported = True

                    if not is_imported:
                        advice = Advice(
                            analyzer=self,
                            severity='info',
                            message=(
                                "Required dependency '%s' is never imported (%s)"
                            ) % (
                                pkg_req.as_display_name(),
                                ', '.join(top_levels)
                            ),
                        )
                        advice_list.append(advice)

        return AdviceList(advice_list=advice_list)
