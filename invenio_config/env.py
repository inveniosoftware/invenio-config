# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2024-2025 KTH Royal Institute of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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


def _get_env_var(prefix: str, keys: list) -> dict:
    """Retrieve environment variables with a given prefix."""
    return {k: os.environ.get(f"{prefix}_{k.upper()}") for k in keys}


def _check_prefix(prefix: str) -> str:
    """Check if prefix ends with an underscore and remove it."""
    if not prefix:
        return "INVENIO"
    if prefix.endswith("_"):
        prefix = prefix[:-1]
    return prefix


def build_db_uri(prefix="INVENIO"):
    """
    Build database URI from environment variables or use default.

    Priority order:
    1. INVENIO_SQLALCHEMY_DATABASE_URI
    2. SQLALCHEMY_DATABASE_URI
    3. INVENIO_DB_* specific environment variables
    4. Default URI

    Note: For option 3, to assert that the INVENIO_DB_* settings take effect,
    you need to set SQLALCHEMY_DATABASE_URI="" in your environment.
    """
    prefix = _check_prefix(prefix)
    default_uri = "postgresql+psycopg2://invenio-app-rdm:invenio-app-rdm@localhost/invenio-app-rdm"

    for key in [f"{prefix}_SQLALCHEMY_DATABASE_URI", "SQLALCHEMY_DATABASE_URI"]:
        if uri := os.environ.get(key):
            return uri

    db_params = _get_env_var(
        f"{prefix}_DB", ["user", "password", "host", "port", "name", "protocol"]
    )
    if all(db_params.values()):
        uri = f"{db_params['protocol']}://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['name']}"
        return uri

    return default_uri


def build_broker_url(prefix="INVENIO"):
    """
    Build broker URL from environment variables or use default.

    Priority order:
    1. INVENIO_BROKER_URL
    2. BROKER_URL
    3. INVENIO_AMQP_BROKER_* specific environment variables
    4. Default URL
    Note: see: https://docs.celeryq.dev/en/stable/userguide/configuration.html#new-lowercase-settings
    """
    prefix = _check_prefix(prefix)
    default_url = "amqp://guest:guest@localhost:5672/"

    for key in [f"{prefix}_BROKER_URL", "BROKER_URL"]:
        if broker_url := os.environ.get(key):
            return broker_url

    broker_params = _get_env_var(
        f"{prefix}_AMQP_BROKER", ["user", "password", "host", "port", "protocol"]
    )
    if all(broker_params.values()):
        broker_env_var = f"{prefix}_AMQP_BROKER_VHOST"
        vhost = f"{os.environ.get(broker_env_var).removeprefix('/')}"
        broker_url = f"{broker_params['protocol']}://{broker_params['user']}:{broker_params['password']}@{broker_params['host']}:{broker_params['port']}/{vhost}"
        return broker_url
    return default_url


def build_redis_url(db=None, prefix="INVENIO"):
    """
    Build Redis URL from environment variables or use default.

    Priority order:
    1. INVENIO_CACHE_REDIS_URL
    2. CACHE_REDIS_URL
    3. INVENIO_KV_CACHE_* specific environment variables
    4. Default URL
    """
    prefix = _check_prefix(prefix)
    db = db if db is not None else 0
    default_url = f"redis://localhost:6379/{db}"

    for key in [f"{prefix}_CACHE_REDIS_URL", "CACHE_REDIS_URL"]:
        if cache_url := os.environ.get(key):
            if cache_url.startswith(("redis://", "rediss://", "unix://")):
                return cache_url

    redis_params = _get_env_var(
        f"{prefix}_KV_CACHE", ["host", "port", "password", "protocol"]
    )

    if redis_params["host"] and redis_params["port"]:
        protocol = redis_params.get("protocol", "redis")
        password = (
            f":{redis_params['password']}@" if redis_params.get("password") else ""
        )
        cache_url = (
            f"{protocol}://{password}{redis_params['host']}:{redis_params['port']}/{db}"
        )
        return cache_url

    return default_url
