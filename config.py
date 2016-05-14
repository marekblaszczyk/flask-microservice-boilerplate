"""
This is application's main config file.
"""

import os
import json


class ConfigCreator(type):
    """
    This metaclass is used to fill a class and module's globals with config data.
    """

    def __new__(mcs, name, bases, attrs):
        basedir = os.path.abspath(os.path.dirname(__file__))
        context = { 'basedir': basedir }

        with open(os.path.join(basedir, 'config.json')) as conf:
            data = conf.read()

        for key, value in context.iteritems():
            data = data.replace('{' + key + '}', value)

        data = json.loads(data)

        for config_item in ('CACHE_DIR'):
            if 'base' in data and config_item in data['base']:
                data['base'][config_item] = basedir + data['base'][config_item]

        attrs.update(data['base'])

        if 'EURO2016_CONFIG' in os.environ and os.environ['EURO2016_CONFIG'].lower() in data:
            attrs.update(data[os.environ['EURO2016_CONFIG'].lower()])
        else:
            attrs.update(data['development'])

        return super(ConfigCreator, mcs).__new__(mcs, name, bases, attrs)

    def __getitem__(cls, item):
        return getattr(cls, item)


class Config(object):
    """
    This class keeps config data.
    """
    __metaclass__ = ConfigCreator
