from reqlint.model.package_releases import PackageReleases


def test_package_releases_equality():
    pkg1 = PackageReleases(name='simplejson', versions=('1.0', '1.1'))

    # different name
    pkg2 = PackageReleases(name='difficultyaml', versions=('1.0', '1.1'))

    # different version
    pkg3 = PackageReleases(name='simplejson', versions=('1.0', '1.2'))

    assert pkg1 == pkg1
    assert not pkg1 != pkg1

    assert pkg1 != pkg2
    assert not pkg1 == pkg2

    assert pkg1 != pkg3
    assert not pkg1 == pkg3
