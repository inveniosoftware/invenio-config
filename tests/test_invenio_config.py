# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Simple tests."""

import os
import shutil
import tempfile
import warnings
from os.path import join

from flask import Flask
from mock import patch
from pkg_resources import EntryPoint

from invenio_config import (
    InvenioConfigDefault,
    InvenioConfigEntryPointModule,
    InvenioConfigEnvironment,
    InvenioConfigInstanceFolder,
    InvenioConfigModule,
    create_config_loader,
)
from invenio_config.default import ALLOWED_HTML_ATTRS, ALLOWED_HTML_TAGS


class ConfigEP(EntryPoint):
    """Mocking of entrypoint."""

    def __init__(self, name=None, module_name=None, **kwargs):
        """Save keyword arguments as config."""
        self.name = name
        self.module_name = module_name
        self.kwargs = kwargs

    def __str__(self):
        """Mock __str__ method."""
        return self.name or ""

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
    app = Flask("testapp")

    class Config(object):
        TESTVAR = True

    assert not app.config.get("TESTVAR", False)
    InvenioConfigModule(app, module=Config)
    assert app.config.get("TESTVAR", False)


@patch("pkg_resources.iter_entry_points", _mock_ep([ConfigEP(TESTVAR=True)]))
def test_entry_point():
    """Test entry point."""
    app = Flask("testapp")

    assert not app.config.get("TESTVAR", False)
    InvenioConfigEntryPointModule(app)
    assert app.config.get("TESTVAR", False)


UNSORTED_ENTRY_POINTS = [
    ConfigEP(name="20_app", module_name="last_app.config", TESTVAR="last"),
    ConfigEP(name="00_app", module_name="first_app.config", TESTVAR="first"),
    ConfigEP(name="10_app", module_name="middle_app.config", TESTVAR="middle"),
]


@patch("pkg_resources.iter_entry_points", _mock_ep(UNSORTED_ENTRY_POINTS))
def test_entry_points_loading_order():
    """Test that entry points are loaded alphabetically ordered."""
    app = Flask("testapp")

    InvenioConfigEntryPointModule(app)
    assert app.config["TESTVAR"] == "last"


def test_folder():
    """Test instance folder loading."""
    tmppath = tempfile.mkdtemp()
    try:
        # Write config into instance folder.
        with open(join(tmppath, "testapp.cfg"), "w") as f:
            f.write("TESTVAR = True\n")

        app = Flask("testapp", instance_path=tmppath, instance_relative_config=True)
        assert not app.config.get("TESTVAR", False)
        InvenioConfigInstanceFolder(app=app)
        assert app.config.get("TESTVAR", False)
    finally:
        shutil.rmtree(tmppath)


def test_default():
    """Test instance folder loading."""
    app = Flask("testapp")

    with warnings.catch_warnings(record=True) as w:
        assert len(w) == 0
        InvenioConfigDefault(app)
        assert len(w) == 1
        assert app.config["SECRET_KEY"] == "CHANGE_ME"

    app = Flask("testapp")
    app.config["SECRET_KEY"] = "thisisasecret"

    with warnings.catch_warnings(record=True) as w:
        assert len(w) == 0
        InvenioConfigDefault(app)
        assert len(w) == 0


def test_default_allowed_html_tags():
    """Test instance folder loading."""
    app = Flask("testapp")

    InvenioConfigDefault(app)
    assert app.config["ALLOWED_HTML_TAGS"] == ALLOWED_HTML_TAGS

    app.config["ALLOWED_HTML_TAGS"] = ["a"]
    InvenioConfigDefault(app)
    assert app.config["ALLOWED_HTML_TAGS"] == ["a"]


def test_default_allowed_html_attrs():
    """Test instance folder loading."""
    app = Flask("testapp")

    InvenioConfigDefault(app)
    assert app.config["ALLOWED_HTML_ATTRS"] == ALLOWED_HTML_ATTRS

    app.config["ALLOWED_HTML_ATTRS"] = "test override"
    InvenioConfigDefault(app)
    assert app.config["ALLOWED_HTML_ATTRS"] == "test override"


def test_env():
    """Test loading from environment variables."""
    app = Flask("testapp")
    InvenioConfigEnvironment(app, prefix="MYPREFIX_")
    assert not app.config.get("TESTVAR", False)

    os.environ["MYPREFIX_TESTVAR"] = "True"
    os.environ["MYPREFIX_JUSTASTRING"] = "This is just a string"
    os.environ["MYPREFIX_COMPLEX_DICT"] = (
        "{'complex': {'python': 'dict'}, 'with': ['list', 'and', 1234]}"
    )
    InvenioConfigEnvironment(app, prefix="MYPREFIX_")
    assert app.config.get("TESTVAR") is True
    assert app.config.get("JUSTASTRING") == "This is just a string"
    assert app.config.get("COMPLEX_DICT") == {
        "complex": {"python": "dict"},
        "with": ["list", "and", 1234],
    }


@patch(
    "pkg_resources.iter_entry_points",
    _mock_ep([ConfigEP(EP="ep", MODULE="ep", FOLDER="ep", KWARGS="ep", ENV="ep")]),
)
def test_conf_loader_factory():
    """Test the conf factory."""
    tmppath = tempfile.mkdtemp()
    try:
        app = Flask("testapp")

        # Module configuration
        class Config(object):
            MODULE = "module"
            FOLDER = "module"
            KWARGS = "module"
            ENV = "module"

        # Instance path configuration
        with open(join(tmppath, "testapp.cfg"), "w") as f:
            f.write("FOLDER = 'folder'\n")
            f.write("KWARGS = 'folder'\n")
            f.write("ENV = 'folder'\n")

        # Keyword arguments configuration
        kwargs = dict(KWARGS="kwargs", ENV="kwargs")

        # Environment configuraiton
        os.environ["APREFIX_ENV"] = "env"

        # Create conf loader
        conf_loader = create_config_loader(Config, env_prefix="APREFIX")
        app = Flask("testapp", instance_path=tmppath, instance_relative_config=True)
        conf_loader(app, **kwargs)

        # Test correct overwriting of values.
        assert app.config["EP"] == "ep"
        assert app.config["MODULE"] == "module"
        assert app.config["FOLDER"] == "folder"
        assert app.config["KWARGS"] == "kwargs"
        assert app.config["ENV"] == "env"
    finally:
        shutil.rmtree(tmppath)
