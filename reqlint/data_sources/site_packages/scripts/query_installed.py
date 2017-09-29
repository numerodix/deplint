'''
This is a script to be executed in the context of a specific project's
virtualenv in order to query its installed packages in site-packages.
'''


import json
import sys

# TODO handle failure modes:
# - pkg_resources not available
# - pkg not installed
# - pkg has no top_level

TOP_LEVEL_FILENAME = 'top_level.txt'


def main(package_names):
    import pkg_resources

    results_dict = {}

    for package_name in package_names:
        pkg_dict = {}

        dist = pkg_resources.get_distribution(package_name)

        # detect top_level
        top_levels = []
        if dist._provider.has_metadata(TOP_LEVEL_FILENAME):
            top_level_bytes = dist._provider.get_metadata(TOP_LEVEL_FILENAME)
            top_levels = top_level_bytes.strip().splitlines()

        pkg_dict['top_levels'] = top_levels

        # detect this package's dependencies
        requires = dist.requires()
        requires_names = []
        for req in requires:
            project_name = req.project_name
            requires_names.append(project_name)

            # append to our worklist
            if project_name not in package_names:
                package_names.append(project_name)

        pkg_dict['requires'] = requires_names

        results_dict[package_name] = pkg_dict

    return results_dict


if __name__ == '__main__':
    package_names = sys.argv[1:]
    results_dict = main(package_names)
    block = json.dumps(results_dict, indent=4, sort_keys=True)
    print(block)
