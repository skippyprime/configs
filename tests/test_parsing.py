import collections

import pytest
import responses
import six

from assertpy import assert_that

from .utils import ConfigParams


@pytest.mark.parametrize('config_set',
                         [
                            # common mappings
                            ConfigParams('xml', None, 'filename', None),
                            ConfigParams('xml', None, 'file', None),
                            ConfigParams('xml', None, 'literal', None),
                            ConfigParams('yaml', None, 'filename', None),
                            ConfigParams('yaml', None, 'file', None),
                            ConfigParams('yaml', None, 'literal', None),
                            ConfigParams('json', None, 'filename', None),
                            ConfigParams('json', None, 'file', None),
                            ConfigParams('json', None, 'literal', None),
                            ConfigParams('ini', None, 'filename', None),
                            ConfigParams('ini', None, 'file', None),
                            ConfigParams('ini', None, 'literal', None),
                            ConfigParams(None, None, 'object', None),

                            # unknown hints (try any)
                            ConfigParams('xml', None, 'filename', 'xyz'),
                            ConfigParams('xml', None, 'file', 'xyz'),
                            ConfigParams('yaml', None, 'filename', 'xyz'),
                            ConfigParams('yaml', None, 'file', 'xyz'),
                            ConfigParams('json', None, 'filename', 'xyz'),
                            ConfigParams('json', None, 'file', 'xyz'),
                            ConfigParams('ini', None, 'filename', 'xyz'),
                            ConfigParams('ini', None, 'file', 'xyz'),
                         ],
                         indirect=['config_set'])
def test_load_and_merge_local_file(config_set):
    from figtree import load_config

    conf = load_config(
        (
            config_set.a.source,
            config_set.b.source
        ))

    # ensure parsed correctly
    assert_that(conf).is_length(2)
    assert_that(conf).is_equal_to(config_set.full.parsed)


@pytest.mark.parametrize('config_set',
                         [
                            # common mappings
                            ConfigParams('xml', None, 'filename', None),
                            ConfigParams('xml', None, 'file', None),
                            ConfigParams('xml', None, 'literal', None),
                            ConfigParams('yaml', None, 'filename', None),
                            ConfigParams('yaml', None, 'file', None),
                            ConfigParams('yaml', None, 'literal', None),
                            ConfigParams('json', None, 'filename', None),
                            ConfigParams('json', None, 'file', None),
                            ConfigParams('json', None, 'literal', None),
                            ConfigParams('ini', None, 'filename', None),
                            ConfigParams('ini', None, 'file', None),
                            ConfigParams('ini', None, 'literal', None),
                            ConfigParams(None, None, 'object', None),

                            # unknown hints (try any)
                            ConfigParams('xml', None, 'filename', 'xyz'),
                            ConfigParams('xml', None, 'file', 'xyz'),
                            ConfigParams('yaml', None, 'filename', 'xyz'),
                            ConfigParams('yaml', None, 'file', 'xyz'),
                            ConfigParams('json', None, 'filename', 'xyz'),
                            ConfigParams('json', None, 'file', 'xyz'),
                            ConfigParams('ini', None, 'filename', 'xyz'),
                            ConfigParams('ini', None, 'file', 'xyz'),
                         ],
                         indirect=['config_set'])
def test_load_first_local_file(config_set):
    from figtree import load_first_found_config

    conf = load_first_found_config(
        (
            config_set.a.source,
            config_set.b.source
        ))

    # ensure parsed correctly
    assert_that(conf).is_length(1)
    assert_that(conf).is_not_equal_to(config_set.full.parsed)
    assert_that(conf).is_not_equal_to(config_set.b.parsed)
    assert_that(conf).is_equal_to(config_set.a.parsed)


