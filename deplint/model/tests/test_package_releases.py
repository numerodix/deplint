import pytest

from deplint.model.package_releases import PackageReleases


def test_package_releases_equality():
    pkg1 = PackageReleases(name='simplejson', versions=('1.0', '1.1'))

    # different name
    pkg2 = PackageReleases(name='difficultyaml', versions=('1.0', '1.1'))

    # different version
    pkg3 = PackageReleases(name='simplejson', versions=('1.0', '1.2'))

    assert not pkg1 == None  # noqa
    assert pkg1 == pkg1
    assert not pkg1 != pkg1

    assert pkg1 != pkg2
    assert not pkg1 == pkg2

    assert pkg1 != pkg3
    assert not pkg1 == pkg3

    # Test repr
    assert repr(pkg1) == (
        "<PackageReleases name='simplejson', versions=['1.0', '1.1']>"
    )


def test_package_releases_as_display_name_single():
    pkg1 = PackageReleases(name='simplejson', versions=('1.0',))
    pkg2 = PackageReleases(name='simplejson', versions=('1.0', '1.1'))

    assert pkg1.as_display_name_single() == 'simplejson-1.0'

    with pytest.raises(ValueError):
        pkg2.as_display_name_single()
