import pytest

from deplint.analyzers.required_not_installed import \
    RequiredNotInstalledAnalyzer
from deplint.model.advice import Advice


def test_advice_ctor():
    with pytest.raises(ValueError):
        Advice(analyzer=None, severity='extreme', message='OK')


def test_advice_equality():
    analyzer1 = RequiredNotInstalledAnalyzer(
        requirements_txt=None,
        installed_packages=None,
    )

    adv1 = Advice(analyzer=analyzer1, severity='error', message='Package not good')

    # different analyzer

    # different severity
    adv3 = Advice(analyzer=analyzer1, severity='warn', message='Package not good')

    # different message
    adv4 = Advice(analyzer=analyzer1, severity='error', message='Package very good')

    assert not adv1 == None  # noqa
    assert adv1 == adv1
    assert not adv1 != adv1

    assert adv1 != adv3
    assert not adv1 == adv3

    assert adv1 != adv4
    assert not adv1 == adv4

    # Test repr
    assert repr(adv1) == (
        "<Advice analyzer='RequiredNotInstalledAnalyzer', "
        "severity='error', message='Package not good'>"
    )


def test_advice_format_display_line():
    analyzer1 = RequiredNotInstalledAnalyzer(
        requirements_txt=None,
        installed_packages=None,
    )

    adv1 = Advice(analyzer=analyzer1, severity='error', message='Package not good')

    assert adv1.format_display_line() == (
        '[RequiredNotInstalled] error: Package not good'
    )
