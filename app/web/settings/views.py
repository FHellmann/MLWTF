#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import render_template

from . import settings


@settings.route('/')
def index():
    """
    Render the settings template on the / route
    """
    return render_template('settings/index.html', title="Settings")


@settings.route('/rf_devices')
def rf_devices():
    """
    Render the rf-device template on the /rf_devices route
    """
    return render_template('settings/rf_devices.html', title="Settings")


@settings.route('/setup_assistant')
def setup_assistant():
    """
    Render the setup assistant on the /setup_assistant route
    """
    return render_template('settings/setup_assistant.html', title="Setup Assistant")
