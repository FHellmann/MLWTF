from flask import render_template

from . import home


@home.route('/')
def index():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")
