# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module configuration."""

from __future__ import absolute_import, print_function


class InvenioConfigModule(object):
    """Load configuration from module.

    .. versionadded:: 1.0.0
    """

    def __init__(self, app=None, module=None):
        """Initialize extension."""
        self.module = module
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize Flask application."""
        if self.module:
            app.config.from_object(self.module)
