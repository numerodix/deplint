import pytest

from deplint.model.package_installed import InstalledPackage
from deplint.model.package_requirement import PackageRequirement


def test_package_requirement_ctor():
    with pytest.raises(ValueError):
        PackageRequirement(name='simplejson', operator='<<', version='1.1')


def test_package_requirement_operator_and_version():
    pkg = PackageRequirement(name='simplejson', operator=None, version=None)

    assert pkg.has_operator() is False
    with pytest.raises(RuntimeError):
        pkg.operator

    assert pkg.has_version() is False
    with pytest.raises(RuntimeError):
        pkg.version


def test_package_requirement_equality():
    pkg1 = PackageRequirement(name='simplejson', operator='==', version='1.1')

    # different name
    pkg2 = PackageRequirement(name='difficultyaml', operator='==', version='1.1')

    # different operator
    pkg3 = PackageRequirement(name='simplejson', operator='>=', version='1.1')

    # different version
    pkg4 = PackageRequirement(name='simplejson', operator='==', version='1.2')

    assert not pkg1 == None  # noqa
    assert pkg1 == pkg1
    assert not pkg1 != pkg1

    assert pkg1 != pkg2
    assert not pkg1 == pkg2

    assert pkg1 != pkg3
    assert not pkg1 == pkg3

    assert pkg1 != pkg4
    assert not pkg1 == pkg4

    # Test repr
    assert repr(pkg1) == (
        "<PackageRequirement name='simplejson', operator='==', version='1.1'>"
    )


def test_package_requirement_display_name():
    pkg1 = PackageRequirement(name='simplejson', operator='==', version='1.1')
    assert pkg1.as_display_name() == 'simplejson==1.1'

    pkg2 = PackageRequirement(name='simplejson', operator=None, version=None)
    assert pkg2.as_display_name() == 'simplejson'


def test_package_requirement_is_satisfied_by():
    # Testing against version
    req1 = PackageRequirement(name='simplejson', operator='~=', version='1.1')

    # wrong name
    ins1 = InstalledPackage(name='six', version='1.1')
    assert req1.is_satisfied_by(ins1) is False

    # exact match
    ins2 = InstalledPackage(name='simplejson', version='1.1')
    assert req1.is_satisfied_by(ins2) is True

    # inexact match
    ins3 = InstalledPackage(name='simplejson', version='1.1.1')
    assert req1.is_satisfied_by(ins3) is True


    # Testing below version
    req2 = PackageRequirement(name='Flask', operator='<=', version='1.0')

    # below version
    ins4 = InstalledPackage(name='Flask', version='0.9')
    assert req2.is_satisfied_by(ins4) is True

    # exact version
    ins5 = InstalledPackage(name='Flask', version='1.0')
    assert req2.is_satisfied_by(ins5) is True

    # above version
    ins6 = InstalledPackage(name='Flask', version='1.1')
    assert req2.is_satisfied_by(ins6) is False


    # Testing above version
    req3 = PackageRequirement(name='Django', operator='>=', version='5.0')

    # below version
    ins7 = InstalledPackage(name='Django', version='4.9')
    assert req3.is_satisfied_by(ins7) is False

    # exact version
    ins8 = InstalledPackage(name='Django', version='5.0')
    assert req3.is_satisfied_by(ins8) is True

    # above version
    ins9 = InstalledPackage(name='Django', version='5.1')
    assert req3.is_satisfied_by(ins9) is True


    # Testing without version
    req1 = PackageRequirement(name='simplejson', operator=None, version=None)

    # wrong name
    ins1 = InstalledPackage(name='six', version='1.1')
    assert req1.is_satisfied_by(ins1) is False

    # any version match
    ins2 = InstalledPackage(name='simplejson', version='1.1')
    assert req1.is_satisfied_by(ins2) is True
