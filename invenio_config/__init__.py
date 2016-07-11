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

"""Invenio configuration loader.

Invenio-Config is a *base package* of the Invenio digital library framework.
It is usually installed automatically as a dependency. It should facilitate
configuration loading from various sources to an application instance.

There are following configuration loaders:

- `InvenioConfigDefault` - ensure required configuration values are set.
- `InvenioConfigModule` - for loading configuration from a module.
- `InvenioConfigInstanceFolder` - for loading configuration from ``cfg`` file
  in folder.
- `InvenioConfigEnvironment` - for loading configuration from environment
  variables with defined prefix (e.g. ``INVENIO_SECRET_KEY``).

It also includes configuration loader factory that it is used to merge these
sources in predefined order ensuring correct behavior in common scenarios.

Initialization
--------------
Following example needs a writable instance folder, hence we start by creating
a temporary directory.

>>> import tempfile
>>> tmppath = tempfile.mkdtemp()

In order to make sure that there are no files left in case of exception,
lets register a clean up function that removes the temporary directory.

>>> import atexit
>>> import shutil
>>> atexit.register(lambda: shutil.rmtree(tmppath))
<function ...>

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
values are always loaded. You should call it after **all** configuration
loaders have been already called.

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

Instance Folder
~~~~~~~~~~~~~~~
The runtime configuration should stored in a separate file, ideally located
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
environment variables set by system or other application, you should define
variable prefix used by loader.

>>> os.environ['MYAPP_EXAMPLE'] = 'environment'
>>> from invenio_config import InvenioConfigEnvironment
>>> config_environment = InvenioConfigEnvironment(app=app, prefix='MYAPP_')
>>> app.config['EXAMPLE']
'environment'

Factory Pattern
---------------
The Invenio-Config comes with an opinionated way of loading configuration,
that combines loaders in predictable way. You can use
:func:`invenio_config.utils.create_config_loader` if you would like to:

  1. Load configuration from ``config`` module if provided as argument.
  2. Load configuration from the instance folder:
     ``<app.instance_path>/<app.name>.cfg``.
  3. Load configuration keyword arguments provided.
  4. Load configuration from environment variables with the prefix
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

from __future__ import absolute_import, print_function

from .default import InvenioConfigDefault
from .env import InvenioConfigEnvironment
from .folder import InvenioConfigInstanceFolder
from .module import InvenioConfigModule
from .utils import create_conf_loader, create_config_loader
from .version import __version__

__all__ = (
    '__version__',
    'InvenioConfigDefault',
    'InvenioConfigEnvironment',
    'InvenioConfigInstanceFolder',
    'InvenioConfigModule',
    'create_conf_loader',
    'create_config_loader',
)
