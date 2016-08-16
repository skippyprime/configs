import pytest

from assertpy import assert_that


def test_merge_duplicate_keys():
    from figtree.dictconfig import DictConfiguration

    first = DictConfiguration({
        'one': 1,
        'two': 2
    })

    second = {
        'two': 22,
        'three': 3
    }

    # ensure first is correct
    assert_that(first).is_length(2)
    assert_that(first).contains_entry({'one': 1}, {'two': 2})

    # ensure second is correct
    assert_that(second).is_length(2)
    assert_that(second).contains_entry({'two': 22}, {'three': 3})

    # merge dictionaries
    first.merge(second)
    assert_that(first).is_length(3)
    assert_that(first).contains_entry({'one': 1}, {'two': 22}, {'three': 3})
    assert_that(first).does_not_contain_entry({'two': 2})


def test_merge_unique_keys():
    from figtree.dictconfig import DictConfiguration

    first = DictConfiguration({
        'one': 1,
        'two': 2
    })

    second = {
        'three': 3,
        'four': 4
    }

    # ensure first is correct
    assert_that(first).is_length(2)
    assert_that(first).contains_entry({'one': 1}, {'two': 2})

    # ensure second is correct
    assert_that(second).is_length(2)
    assert_that(second).contains_entry({'three': 3}, {'four': 4})

    # merge dictionaries
    first.merge(second)
    assert_that(first).is_length(4)
    assert_that(first).contains_entry(
        {'one': 1},
        {'two': 2},
        {'three': 3},
        {'four': 4})


def test_merge_duplicate_nested_keys():
    from figtree.dictconfig import DictConfiguration

    first = DictConfiguration({
        'one': 1,
        'two': {
            'two_a': '2a',
            'two_b': '2b'
        }
    })

    second = {
        'two': {
            'two_b': '22b',
            'two_c': '2c'
        },
        'three': {
            'three_a': '3a'
        },
        'four': 4
    }

    # ensure first is correct
    assert_that(first).is_length(2)
    assert_that(first).contains_entry({'one': 1})
    assert_that(first).contains_key('two')
    assert_that(first['two']).is_length(2)
    assert_that(first['two']).contains_entry({'two_a': '2a'}, {'two_b': '2b'})

    # ensure second is correct
    assert_that(second).is_length(3)
    assert_that(second).contains_entry({'four': 4})
    assert_that(second).contains_key('two')
    assert_that(second).contains_key('three')
    assert_that(second['two']).is_length(2)
    assert_that(second['two']).contains_entry(
        {'two_b': '22b'},
        {'two_c': '2c'})
    assert_that(second['three']).is_length(1)
    assert_that(second['three']).contains_entry({'three_a': '3a'})

    # merge dictionaries
    first.merge(second)
    assert_that(first).is_length(4)
    assert_that(first).contains_entry({'one': 1}, {'four': 4})
    assert_that(second).contains_key('two')
    assert_that(second).contains_key('three')
    assert_that(first['two']).is_length(3)
    assert_that(first['two']).contains_entry(
        {'two_a': '2a'},
        {'two_b': '22b'},
        {'two_c': '2c'})
    assert_that(first['three']).is_length(1)
    assert_that(first['three']).contains_entry({'three_a': '3a'})
    assert_that(first['two']).does_not_contain_entry({'two_b': '2b'})


def test_merge_duplicate_keys_with_different_types():
    from figtree.dictconfig import DictConfiguration

    first = DictConfiguration({
        'one': 1,
        'two': {
            'two_a': '2a',
            'two_b': '2b'
        }
    })

    second = {
        'two': [2, 1, 2],
        'three': {
            'three_a': '3a'
        },
        'four': 4
    }

    # ensure first is correct
    assert_that(first).is_length(2)
    assert_that(first).contains_entry({'one': 1})
    assert_that(first).contains_key('two')
    assert_that(first['two']).is_type_of(DictConfiguration)
    assert_that(first['two']).is_length(2)
    assert_that(first['two']).contains_entry({'two_a': '2a'}, {'two_b': '2b'})

    # ensure second is correct
    assert_that(second).is_length(3)
    assert_that(second).contains_entry({'four': 4})
    assert_that(second).contains_key('two')
    assert_that(second).contains_key('three')
    assert_that(second['two']).is_instance_of(list)
    assert_that(second['two']).is_equal_to([2, 1, 2])
    assert_that(second['three']).is_length(1)
    assert_that(second['three']).contains_entry({'three_a': '3a'})

    # merge dictionaries
    first.merge(second)
    assert_that(first).is_length(4)
    assert_that(first).contains_entry({'one': 1}, {'four': 4})
    assert_that(first).contains_key('two')
    assert_that(first).contains_key('three')
    assert_that(first['two']).is_instance_of(list)
    assert_that(first['two']).is_equal_to([2, 1, 2])
    assert_that(first['three']).is_length(1)
    assert_that(first['three']).contains_entry({'three_a': '3a'})


@pytest.mark.xfail(raises=ValueError)
def test_merge_non_mapping():
    from figtree.dictconfig import DictConfiguration

    first = DictConfiguration({
        'one': 1,
        'two': 2
    })

    first.merge(['a', 'b'])


def test_make_dict_config():
    from figtree.dictconfig import DictConfiguration

    # pylint: disable=W0212
    result = DictConfiguration._make_dict_config(None)

    assert_that(result).is_none()


def test_maybe_make_dict_config():
    from figtree.dictconfig import DictConfiguration

    # pylint: disable=W0212
    result = DictConfiguration._maybe_make_dict_config(None)

    assert_that(result).is_none()


def test_make_dict_config_non_recursive():
    from figtree.dictconfig import DictConfiguration

    # pylint: disable=W0212
    result = DictConfiguration._make_dict_config({
            'one': {
                'first': 1,
                'second': 2
            }
        },
        recurse=False)

    assert_that(result).is_equal_to({
        'one': {
            'first': 1,
            'second': 2
        }
    })

    assert_that(result).is_type_of(DictConfiguration)
    assert_that(result['one']).is_type_of(DictConfiguration)
