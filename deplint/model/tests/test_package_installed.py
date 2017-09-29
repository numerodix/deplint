from deplint.model.package_installed import InstalledPackage


def test_package_installed_equality():
    pkg1 = InstalledPackage(name='simplejson', version='1.1')

    # different name
    pkg2 = InstalledPackage(name='difficultyaml', version='1.1')

    # different version
    pkg3 = InstalledPackage(name='simplejson', version='1.2')

    assert not pkg1 == None  # noqa
    assert pkg1 == pkg1
    assert not pkg1 != pkg1

    assert pkg1 != pkg2
    assert not pkg1 == pkg2

    assert pkg1 != pkg3
    assert not pkg1 == pkg3

    # Test repr
    assert repr(pkg1) == (
        "<InstalledPackage name='simplejson', version='1.1'>"
    )
