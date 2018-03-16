#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging

import time
import threading
from datetime import datetime

from attr import s, ib
from attr.validators import instance_of

_LOGGER = logging.getLogger(__name__)


@s(frozen=True)
class SchedulerTask(object):
    name = ib(validator=instance_of(str), type=str)
    function = ib()
    interval = ib(validator=instance_of(float), type=float, default=1.0)
    delay = ib(validator=instance_of(float), type=float, default=0.0)


class Scheduler(object):
    """
    The scheduler is a singleton instance
    """

    class __Scheduler(object):
        def __init__(self):
            self.last_exec = {}
            self.tasks = []
            self.runs = False
            self.terminate = False

    instance = None

    def __init__(self):
        if not Scheduler.instance:
            Scheduler.instance = Scheduler.__Scheduler()

    def register_task(self, task: SchedulerTask):
        self.instance.tasks.append(task)

    def start(self):
        if not self.instance.runs:
            self.instance.runs = True
            threading.Thread(target=self._run).start()

    def stop(self):
        self.instance.terminate = True

    def _run(self):
        _LOGGER.info("Scheduler started")

        init_timestamp = datetime.utcnow()

        while not self.instance.terminate:
            for task in self.instance.tasks:
                self._run_task(init_timestamp, task.name, task.interval, task.delay, task.function)

            time.sleep(0.01)

        self.instance.runs = False

        _LOGGER.info("Scheduler terminated")

    def _run_task(self, start_time: datetime, name: str, interval: float, delay: float, lambda_function):
        first_run = not (name in self.instance.last_exec)
        if (first_run and self.is_active(start_time, delay)) or \
                (not first_run and self.is_active(self.instance.last_exec[name], interval)):
            _LOGGER.info("Scheduler execute task: " + name)
            lambda_function()
            self.instance.last_exec[name] = datetime.utcnow()

    @staticmethod
    def is_active(old_datetime: datetime, interval: float):
        return (datetime.utcnow() - old_datetime).total_seconds() - interval >= 0


scheduler = Scheduler()
