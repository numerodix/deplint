from reqlint.model.package_requirement import PackageRequirement


def test_package_requirement_equality():
    pkg1 = PackageRequirement(name='simplejson', operator='==', version='1.1')

    # different name
    pkg2 = PackageRequirement(name='difficultyaml', operator='==', version='1.1')

    # different operator
    pkg3 = PackageRequirement(name='simplejson', operator='>=', version='1.1')

    # different version
    pkg4 = PackageRequirement(name='simplejson', operator='==', version='1.2')

    assert pkg1 == pkg1
    assert not pkg1 != pkg1

    assert pkg1 != pkg2
    assert not pkg1 == pkg2

    assert pkg1 != pkg3
    assert not pkg1 == pkg3

    assert pkg1 != pkg4
    assert not pkg1 == pkg4


def test_package_requirement_display_name():
    pkg1 = PackageRequirement(name='simplejson', operator='==', version='1.1')

    assert pkg1.as_display_name() == 'simplejson==1.1'
