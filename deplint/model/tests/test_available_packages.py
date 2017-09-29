from deplint.model.available_packages import AvailablePackages
from deplint.model.package_releases import PackageReleases


def test_available_packages_equality():
    avs1 = AvailablePackages(
        packages=[
            PackageReleases(name='simplejson', versions=('1.0', '1.1')),
            PackageReleases(name='six', versions=('1.2', '2.3')),
        ],
    )

    # missing one package
    avs2 = AvailablePackages(
        packages=[
            PackageReleases(name='six', versions=('1.2', '2.3')),
        ],
    )

    # name differs
    avs3 = AvailablePackages(
        packages=[
            PackageReleases(name='complicatedyaml', versions=('1.0', '1.1')),
            PackageReleases(name='six', versions=('1.2', '2.3')),
        ],
    )

    # versions differ
    avs4 = AvailablePackages(
        packages=[
            PackageReleases(name='simplejson', versions=('1.0', '1.1')),
            PackageReleases(name='six', versions=('1.2', '2.4')),
        ],
    )

    assert not avs1 == None  # noqa
    assert avs1 == avs1
    assert not avs1 != avs1

    assert avs1 != avs2
    assert not avs1 == avs2

    assert avs1 != avs3
    assert not avs1 == avs3

    assert avs1 != avs4
    assert not avs1 == avs4

    # Test repr
    assert repr(avs1) == (
        "<AvailablePackages num_packages=2>"
    )


def test_available_packages_get_by_name():
    simplejson = PackageReleases(name='simplejson', versions=('1.0', '1.1'))
    six = PackageReleases(name='six', versions=('1.2', '2.4'))

    avs = AvailablePackages(
        packages=[
            simplejson,
            six,
        ],
    )

    # exact name matches
    assert avs.get_by_name('simplejson') is simplejson
    assert avs.get_by_name('six') is six

    # nothing else matches
    assert avs.get_by_name('simplejson==1.0') is None
    assert avs.get_by_name('simple') is None
