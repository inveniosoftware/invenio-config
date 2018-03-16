# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio default configuration."""

from __future__ import absolute_import, print_function

import warnings


class InvenioConfigDefault(object):
    """Load configuration from module.

    .. versionadded:: 1.0.0
    """

    def __init__(self, app=None):
        """Initialize extension."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize Flask application."""
        # Ensure SECRET_KEY is set.
        SECRET_KEY = app.config.get('SECRET_KEY')

        if SECRET_KEY is None:
            app.config['SECRET_KEY'] = 'CHANGE_ME'
            warnings.warn(
                'Set configuration variable SECRET_KEY with random string',
                UserWarning)