@pytest.mark.parametrize('config_set',
                         [
                            # common mappings
                            ConfigParams('xml', None, 'filename', None),
                            ConfigParams('xml', None, 'file', None),
                            ConfigParams('xml', None, 'literal', None),
                            ConfigParams('yaml', None, 'filename', None),
                            ConfigParams('yaml', None, 'file', None),
                            ConfigParams('yaml', None, 'literal', None),
                            ConfigParams('json', None, 'filename', None),
                            ConfigParams('json', None, 'file', None),
                            ConfigParams('json', None, 'literal', None),
                            ConfigParams('ini', None, 'filename', None),
                            ConfigParams('ini', None, 'file', None),
                            ConfigParams('ini', None, 'literal', None),
                            ConfigParams(None, None, 'object', None),

                            # unknown hints (try any)
                            ConfigParams('xml', None, 'filename', 'xyz'),
                            ConfigParams('xml', None, 'file', 'xyz'),
                            ConfigParams('yaml', None, 'filename', 'xyz'),
                            ConfigParams('yaml', None, 'file', 'xyz'),
                            ConfigParams('json', None, 'filename', 'xyz'),
                            ConfigParams('json', None, 'file', 'xyz'),
                            ConfigParams('ini', None, 'filename', 'xyz'),
                            ConfigParams('ini', None, 'file', 'xyz'),
                         ],
                         indirect=['config_set'])
def test_load_local_file(config_set):
    from figtree import load_config

    conf = load_config(config_set.full.source)

    # ensure parsed correctly
    assert_that(conf).is_length(2)
    assert_that(conf).is_equal_to(config_set.full.parsed)


@pytest.mark.parametrize('test_input,expected',
                         [
                             ('yes', True),
                             ('YES', True),
                             ('on', True),
                             ('ON', True),
                             ('true', True),
                             ('TRUE', True),
                             ('no', False),
                             ('NO', False),
                             ('off', False),
                             ('OFF', False),
                             ('false', False),
                             ('FALSE', False),
                             pytest.mark.xfail((None, None),
                                               raises=ValueError),
                             pytest.mark.xfail((1, None),
                                               raises=ValueError),
                             pytest.mark.xfail(('a', None),
                                               raises=ValueError),
                         ])
def test_parse_bool_string(test_input, expected):
    from figtree.parsers import _bool
    assert_that(_bool(test_input)).is_equal_to(expected)


@pytest.mark.parametrize('test_input,expected',
                         [
                             ('1', 1),
                             ('100', 100),
                             ('1.1', 1.1),
                             ('100.345', 100.345),
                             ('true', True),
                             ('false', False),
                             ('abcdef', 'abcdef'),
                             ({'one': 'two'}, {'one': 'two'}),
                             (['abc', 'def'], ['abc', 'def']),
                             (None, None)
                         ])
def test_parse_value_string(test_input, expected):
    from figtree.parsers import _parse_value
    assert_that(_parse_value(test_input)).is_equal_to(expected)


@pytest.mark.parametrize('test_input',
                         [
                             'yaml',
                             'yml',
                             'json',
                             'cfg',
                             'conf',
                             'cnf',
                             'config',
                             'ini',
                             'xml',
                             pytest.mark.xfail('xyz',
                                               raises=ValueError),
                         ])
def test_hints(test_input):
    from figtree import LiteralConfigSource, FileConfigSource

    assert_that(LiteralConfigSource('ancdef', hint=test_input)).is_not_none()
    assert_that(
        FileConfigSource('/tmp/abc/def/test.xyz',
                         hint=test_input)).is_not_none()


@pytest.mark.parametrize('test_input',
                         [
                             pytest.mark.xfail(
                                '',
                                raises=ValueError),
                             pytest.mark.xfail(
                                None,
                                raises=ValueError),
                         ])
def test_no_source_file(test_input):
    from figtree import FileConfigSource

    # pylint: disable=W0612
    conf_source = FileConfigSource(test_input)  # NOQA


@pytest.mark.parametrize('test_input',
                         [
                             pytest.mark.xfail(
                                '',
                                raises=ValueError),
                             pytest.mark.xfail(
                                None,
                                raises=ValueError),
                         ])
