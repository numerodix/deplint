from reqlint.model.package_installed import InstalledPackage
from reqlint.model.installed_packages import InstalledPackages


def test_installed_packages_equality():
    reqs1 = InstalledPackages(
        packages=[
            InstalledPackage(name='coverage', version='3.6'),
            InstalledPackage(name='parsimonious', version='0.5'),
        ],
    )

    # missing one package
    reqs2 = InstalledPackages(
        packages=[
            InstalledPackage(name='coverage', version='3.6'),
        ],
    )

    # name differs
    reqs3 = InstalledPackages(
        packages=[
            InstalledPackage(name='discovery', version='3.6'),
            InstalledPackage(name='parsimonious', version='0.5'),
        ],
    )

    assert reqs1 == reqs1
    assert not reqs1 != reqs1

    assert reqs1 != reqs2
    assert not reqs1 == reqs2

    assert reqs1 != reqs3
    assert not reqs1 == reqs3


def test_installed_packages_get_by_name():
    coverage = InstalledPackage(name='coverage', version='3.6')
    parsimonious = InstalledPackage(name='parsimonious', version='0.5')

    reqs = InstalledPackages(
        packages=[
            coverage,
            parsimonious,
        ],
    )

    # exact name matches
    assert reqs.get_by_name('coverage') is coverage
    assert reqs.get_by_name('parsimonious') is parsimonious

    # nothing else matches
    assert reqs.get_by_name('coverage==1.0') is None
    assert reqs.get_by_name('cov') is None
