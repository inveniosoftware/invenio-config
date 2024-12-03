# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2018 CERN.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio entry point module configuration."""


from operator import attrgetter

import pkg_resources


class InvenioConfigEntryPointModule(object):
    """Load configuration from module defined by entry point.

    Configurations are loaded in alphabetical ascending order, meaning that an
    entry point named ``00_name`` will be loaded first and an entry point named
    ``10_name`` will be loaded as last. This ensures that configurations
    defined in ``10_name`` app override configurations defined in ``00_name``
    app.

    .. versionadded:: 1.0.0
    """

    def __init__(self, app=None, entry_point_group="invenio_config.module"):
        """Initialize extension."""
        self.entry_point_group = entry_point_group
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize Flask application."""
        if self.entry_point_group:
            eps = sorted(
                pkg_resources.iter_entry_points(self.entry_point_group),
                key=attrgetter("name"),
            )
            for ep in eps:
                app.logger.debug("Loading config for entry point {}".format(ep))
                app.config.from_object(ep.load())
