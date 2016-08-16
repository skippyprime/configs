import sys
import collections
import copy
import io

try:
    import simplejson as json
except ImportError:
    import json

import pytest

import yaml

import six
import lxml.objectify
import lxml.etree


TEST_DATA_A_INI = '''
[parent_a]
child_aa = 1
child_ab = 2

'''


TEST_DATA_B_INI = '''
[parent_b]
child_ba.grand_child_baa = 3
child_ba.grand_child_bab = 4
child_bb = 5
child_bc = a
child_bc = b
child_bc = c
'''


TEST_DATA_FULL_INI = TEST_DATA_A_INI + TEST_DATA_B_INI


TEST_DATA_FULL = {
    'parent_a': {
        'child_aa': 1,
        'child_ab': 2
    },
    'parent_b': {
        'child_ba': {
            'grand_child_baa': 3,
            'grand_child_bab': 4
        },
        'child_bb': 5,
        'child_bc': [
            'a',
            'b',
            'c'
        ]
    }
}


TestDataSource = collections.namedtuple(
    'TestDataSource',
    [
        'full',
        'a',
        'b'
    ])

TestDataItem = collections.namedtuple(
    'TestDataItem',
    [
        'source',
        'parsed'
    ])


@pytest.fixture(scope='session')
def config_set(tmpdir_factory, request):
    from figtree import FileConfigSource, ObjectConfigSource

    params = request.param

    # return copies of test objects if objects requested
    if params.disposition == 'object':
        testdata_a = copy.deepcopy(TEST_DATA_FULL)
        testdata_a.pop('parent_b')
        testdata_b = copy.deepcopy(TEST_DATA_FULL)
        testdata_b.pop('parent_a')

        return TestDataSource(
            full=TestDataItem(
                source=ObjectConfigSource(
                    copy.deepcopy(TEST_DATA_FULL)),
                parsed=copy.deepcopy(TEST_DATA_FULL)),
            a=TestDataItem(
                ObjectConfigSource(
                    testdata_a),
                parsed=copy.deepcopy(testdata_a)),
            b=TestDataItem(
                ObjectConfigSource(
                    testdata_b),
                parsed=copy.deepcopy(testdata_b)))

    # create the configs in their encoded format as literals
    this = sys.modules[__name__]
    maker = getattr(this,
                    '_make_confs_{0:s}'.format(params.format),
                    _make_confs_unimplemented)

    literal_confs = maker(params.hint or params.format)

    # if requested literals, nothing more to be done
    if params.disposition == 'literal':
        return literal_confs

    # either requesting a file or filename
    if params.disposition.startswith('file'):
        extension = params.extension or params.hint or params.format
        full_file = '@' + str(tmpdir_factory.mktemp('data').join(
            'config_full.{0:s}'.format(extension)))
        a_file = '@' + str(tmpdir_factory.mktemp('data').join(
            'config_a.{0:s}'.format(extension)))
        b_file = '@' + str(tmpdir_factory.mktemp('data').join(
            'config_b.{0:s}'.format(extension)))

        if params.disposition == 'file':
            full_file = FileConfigSource(full_file, hint=params.hint)
            a_file = FileConfigSource(a_file, hint=params.hint)
            b_file = FileConfigSource(b_file, hint=params.hint)

        file_confs = TestDataSource(
            full=TestDataItem(
                source=full_file,
                parsed=literal_confs.full.parsed),
            a=TestDataItem(
                source=a_file,
                parsed=literal_confs.a.parsed),
            b=TestDataItem(
                source=b_file,
                parsed=literal_confs.b.parsed))

        for l, f in six.moves.zip(literal_confs, file_confs):
            filename = f.source
            if isinstance(filename, FileConfigSource):
                filename = filename.source
            else:
                filename = filename[1:]
            mode = 'w' if isinstance(l.source.source, six.text_type)\
                else 'wb'
            with io.open(filename, mode=mode) as outstream:
                outstream.write(l.source.source)

        return file_confs


# pylint: disable=W0613
def _make_confs_unimplemented(hint):
    raise NotImplementedError(
        'Request for unsupported or not implement config format')


