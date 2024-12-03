# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio default configuration."""

import warnings

#: Allowed tags used for html sanitizing by bleach.
ALLOWED_HTML_TAGS = [
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "br",
    "code",
    "div",
    "table",
    "tbody",
    "td",
    "th",
    "tr",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "i",
    "li",
    "ol",
    "p",
    "pre",
    "span",
    "strike",
    "strong",
    "sub",
    "sup",
    "u",
    "ul",
]

#: Allowed attributes used for html sanitizing by bleach.
ALLOWED_HTML_ATTRS = {
    "*": ["class"],
    "a": ["href", "title", "name", "class", "rel"],
    "abbr": ["title"],
    "acronym": ["title"],
}


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
        SECRET_KEY = app.config.get("SECRET_KEY")

        if SECRET_KEY is None:
            app.config["SECRET_KEY"] = "CHANGE_ME"
            warnings.warn(
                "Set configuration variable SECRET_KEY with random string", UserWarning
            )

        if app.config.get("ALLOWED_HTML_TAGS") is None:
            app.config["ALLOWED_HTML_TAGS"] = ALLOWED_HTML_TAGS

        if app.config.get("ALLOWED_HTML_ATTRS") is None:
            app.config["ALLOWED_HTML_ATTRS"] = ALLOWED_HTML_ATTRS
