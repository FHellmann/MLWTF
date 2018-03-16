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


class Scheduler:
    """
    The scheduler is a singleton instance
    """

    def __init__(self):
        self.last_exec = {}
        self.tasks = {}
        self.runs = False
        self.terminate = False
        self.start()

    def register_task(self, task: SchedulerTask):
        self.tasks[task.name] = task

    def start(self):
        if not self.runs:
            self.runs = True
            threading.Thread(target=self._run).start()

    def stop(self):
        self.terminate = True

    def _run(self):
        _LOGGER.info("Scheduler started")

        init_timestamp = datetime.utcnow()

        while not self.terminate:
            for task_name, task in self.tasks.items():
                self._run_task(init_timestamp, task_name, task.interval, task.delay, task.function)

            time.sleep(0.01)

        self.runs = False

        _LOGGER.info("Scheduler terminated")

    def _run_task(self, start_time: datetime, name: str, interval: float, delay: float, task_function):
        first_run = not (name in self.last_exec)
        if (first_run and self.is_active(start_time, delay)) or \
                (not first_run and self.is_active(self.last_exec[name], interval)):
            _LOGGER.info("Scheduler execute task: " + name)
            self.last_exec[name] = datetime.utcnow()
            task_function()

    @staticmethod
    def is_active(old_datetime: datetime, interval: float):
        return (datetime.utcnow() - old_datetime).total_seconds() - interval >= 0


scheduler = Scheduler()