def _make_confs_xml(hint):
    from figtree import LiteralConfigSource

    testdata_a = copy.deepcopy(TEST_DATA_FULL)
    testdata_a.pop('parent_b')
    testdata_b = copy.deepcopy(TEST_DATA_FULL)
    testdata_b.pop('parent_a')

    maker = lxml.objectify.ElementMaker(annotate=False)

    confs = TestDataSource(
        full=TestDataItem(
            source=LiteralConfigSource(
                lxml.etree.tostring(
                    maker.config(
                        maker.parent_a(
                            maker.child_aa(1),
                            maker.child_ab(2)
                        ),
                        maker.parent_b(
                            maker.child_ba(
                                maker.grand_child_baa(3),
                                maker.grand_child_bab(4)
                            ),
                            maker.child_bb(5),
                            maker.child_bc('a'),
                            maker.child_bc('b'),
                            maker.child_bc('c')
                        )
                    ), pretty_print=True),
                hint=hint),
            parsed=copy.deepcopy(TEST_DATA_FULL)),
        a=TestDataItem(
            source=LiteralConfigSource(
                lxml.etree.tostring(
                    maker.config(
                        maker.parent_a(
                            maker.child_aa(1),
                            maker.child_ab(2)
                        )
                    ), pretty_print=True),
                hint=hint),
            parsed=testdata_a),
        b=TestDataItem(
            source=LiteralConfigSource(
                lxml.etree.tostring(
                    maker.config(
                        maker.parent_b(
                            maker.child_ba(
                                maker.grand_child_baa(3),
                                maker.grand_child_bab(4)
                            ),
                            maker.child_bb(5),
                            maker.child_bc('a'),
                            maker.child_bc('b'),
                            maker.child_bc('c')
                        )
                    ), pretty_print=True),
                hint=hint),
            parsed=testdata_b))

    return confs


def _make_confs_ini(hint):
    from figtree import LiteralConfigSource

    testdata_a = copy.deepcopy(TEST_DATA_FULL)
    testdata_a.pop('parent_b')
    testdata_b = copy.deepcopy(TEST_DATA_FULL)
    testdata_b.pop('parent_a')

    confs = TestDataSource(
        full=TestDataItem(
            source=LiteralConfigSource(
                TEST_DATA_FULL_INI,
                hint=hint),
            parsed=copy.deepcopy(TEST_DATA_FULL)),
        a=TestDataItem(
            source=LiteralConfigSource(
                TEST_DATA_A_INI,
                hint=hint),
            parsed=testdata_a),
        b=TestDataItem(
            source=LiteralConfigSource(
                TEST_DATA_B_INI,
                hint=hint),
            parsed=testdata_b))

    return confs


def _make_confs_yaml(hint):
    from figtree import LiteralConfigSource

    testdata_a = copy.deepcopy(TEST_DATA_FULL)
    testdata_a.pop('parent_b')
    testdata_b = copy.deepcopy(TEST_DATA_FULL)
    testdata_b.pop('parent_a')

    confs = TestDataSource(
        full=TestDataItem(
            source=LiteralConfigSource(
                yaml.dump(TEST_DATA_FULL),
                hint=hint),
            parsed=copy.deepcopy(TEST_DATA_FULL)),
        a=TestDataItem(
            source=LiteralConfigSource(
                yaml.dump(testdata_a),
                hint=hint),
            parsed=testdata_a),
        b=TestDataItem(
            source=LiteralConfigSource(
                yaml.dump(testdata_b),
                hint=hint),
            parsed=testdata_b))

    return confs


def _make_confs_json(hint):
    from figtree import LiteralConfigSource

    testdata_a = copy.deepcopy(TEST_DATA_FULL)
    testdata_a.pop('parent_b')
    testdata_b = copy.deepcopy(TEST_DATA_FULL)
    testdata_b.pop('parent_a')

    confs = TestDataSource(
        full=TestDataItem(
            source=LiteralConfigSource(
                json.dumps(TEST_DATA_FULL),
                hint=hint),
            parsed=copy.deepcopy(TEST_DATA_FULL)),
        a=TestDataItem(
            source=LiteralConfigSource(
                json.dumps(testdata_a),
                hint=hint),
            parsed=testdata_a),
        b=TestDataItem(
            source=LiteralConfigSource(
                json.dumps(testdata_b),
                hint=hint),
            parsed=testdata_b))

    return confs
