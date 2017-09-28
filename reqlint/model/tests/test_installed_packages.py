from reqlint.model.package_installed import InstalledPackage
from reqlint.model.installed_packages import InstalledPackages


def test_requirements_txt_equality():
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
