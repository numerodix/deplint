from deplint.model.package_requirement import PackageRequirement
from deplint.model.requirements_txt import RequirementsTxt


def test_requirements_txt_equality():
    reqs1 = RequirementsTxt(
        packages=[
            PackageRequirement(name='coverage', operator='<', version='3.6'),
            PackageRequirement(name='parsimonious', operator='<=', version='0.5'),
        ],
    )

    # missing one package
    reqs2 = RequirementsTxt(
        packages=[
            PackageRequirement(name='coverage', operator='<', version='3.6'),
        ],
    )

    # operator differs
    reqs3 = RequirementsTxt(
        packages=[
            PackageRequirement(name='coverage', operator='<', version='3.6'),
            PackageRequirement(name='parsimonious', operator='==', version='0.5'),
        ],
    )

    assert not reqs1 == None  # noqa
    assert reqs1 == reqs1
    assert not reqs1 != reqs1

    assert reqs1 != reqs2
    assert not reqs1 == reqs2

    assert reqs1 != reqs3
    assert not reqs1 == reqs3

    # Test repr
    assert repr(reqs1) == '<RequirementsTxt num_packages=2>'


def test_requirements_txt_get_by_name():
    coverage = PackageRequirement(name='coverage', operator='<', version='3.6')

    reqs = RequirementsTxt(
        packages=[
            coverage,
        ],
    )

    # exact name matches
    assert reqs.get_by_name('coverage') is coverage
    assert reqs.get_by_name('Coverage') is None

    # ignore case
    assert reqs.get_by_name('coverage', ignore_case=True) is coverage
    assert reqs.get_by_name('Coverage', ignore_case=True) is coverage

    # nothing else matches
    assert reqs.get_by_name('coverage==1.0') is None
    assert reqs.get_by_name('cov') is None
