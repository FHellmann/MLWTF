from flask import render_template, request, redirect, url_for

from . import settings
from ..core.rf.rf_controller import RfController

rf_controller = RfController()


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
    return render_template('settings/rf_devices.html', title="Settings", devices=rf_controller.get_signals())


@settings.route('/rf_devices/test', methods=['POST'])
def rf_device_test():
    """
    Send the specific signal and return same site
    """
    rf_signal = request.form['rf_signal']
    rf_controller.send(rf_signal)
    return redirect(url_for('settings.rf_devices'))
