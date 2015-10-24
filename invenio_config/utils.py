# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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
from .env import InvenioConfigEnvironment
from .folder import InvenioConfigInstanceFolder
from .module import InvenioConfigModule


def default_conf_loader(config, env_prefix='APP'):
    """Default configuration loader."""
    def _conf_loader(app, **kwargs_config):
        if config:
            InvenioConfigModule(app=app, module=config)
        InvenioConfigInstanceFolder(app=app)
        app.config.update(**kwargs_config)
        InvenioConfigEnvironment(app=app, prefix='{0}_'.format(env_prefix))
        InvenioConfigDefault(app=app)

    return _conf_loader
