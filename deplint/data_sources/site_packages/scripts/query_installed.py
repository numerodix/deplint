'''
This is a script to be executed in the context of a specific project's
virtualenv in order to query its installed packages in site-packages.
'''


import json
import sys

# Expected failure modes:
# - pkg_resources not available
# - pkg not installed
# - pkg has no top_level

TOP_LEVEL_FILENAME = 'top_level.txt'


def main(package_names):
    results_dict = {
        'errors': [],
        'packages': {},
    }

    try:
        import pkg_resources
    except ImportError:
        results_dict['errors'].append('missing-pkg-resources')
        return results_dict

    for package_name in package_names:
        # NOTE: make sure we lower case the package name, since depedencies in
        # the python world are not case sensitive
        package_name_key = package_name.lower()

        pkg_dict = {
            'errors': [],
            'requires': [],
            'top_levels': [],
            'version': None,
        }

        dist = None
        try:
            dist = pkg_resources.get_distribution(package_name_key)
        except pkg_resources.DistributionNotFound:
            pkg_dict['errors'].append('error-not-installed')

        if dist:
            if dist.has_version():
                pkg_dict['version'] = dist.version

            # detect top_level
            if dist._provider.has_metadata(TOP_LEVEL_FILENAME):
                top_level_bytes = dist._provider.get_metadata(TOP_LEVEL_FILENAME)
                top_levels = top_level_bytes.strip().splitlines()
                pkg_dict['top_levels'] = top_levels

            # detect this package's dependencies
            requires = dist.requires()
            requires_names = []
            for req in requires:
                project_name = req.key
                requires_names.append(project_name)

                # append to our worklist
                if project_name not in package_names:
                    package_names.append(project_name)

            pkg_dict['requires'] = requires_names

        results_dict['packages'][package_name_key] = pkg_dict

    return results_dict


if __name__ == '__main__':
    package_names = sys.argv[1:]
    results_dict = main(package_names)
    block = json.dumps(results_dict, indent=4, sort_keys=True)
    print(block)
