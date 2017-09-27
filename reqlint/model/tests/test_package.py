from reqlint.model.package import PackageRequirement


def test_package_equality():
    pkg1 = PackageRequirement(name='simplejson', operator='==', version='1.1')

    # different operator
    pkg2 = PackageRequirement(name='simplejson', operator='>=', version='1.1')

    # different version
    pkg3 = PackageRequirement(name='simplejson', operator='==', version='1.2')

    assert pkg1 == pkg1
    assert not pkg1 != pkg1

    assert pkg1 != pkg2
    assert not pkg1 == pkg2

    assert pkg1 != pkg3
    assert not pkg1 == pkg3
