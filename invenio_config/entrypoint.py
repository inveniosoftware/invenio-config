# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio entry point module configuration."""

from __future__ import absolute_import, print_function

import warnings

import pkg_resources


class InvenioConfigEntryPointModule(object):
    """Load configuration from module defined by entry point.

    .. versionadded:: 1.0.0
    """

    def __init__(self, app=None, entry_point_group='invenio_config.module'):
        """Initialize extension."""
        self.entry_point_group = entry_point_group
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize Flask application."""
        if self.entry_point_group:
            for ep in pkg_resources.iter_entry_points(self.entry_point_group):
                app.config.from_object(ep.load())
