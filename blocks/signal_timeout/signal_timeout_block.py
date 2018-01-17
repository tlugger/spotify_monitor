from collections import defaultdict
from threading import Event, Lock

from nio.block.base import Block
from nio.properties import TimeDeltaProperty, BoolProperty, ListProperty, \
    PropertyHolder, VersionProperty
from nio.modules.scheduler import Job
from nio.block.mixins import GroupBy, Persistence


class Interval(PropertyHolder):
    interval = TimeDeltaProperty(title='Interval', default={})
    repeatable = BoolProperty(title='Repeatable',
                              default=False)


class SignalTimeout(Persistence, GroupBy, Block):

    """ Notifies a timeout signal when no signals have been processed
    by this block for the defined intervals.

    The timeout signal is the last signal that entered the block, with the
    added attributes *timeout* and *group*.

    Properties:
        group_by (expression): The value by which signals are grouped.
        intervals (list):
            interval (timedelta): Interval to notifiy timeout signal.
            repeatable (bool): If true, notifies every interval without a sig.

    """

    intervals = ListProperty(Interval, title='Timeout Intervals', default=[])
    version = VersionProperty('0.1.0')

    def __init__(self):
        super().__init__()
        self._jobs = defaultdict(dict)
        self._jobs_locks = defaultdict(Lock)
        self._repeatable_jobs = defaultdict(dict)
        self._persistence_scheduled = Event()

    def persisted_values(self):
        """Use persistence mixin"""
        return ["_repeatable_jobs"]

    def start(self):
        super().start()
        # Schedule persisted jobs
        for key, intervals in self._repeatable_jobs.items():
            for interval, job in intervals.items():
                self._schedule_timeout_job(job, key, interval, True)
        self._persistence_scheduled.set()

    def process_signals(self, signals):
        self._persistence_scheduled.wait(1)
        self.for_each_group(self.process_group, signals)

    def process_group(self, signals, key):
        if len(signals) == 0:
            # No signals actually came through, do nothing
            self.logger.debug("No signals detected for {}".format(key))
            return
        with self._jobs_locks[key]:
            # Cancel any existing timeout jobs, then reschedule them
            self._cancel_timeout_jobs(key)
            for interval in self.intervals():
                self._schedule_timeout_job(
                    signals[-1],
                    key,
                    interval.interval(signals[-1]),
                    interval.repeatable(signals[-1]))

    def _cancel_timeout_jobs(self, key):
        """ Cancel all the timeouts for a given group """
        self.logger.debug("Cancelling jobs for {}".format(key))
        for job in self._jobs[key].values():
            job.cancel()
        if key in self._repeatable_jobs:
            del self._repeatable_jobs[key]

    def _schedule_timeout_job(self, signal, key, interval, repeatable):
        self.logger.debug("Scheduling new timeout job for group {}, "
                          "interval={} repeatable={}".format(
                                key, interval, repeatable))
        self._jobs[key][interval] = Job(
            self._timeout_job, interval, repeatable, signal, key, interval)
        if repeatable:
            self._repeatable_jobs[key][interval] = signal

    def _timeout_job(self, signal, key, interval):
        """ Triggered when an interval times out """
        signal.timeout = interval
        signal.group = key
        self.notify_signals([signal])
