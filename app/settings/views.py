from flask import render_template

from . import settings
from ..core.rf.rf_controller import RfController

rf_controller = RfController()


@settings.route('/')
def index():
    """
    Render the settings template on the / route
    """
    return render_template('settings/index.html', title="Settings")


@settings.route('/rfdevices')
def rf_devices():
    """
    Render the rf-device template on the /rfdevices route
    """
    print(rf_controller.get_signals())
    return render_template('settings/rfdevices.html', title="Settings", devices=rf_controller.get_signals())
