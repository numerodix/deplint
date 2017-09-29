from reqlint.analyzers.is_transitive_dep import IsTransitiveDepAnalyzer
from reqlint.data_sources.site_packages.site_packages import SitePackages
from reqlint.model.advice import Advice
from reqlint.model.advice_list import AdviceList
from reqlint.model.available_packages import AvailablePackages
from reqlint.model.installed_packages import InstalledPackages
from reqlint.model.package_installed import InstalledPackage
from reqlint.model.package_releases import PackageReleases
from reqlint.model.package_requirement import PackageRequirement
from reqlint.model.requirements_txt import RequirementsTxt


EXAMPLE_RESULTS_DICT = {
    "errors": [],
    "packages": {
        "certifi": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "certifi"
            ],
            "version": "2017.7.27.1"
        },
        "chardet": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "chardet"
            ],
            "version": "3.0.4"
        },
        "click": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "click"
            ],
            "version": "6.7"
        },
        "flask": {
            "errors": [],
            "requires": [
                "itsdangerous",
                "jinja2",
                "werkzeug",
                "click"
            ],
            "top_levels": [
                "flask"
            ],
            "version": "0.12.2"
        },
        "gevent": {
            "errors": [],
            "requires": [
                "greenlet"
            ],
            "top_levels": [
                "gevent"
            ],
            "version": "1.2.2"
        },
        "greenlet": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "greenlet"
            ],
            "version": "0.4.12"
        },
        "idna": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "idna"
            ],
            "version": "2.6"
        },
        "itsdangerous": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "itsdangerous"
            ],
            "version": "0.24"
        },
        "jinja2": {
            "errors": [],
            "requires": [
                "markupsafe"
            ],
            "top_levels": [
                "jinja2"
            ],
            "version": "2.9.6"
        },
        "locustio": {
            "errors": [],
            "requires": [
                "six",
                "flask",
                "gevent",
                "pyzmq",
                "requests",
                "msgpack-python"
            ],
            "top_levels": [
                "locust"
            ],
            "version": "0.8a2"
        },
        "markupsafe": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "markupsafe"
            ],
            "version": "1.0"
        },
        "msgpack-python": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "msgpack"
            ],
            "version": "0.4.8"
        },
        "pyzmq": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "zmq"
            ],
            "version": "15.2.0"
        },
        "requests": {
            "errors": [],
            "requires": [
                "urllib3",
                "chardet",
                "idna",
                "certifi"
            ],
            "top_levels": [
                "requests"
            ],
            "version": "2.18.4"
        },
        "six": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "six"
            ],
            "version": "1.11.0"
        },
        "urllib3": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "urllib3"
            ],
            "version": "1.22"
        },
        "werkzeug": {
            "errors": [],
            "requires": [],
            "top_levels": [
                "werkzeug"
            ],
            "version": "0.12.2"
        }
    }
}


def test_can_be_upgraded_analyzer():
    pkgs_reqs = RequirementsTxt(
        packages=[
            PackageRequirement(name='locustio', operator='==', version='0.8a2'),  # top level
            PackageRequirement(name='Flask', operator='==', version='0.12.2'),  # one level down
            PackageRequirement(name='Jinja2', operator='==', version='2.9.6'),  # two levels down
        ],
    )

    pkgs_installed = InstalledPackages(
        packages=[
            InstalledPackage(name='Flask', version='0.12.2'),
            InstalledPackage(name='Jinja2', version='2.9.6'),
            InstalledPackage(name='MarkupSafe', version='1.0'),
            InstalledPackage(name='Werkzeug', version='0.12.2'),
            InstalledPackage(name='certifi', version='2017.7.27.1'),
            InstalledPackage(name='chardet', version='3.0.4'),
            InstalledPackage(name='click', version='6.7'),
            InstalledPackage(name='gevent', version='1.2.2'),
            InstalledPackage(name='greenlet', version='0.4.12'),
            InstalledPackage(name='idna', version='2.6'),
            InstalledPackage(name='itsdangerous', version='0.24'),
            InstalledPackage(name='locustio', version='0.8a2'),
            InstalledPackage(name='msgpack-python', version='0.4.8'),
            InstalledPackage(name='pyzmq', version='15.2.0'),
            InstalledPackage(name='requests', version='2.18.4'),
            InstalledPackage(name='six', version='1.11.0'),
            InstalledPackage(name='urllib3', version='1.22'),
        ],
    )

    installed_names = [pkg.name for pkg in pkgs_installed.packages]
    site_packages = SitePackages(
        python_path=None,
        installed_package_names=installed_names,
    )
    site_packages._query_cache = EXAMPLE_RESULTS_DICT

    analyzer = IsTransitiveDepAnalyzer(
        requirements_txt=pkgs_reqs,
        installed_packages=pkgs_installed,
        site_packages=site_packages,
    )
    advice_list = analyzer.analyze()

    expected_advice_list = AdviceList(
        advice_list=[
            Advice(
                analyzer=analyzer,
                severity='info',
                message=(
                    "Required dependency 'Flask==0.12.2' "
                    "is a transitive dependency of 'locustio==0.8a2'"
                ),
            ),
            Advice(
                analyzer=analyzer,
                severity='info',
                message=(
                    "Required dependency 'Jinja2==2.9.6' "
                    "is a transitive dependency of 'locustio==0.8a2'"
                ),
            ),
        ],
    )

    assert expected_advice_list == advice_list
