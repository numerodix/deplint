from six import StringIO

from deplint.model.package_requirement import PackageRequirement
from deplint.model.requirements_txt import RequirementsTxt
from deplint.parsers.requirements_txt import RequirementsTxtParser


# use every operator
REQS_EXAMPLE = '''
coverage<3.6
parsimonious<=0.5
pytest==2.3.5
six>=1.6.0
tox>1.6.1
mock!=5.1.1
ply~=3.10
jsonpath===2.0.x
simplejson
-i
--index-url=http://something.io
'''

REQS_EXAMPLE_GARBAGE = '''
Something we do not recognize as valid.
'''


def test_requirements_txt_parser():
    reqs_expected = RequirementsTxt(
        packages=[
            PackageRequirement(name='coverage', operator='<', version='3.6'),
            PackageRequirement(name='parsimonious', operator='<=', version='0.5'),
            PackageRequirement(name='pytest', operator='==', version='2.3.5'),
            PackageRequirement(name='six', operator='>=', version='1.6.0'),
            PackageRequirement(name='tox', operator='>', version='1.6.1'),
            PackageRequirement(name='mock', operator='!=', version='5.1.1'),
            PackageRequirement(name='ply', operator='~=', version='3.10'),
            PackageRequirement(name='jsonpath', operator='===', version='2.0.x'),
            PackageRequirement(name='simplejson', operator=None, version=None),
        ],
    )

    parser = RequirementsTxtParser(fileobj=StringIO(REQS_EXAMPLE))
    reqs = parser.parse()

    assert reqs_expected == reqs


def test_requirements_txt_parser_garbage():
    parser = RequirementsTxtParser(fileobj=StringIO(REQS_EXAMPLE_GARBAGE))
    parser.parse()  # does not raise
