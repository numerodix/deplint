from six import StringIO

from reqlint.model.package_requirement import PackageRequirement
from reqlint.model.requirements_txt import RequirementsTxt
from reqlint.parsers.requirements_txt import RequirementsTxtParser


# use every operator
REQS_EXAMPLE = '''
coverage<3.6
parsimonious<=0.5
pytest==2.3.5
six>=1.6.0
tox>1.6.1
'''


def test_requirements_txt_parser():
    reqs_expected = RequirementsTxt(
        packages=[
            PackageRequirement(name='coverage', operator='<', version='3.6'),
            PackageRequirement(name='parsimonious', operator='<=', version='0.5'),
            PackageRequirement(name='pytest', operator='==', version='2.3.5'),
            PackageRequirement(name='six', operator='>=', version='1.6.0'),
            PackageRequirement(name='tox', operator='>', version='1.6.1'),
        ],
    )

    parser = RequirementsTxtParser(fileobj=StringIO(REQS_EXAMPLE))
    reqs = parser.parse()

    assert reqs_expected == reqs