def test_no_source_literal(test_input):
    from figtree import LiteralConfigSource

    # pylint: disable=W0612
    conf_source = LiteralConfigSource(test_input)  # NOQA


def test_load_empty_source():
    from figtree import load_config
    from figtree.loader import EmptyConfigSource

    conf = load_config(EmptyConfigSource(None))

    assert_that(conf).is_not_none()
    assert_that(EmptyConfigSource(None).load()).is_none()


def test_load_object_source():
    from figtree import load_config

    test_data = {'a': 'b'}

    conf = load_config(test_data)

    assert_that(conf).is_equal_to(test_data)


def test_load_none_source():
    from figtree import load_config

    conf = load_config(None)

    assert_that(conf).is_equal_to({})


@pytest.mark.parametrize('config_set,encoding',
                         [
                            # common mappings
                            (
                                ConfigParams('xml', None, 'literal', None),
                                'xml'
                            ),
                            (
                                ConfigParams('yaml', None, 'literal', None),
                                'yaml'
                            ),
                            (
                                ConfigParams('json', None, 'literal', None),
                                'json'
                            ),
                            (
                                ConfigParams('ini', None, 'literal', None),
                                'ini'
                            ),
                         ],
                         indirect=['config_set'])
def test_load_remote_http_with_content_type(config_set, encoding):
    from figtree import load_config, FileConfigSource
    from figtree.loader import MIME_TYPE_HINTS

    content_types = collections.defaultdict(list)
    for k, v in six.iteritems(MIME_TYPE_HINTS):
        content_types[v].append(k)
    content_types = content_types[encoding]

    for content_type in content_types:
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(responses.GET,
                              'http://doesnotexist.localdomain',
                              body=config_set.full.source.source,
                              status=200,
                              content_type=content_type)

            conf = load_config(
                FileConfigSource('http://doesnotexist.localdomain'))

            # ensure parsed correctly
            assert_that(conf).is_length(2)
            assert_that(conf).is_equal_to(config_set.full.parsed)


@pytest.mark.parametrize('config_set,encoding',
                         [
                            # common mappings
                            (
                                ConfigParams('xml', None, 'literal', None),
                                'xml'
                            ),
                            (
                                ConfigParams('yaml', None, 'literal', None),
                                'yaml'
                            ),
                            (
                                ConfigParams('json', None, 'literal', None),
                                'json'
                            ),
                            (
                                ConfigParams('ini', None, 'literal', None),
                                'ini'
                            ),
                         ],
                         indirect=['config_set'])
def test_load_remote_http_with_extension(config_set, encoding):
    from figtree import load_config, FileConfigSource
    from figtree.loader import MIME_TYPE_HINTS

    url = 'http://doesnotexist.localdomain/config.{0:s}'.format(encoding)

    with responses.RequestsMock() as requests_mock:
        requests_mock.add(responses.GET,
                          url,
                          body=config_set.full.source.source,
                          status=200,
                          content_type='application/x-testtestest')

        conf = load_config(FileConfigSource(url))

        # ensure parsed correctly
        assert_that(conf).is_length(2)
        assert_that(conf).is_equal_to(config_set.full.parsed)


@pytest.mark.parametrize('config_set,encoding',
                         [
                            # common mappings
                            (
                                ConfigParams('yaml', None, 'literal', None),
                                'yaml'
                            )
                         ],
                         indirect=['config_set'])
def test_load_remote_http_error(config_set, encoding):
    from figtree import load_config, FileConfigSource
    from figtree.loader import MIME_TYPE_HINTS

    url = 'http://doesnotexist.localdomain/config.{0:s}'.format(encoding)

    with responses.RequestsMock() as requests_mock:
        requests_mock.add(responses.GET,
                          url,
                          body=config_set.full.source.source,
                          status=404,
                          content_type='application/x-testtestest')

        conf = load_config(FileConfigSource(url))

        # ensure parsed correctly
        assert_that(conf).is_length(0)
        assert_that(conf).is_equal_to({})
