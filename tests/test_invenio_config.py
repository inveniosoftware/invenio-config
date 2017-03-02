# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Simple tests."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile
import warnings
from os.path import join

from flask import Flask
from mock import patch
from pkg_resources import EntryPoint

from invenio_config import InvenioConfigDefault, \
    InvenioConfigEntryPointModule, InvenioConfigEnvironment, \
    InvenioConfigInstanceFolder, InvenioConfigModule, create_config_loader


class ConfigEP(EntryPoint):
    """Mocking of entrypoint."""

    def __init__(self, **kwargs):
        """Save keyword arguments as config."""
        self.kwargs = kwargs

    def load(self):
        """Mock load entry point."""
        class Config(object):
            pass
        for key, val in self.kwargs.items():
            setattr(Config, key, val)
        return Config


def _mock_ep(eps):
    """Mock for pkg_resources.iter_entry_points."""
    def iter_entry_points(name):
        for ep in eps:
            yield ep
    return iter_entry_points


def test_version():
    """Test version import."""
    from invenio_config import __version__
    assert __version__


def test_module():
    """Test module."""
    app = Flask('testapp')

    class Config(object):
        TESTVAR = True

    assert not app.config.get('TESTVAR', False)
    InvenioConfigModule(app, module=Config)
    assert app.config.get('TESTVAR', False)


@patch('pkg_resources.iter_entry_points', _mock_ep([ConfigEP(TESTVAR=True)]))
def test_entry_point():
    """Test entry point."""
    app = Flask('testapp')

    assert not app.config.get('TESTVAR', False)
    InvenioConfigEntryPointModule(app)
    assert app.config.get('TESTVAR', False)


def test_folder():
    """Test instance folder loading."""
    tmppath = tempfile.mkdtemp()
    try:
        # Write config into instance folder.
        with open(join(tmppath, 'testapp.cfg'), 'w') as f:
            f.write("TESTVAR = True\n")

        app = Flask(
            'testapp', instance_path=tmppath, instance_relative_config=True)
        assert not app.config.get('TESTVAR', False)
        InvenioConfigInstanceFolder(app=app)
        assert app.config.get('TESTVAR', False)
    finally:
        shutil.rmtree(tmppath)


def test_default():
    """Test instance folder loading."""
    app = Flask('testapp')

    with warnings.catch_warnings(record=True) as w:
        assert len(w) == 0
        InvenioConfigDefault(app)
        assert len(w) == 1
        assert app.config['SECRET_KEY'] == "CHANGE_ME"

    app = Flask('testapp')
    app.config['SECRET_KEY'] = "thisisasecret"

    with warnings.catch_warnings(record=True) as w:
        assert len(w) == 0
        InvenioConfigDefault(app)
        assert len(w) == 0


def test_env():
    """Test loading from environment variables."""
    app = Flask('testapp')
    InvenioConfigEnvironment(app, prefix="MYPREFIX_")
    assert not app.config.get('TESTVAR', False)

    os.environ["MYPREFIX_TESTVAR"] = "True"
    os.environ["MYPREFIX_JUSTASTRING"] = "This is just a string"
    InvenioConfigEnvironment(app, prefix="MYPREFIX_")
    assert app.config.get('TESTVAR') is True
    assert app.config.get('JUSTASTRING') == "This is just a string"


@patch('pkg_resources.iter_entry_points', _mock_ep([
    ConfigEP(EP='ep', MODULE='ep', FOLDER='ep', KWARGS='ep', ENV='ep')]))
def test_conf_loader_factory():
    """Test the conf factory."""
    tmppath = tempfile.mkdtemp()
    try:
        app = Flask('testapp')

        # Module configuration
        class Config(object):
            MODULE = 'module'
            FOLDER = 'module'
            KWARGS = 'module'
            ENV = 'module'

        # Instance path configuration
        with open(join(tmppath, 'testapp.cfg'), 'w') as f:
            f.write("FOLDER = 'folder'\n")
            f.write("KWARGS = 'folder'\n")
            f.write("ENV = 'folder'\n")

        # Keyword arguments configuration
        kwargs = dict(KWARGS='kwargs', ENV='kwargs')

        # Environment configuraiton
        os.environ['APREFIX_ENV'] = 'env'

        # Create conf loader
        conf_loader = create_config_loader(Config, env_prefix="APREFIX")
        app = Flask(
            'testapp', instance_path=tmppath, instance_relative_config=True)
        conf_loader(app, **kwargs)

        # Test correct overwriting of values.
        assert app.config['EP'] == 'ep'
        assert app.config['MODULE'] == 'module'
        assert app.config['FOLDER'] == 'folder'
        assert app.config['KWARGS'] == 'kwargs'
        assert app.config['ENV'] == 'env'
    finally:
        shutil.rmtree(tmppath)
