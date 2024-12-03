# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2024 CERN.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio configuration loader.

Invenio-Config is a *base package* of the Invenio digital library framework.
It is usually installed automatically as a dependency. It should facilitate
configuration loading from various sources to an application instance.

The following configuration loaders exists:

- :py:data:`invenio_config.default.InvenioConfigDefault` - ensure required
  configuration values are set.
- :py:data:`invenio_config.module.InvenioConfigModule` - for loading
  configuration from a Python module.
- :py:data:`invenio_config.entrypoint.InvenioConfigEntryPointModule` - for
  loading configuration from a Python module specified by an entry point (by
  default ``invenio_config.module``).
- :py:data:`invenio_config.folder.InvenioConfigInstanceFolder` - for loading
  configuration from ``cfg`` file in an instance folder.
- :py:data:`invenio_config.env.InvenioConfigEnvironment` - for loading
  configuration from environment variables with defined prefix (e.g.
  ``INVENIO_SECRET_KEY``).

It also includes configuration loader factory that it is used to merge these
sources in predefined order ensuring correct behavior in common scenarios.

Initialization
--------------
Following example needs a writable instance folder, hence we start by creating
a temporary directory.

>>> import tempfile
>>> tmppath = tempfile.mkdtemp()

.. testcode::
   :hide:

   import atexit
   import shutil
   atexit.register(lambda: shutil.rmtree(tmppath))

Now we can create a Flask application:

>>> from flask import Flask
>>> app = Flask('myapp', instance_path=tmppath, instance_relative_config=True)

Loaders
-------
You can check default configuration values in newly created ``app``.

>>> 'DEBUG' in app.config
True
>>> app.config.get('SECRET_KEY') is None
True

Default
~~~~~~~
The default configuration loader makes sure that the required configuration
values are always loaded. You should call it **after** all configuration
loaders have been already called.

The following default configuration values exist:

- :py:data:`SECRET_KEY` - A secret key that will be used for securely signing
  the session cookie and can be used for any other security related needs.
- :py:data:`~invenio_config.default.ALLOWED_HTML_TAGS` - allowed tags used for
  html sanitizing by bleach.
- :py:data:`~invenio_config.default.ALLOWED_HTML_ATTRS` - allowed attributes
  used for html sanitizing by bleach.

The default configuration loader will warn if the ``SECRET_KEY`` is not
defined:

>>> import warnings
>>> from invenio_config import InvenioConfigDefault
>>> with warnings.catch_warnings(record=True) as w:
...     config_default = InvenioConfigDefault(app=app)
...     assert len(w) == 1
>>> app.config['SECRET_KEY']
'CHANGE_ME'

Module
~~~~~~
The module loader accepts an object and proxies the call to
:meth:`flask.Config.from_object`.

Here is an example of a configuration object:

>>> class Config:
...     EXAMPLE = 'module'
>>> from invenio_config import InvenioConfigModule
>>> config_module = InvenioConfigModule(app=app, module=Config)
>>> app.config['EXAMPLE']
'module'

Entry point
~~~~~~~~~~~
The entry point loader works similar to the module loader, it just loads the
config module from the entry point ``invenio_config.module``:

>>> from invenio_config import InvenioConfigEntryPointModule
>>> config_ep = InvenioConfigEntryPointModule(app=app)

Instance Folder
~~~~~~~~~~~~~~~
The runtime configuration should be stored in a separate file, ideally located
outiside the actual application package. The configuration files are handled
as Python files where only variables in uppercase are stored in the application
config.

>>> import os
>>> from invenio_config import InvenioConfigInstanceFolder
>>> with open(os.path.join(tmppath, 'myapp.cfg'), 'w') as f:
...     result = f.write("EXAMPLE = 'instance folder'")
>>> config_instance_folder = InvenioConfigInstanceFolder(app=app)
>>> app.config['EXAMPLE']
'instance folder'

Environment
~~~~~~~~~~~
Using environment variables is very handy when it comes to configuring
connections to services like database, Redis server, RabbitMQ, etc. used via
containers (e.g. Docker). In order to protect your application from reading
environment variables set by the system or other applications, you should
define a variable prefix used by the loader.

>>> os.environ['MYAPP_EXAMPLE'] = 'environment'
>>> from invenio_config import InvenioConfigEnvironment
>>> config_environment = InvenioConfigEnvironment(app=app, prefix='MYAPP_')
>>> app.config['EXAMPLE']
'environment'

You can also set more complex Python literal variables (e.g. dictionaries or
lists):

>>> os.environ['MYAPP_COMPLEX'] = "{'items': [{'num': 42}, {'foo': 'bar'}]}"
>>> # ...or export MYAPP_COMPLEX="{'items': [{'num': 42}, {'foo': 'bar'}]}"
>>> config_environment = InvenioConfigEnvironment(app=app, prefix='MYAPP_')
>>> app.config['COMPLEX']
{'items': [{'num': 42}, {'foo': 'bar'}]}


Factory Pattern
---------------
The Invenio-Config comes with an opinionated way of loading configuration,
that combines loaders in predictable way. You can use
:func:`invenio_config.utils.create_config_loader` if you would like to:

  1. Load configuration from ``invenio_config.module`` entry point group.
  2. Load configuration from ``config`` module if provided as argument.
  3. Load configuration from the instance folder:
     ``<app.instance_path>/<app.name>.cfg``.
  4. Load configuration keyword arguments provided.
  5. Load configuration from environment variables with the prefix
     ``env_prefix``.

>>> from invenio_config import create_config_loader
>>> app = Flask('myapp', instance_path=tmppath, instance_relative_config=True)
>>> config_loader = create_config_loader(config=Config, env_prefix='MYAPP')
>>> config_loader(app=app, MYARG='config loader')
>>> app.config['EXAMPLE']
'environment'
>>> app.config['MYARG']
'config loader'

"""

from .default import InvenioConfigDefault
from .entrypoint import InvenioConfigEntryPointModule
from .env import InvenioConfigEnvironment
from .folder import InvenioConfigInstanceFolder
from .module import InvenioConfigModule
from .utils import create_conf_loader, create_config_loader

__version__ = "1.0.4"

__all__ = (
    "__version__",
    "InvenioConfigDefault",
    "InvenioConfigEntryPointModule",
    "InvenioConfigEnvironment",
    "InvenioConfigInstanceFolder",
    "InvenioConfigModule",
    "create_conf_loader",
    "create_config_loader",
)
