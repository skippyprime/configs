import pytest

from assertpy import assert_that


def test_update_with_mapping():
    from figtree.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 'a'
    })

    conf['two.child.grandchild'] = 1

    assert_that(conf).is_equal_to({
        'one': 'a',
        'two': {
            'child': {
                'grandchild': 1
            }
        }
    })

    assert_that(conf['two']).is_type_of(DictConfiguration)


def test_update_with_dict():
    from figtree.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 'a'
    })

    conf['two.child.grandchild'] = {}

    conf['two.child.grandchild.first'] = 1

    assert_that(conf).is_equal_to({
        'one': 'a',
        'two': {
            'child': {
                'grandchild': {
                    'first': 1
                }
            }
        }
    })

    assert_that(conf['two']).is_type_of(DictConfiguration)


def test_update_overwrite_with_mapping():
    from figtree.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 'a',
        'two': 'b'
    })

    conf['two.child.grandchild'] = 1

    assert_that(conf).is_equal_to({
        'one': 'a',
        'two': {
            'child': {
                'grandchild': 1
            }
        }
    })

    assert_that(conf['two']).is_type_of(DictConfiguration)


def test_delete_key():
    from figtree.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 1,
        'two': 2
    })

    # delete child of None type
    del conf['one']

    assert_that(conf).is_equal_to({
        'two': 2
    })


@pytest.mark.xfail(raises=KeyError)
def test_delete_on_none():
    from figtree.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': None
    })

    # delete child of None type
    del conf['one.noexist']


@pytest.mark.xfail(raises=KeyError)
def test_delete_on_non_mapping():
    from figtree.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 'a'
    })

    # delete child of non-mapping type
    del conf['one.noexist']


@pytest.mark.xfail(raises=KeyError)
def test_delete_on_none_leaf():
    from figtree.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': None
    })

    # delete child of None type
    del conf['one.noexist.reallynotthere']


@pytest.mark.xfail(raises=KeyError)
def test_delete_on_non_mapping_leaf():
    from figtree.dictconfig import DictConfiguration

    conf = DictConfiguration({
        'one': 'a'
    })

    # delete child of non-mapping type
    del conf['one.noexist.reallynotthere']
