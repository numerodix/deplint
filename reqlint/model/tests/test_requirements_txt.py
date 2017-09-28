from reqlint.model.package_requirement import PackageRequirement
from reqlint.model.requirements_txt import RequirementsTxt


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

    assert reqs1 == reqs1
    assert not reqs1 != reqs1

    assert reqs1 != reqs2
    assert not reqs1 == reqs2

    assert reqs1 != reqs3
    assert not reqs1 == reqs3
