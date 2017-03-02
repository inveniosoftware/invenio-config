# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016, 2017 CERN.
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

"""Default configuration loader usable by e.g. Invenio-Base."""

from __future__ import absolute_import, print_function

from .default import InvenioConfigDefault
from .entrypoint import InvenioConfigEntryPointModule
from .env import InvenioConfigEnvironment
from .folder import InvenioConfigInstanceFolder
from .module import InvenioConfigModule


def create_config_loader(config=None, env_prefix='APP'):
    """Create a default configuration loader.

    A configuration loader takes a Flask application and keyword arguments and
    updates the Flask application's configuration as it sees fit.

    This default configuration loader will load configuration in the following
    order:

        1. Load configuration from ``invenio_config.module`` entry point group.
        2. Load configuration from ``config`` module if provided as argument.
        3. Load configuration from the instance folder:
           ``<app.instance_path>/<app.name>.cfg``.
        4. Load configuration keyword arguments provided.
        5. Load configuration from environment variables with the prefix
           ``env_prefix``.

    If no secret key has been set a warning will be issued.

    :param config: Either an import string to a module with configuration or
        alternatively the module itself.
    :param env_prefix: Environment variable prefix to import configuration
        from.
    :return: A callable with the method signature
        ``config_loader(app, **kwargs)``.

    .. versionadded:: 1.0.0
    """
    def _config_loader(app, **kwargs_config):
        InvenioConfigEntryPointModule(app=app)
        if config:
            InvenioConfigModule(app=app, module=config)
        InvenioConfigInstanceFolder(app=app)
        app.config.update(**kwargs_config)
        InvenioConfigEnvironment(app=app, prefix='{0}_'.format(env_prefix))
        InvenioConfigDefault(app=app)

    return _config_loader


def create_conf_loader(*args, **kwargs):  # pragma: no cover
    """Create a default configuration loader.

    .. deprecated:: 1.0.0b1
       Use :func:`create_config_loader` instead. This function will be removed
       in version 1.0.1.
    """
    import warnings
    warnings.warn(
        '"create_conf_loader" has been renamed to "create_config_loader".',
        DeprecationWarning
    )
    return create_config_loader(*args, **kwargs)
