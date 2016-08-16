figtree
=======

Figtree is a multi-format configuration file loader that normalizes all
values into dictionaries and supports merging multiple configuration
files into a single source. The later can be useful if you have multiple
configuration sources and either want to load the first found or
override default settings (such as having a system wide and per user
configuration file).

Figtree supports the following configuration file formats:

-  YAML
-  JSON
-  XML (Currently ignores attributes)
-  INI (Currently does not support dictionaries within lists)

The Figtree API is also easily extensible to support new structured file
formats through automatic registration of format handlers.

Simple Example
--------------

Configuration source: /etc/myproject/settings.yml

.. code:: yaml

    section:
      debug: on
      complex:
        structure:
          value: 100
          multi:
            - 1
            - 2
            - 3
    flag: off

Loading and access data.

.. code:: python

    import figtree

    conf = figtree.load_config('@/etc/myproject/settings.yml')

    # configuration instances are dictionary like
    flag_set = conf['flag']

    # nested structures are also dictionary like
    is_debugging = conf['section']['debug']

    # easier lookups to avoid intermediate key checks
    is_debugging = conf['section.debug']
    is_debugging = conf.get('section.debug', False)

    # sub-dictionaries can be accessed the same way
    conf_section = conf['section']
    value = conf_section['complex.structure.value']

Loading Options
---------------

Configuration files can be loaded from the following sources:

-  Files (Local and HTTP accessible)
-  String Literals
-  Dictionary Objects

Merge Settings
~~~~~~~~~~~~~~

Load in order and merge settings. The last item has overrides others.

.. code:: python

    import figtree

    conf = figtree.load_config(
        (
            {
                'section': {
                    'debug': True
                },
                'flag': False
            },
            '/etc/myproject/settings.yml',
            'https://mydomain.test/settings',
            figtree.LiteralConfigSource('flag: off', hint='yaml')
        )
    )

First Found
~~~~~~~~~~~

Load the first found source. Mostly useful for file based sources.

.. code:: python

    import figtree

    conf = figtree.load_first_found_config(
        (
            'settings.yml',
            '~/.settings.yml',
            '/etc/myproject/settings.yml'
        )
    )
