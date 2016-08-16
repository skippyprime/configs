import collections

import pytest

from assertpy import assert_that


@pytest.mark.xfail(raises=KeyError)
def test_lookup_on_none():
    from configs.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': None
    })

    # access child of None type
    # pylint: disable=W0104
    conf['one.noexist']


@pytest.mark.xfail(raises=KeyError)
def test_lookup_on_non_mapping():
    from configs.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 'a'
    })

    # access child of None type
    # pylint: disable=W0104
    conf['one.noexist']


@pytest.mark.xfail(raises=KeyError)
def test_lookup_empty_key():
    from configs.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 'a'
    })

    # access child of None type
    # pylint: disable=W0104
    conf['']


@pytest.mark.xfail(raises=KeyError)
def test_lookup_none_key():
    from configs.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 'a'
    })

    # access child of None type
    # pylint: disable=W0104
    conf[None]


@pytest.mark.xfail(raises=TypeError)
def test_lookup_non_string_key():
    from configs.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 'a'
    })

    # access child of None type
    # pylint: disable=W0104
    conf[1]


@pytest.mark.xfail(raises=KeyError)
def test_lookup_empty_key():
    from configs.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 'a'
    })

    # access child of None type
    # pylint: disable=W0104
    conf['one..b']
