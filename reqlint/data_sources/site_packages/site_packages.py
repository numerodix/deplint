import json
import os
import subprocess


class SitePackages(object):
    def __init__(self, python_path, installed_package_names):
        self.python_path = python_path
        self.installed_package_names = [name.lower() for name in installed_package_names]

        self._query_cache = None

    def get_query_script_path(self):
        mydir = os.path.dirname(__file__)
        script_dir = os.path.join(mydir, 'scripts')
        script_filepath = os.path.join(script_dir, 'query_installed.py')
        return script_filepath

    def uncached_query_installed_packages(self, package_names):
        script_filepath = self.get_query_script_path()

        args = [
            self.python_path,
            script_filepath,
        ] + package_names

        output_bytes = subprocess.check_output(args)
        output = output_bytes.decode('utf-8')
        results_dict = json.loads(output)
        return results_dict

    def query_installed_packages(self):
        results_dict = self._query_cache

        if not results_dict:
            results_dict = self.uncached_query_installed_packages(
                package_names=self.installed_package_names,
            )
            self._query_cache = results_dict

        return results_dict

    # Higher level interface

    def get_package_top_levels(self, package_name):
        package_name = package_name.lower()
        results_dict = self.query_installed_packages()

        pkg_dict = results_dict['packages'][package_name]
        top_levels = pkg_dict['top_levels']
        return top_levels

    def get_package_dependents(self, package_name):
        package_name = package_name.lower()
        results_dict = self.query_installed_packages()

        # use a worklist since we are traversing the dep graph from leaf
        # towards root
        worklist = [package_name]
        dependents = []

        for package_name in worklist:

            for name, pkg_dict in results_dict['packages'].items():
                if package_name in pkg_dict['requires']:
                    # `package_name` is required by (a dependency of) `name`,
                    # therefore `name` is a dependent.
                    dependents.append(name)
                    # We also need to add `name` to the worklist since it could
                    # be an intermediate node and not a root dependency.
                    worklist.append(name)

                    # If `package_name` was previously discovered to be a
                    # dependent and now turns out to be a dependency of
                    # something else then it turns out to be an intermediate
                    # node - not a top level package - so remove it from the
                    # dependents.
                    if package_name in dependents:
                        dependents.remove(package_name)

        return dependents
