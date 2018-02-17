#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import render_template

from . import home


@home.route('/')
def index():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Home")
