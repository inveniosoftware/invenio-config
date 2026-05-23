# SPDX-FileCopyrightText: 2015-2018 CERN.
# SPDX-FileCopyrightText: 2024 KTH Royal Institute of Technology.
# SPDX-License-Identifier: MIT

"""Invenio environment configuration."""

import ast
import os


class InvenioConfigEnvironment(object):
    """Load configuration from environment variables.

    .. versionadded:: 1.0.0
    """

    def __init__(self, app=None, prefix="INVENIO_"):
        """Initialize extension."""
        self.prefix = prefix
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize Flask application."""
        prefix_len = len(self.prefix)
        for varname, value in os.environ.items():
            if not varname.startswith(self.prefix):
                continue

            # Prepare values
            varname = varname[prefix_len:]
            value = value or app.config.get(varname)

            # Evaluate value
            try:
                value = ast.literal_eval(value)
            except (SyntaxError, ValueError):
                pass

            # Set value
            app.config[varname] = value
