from deplint.model.advice import Advice
from deplint.model.advice_list import AdviceList


def test_advice_list_equality():
    advl1 = AdviceList(
        advice_list=[
            Advice(analyzer=None, severity='info', message='It rains'),
            Advice(analyzer=None, severity='debug', message='It snows'),
        ],
    )

    # missing one advice
    advl2 = AdviceList(
        advice_list=[
            Advice(analyzer=None, severity='info', message='It rains'),
        ],
    )

    # severity differs
    advl3 = AdviceList(
        advice_list=[
            Advice(analyzer=None, severity='error', message='It rains'),
            Advice(analyzer=None, severity='debug', message='It snows'),
        ],
    )

    assert not advl1 == None  # noqa
    assert advl1 == advl1
    assert not advl1 != advl1

    assert advl1 != advl2
    assert not advl1 == advl2

    assert advl1 != advl3
    assert not advl1 == advl3

    # Test repr
    assert repr(advl1) == (
        "<AdviceList num_advice=2>"
    )

    # XXX improve this
    assert advl1.has_problems() is False
    assert advl2.has_problems() is False
    assert advl3.has_problems() is True
