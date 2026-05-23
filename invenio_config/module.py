# SPDX-FileCopyrightText: 2015-2018 CERN.
# SPDX-FileCopyrightText: 2024 KTH Royal Institute of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module configuration."""


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
