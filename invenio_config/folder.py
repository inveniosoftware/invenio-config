# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio instance folder configuration."""


class InvenioConfigInstanceFolder(object):
    """Load configuration from py file in folder.

    If the application have instance relative config then the file will be read
    from the instance folder, otherwise it will be read from the application
    root path.

    More about `instance folders
    <http://flask.pocoo.org/docs/latest/config/#instance-folders>`_.

    .. versionadded:: 1.0.0
    """

    def __init__(self, app=None):
        """Initialize extension."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize Flask application."""
        app.config.from_pyfile("{0}.cfg".format(app.name), silent=True)
