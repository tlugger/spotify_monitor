from collections import defaultdict
from datetime import datetime

from nio.block.base import Block
from nio.block.mixins.group_by.group_by import GroupBy
from nio.properties import TimeDeltaProperty, VersionProperty


class Debounce(GroupBy, Block):

    interval = TimeDeltaProperty(title='Debounce Interval',
                                 default={'days': 0, 'seconds': 1,
                                          'microseconds': 0})
    version = VersionProperty('0.1.0')

    def __init__(self):
        super().__init__()
        self._last_emission = defaultdict(lambda: None)

    def process_group_signals(self, signals, group, input_id):
        """Check configured interval and return a signal if valid."""
        now = datetime.utcnow()
        if self._last_emission[group] is None or \
                now - self._last_emission[group] > self.interval(signals[-1]):
            self._last_emission[group] = now
            return signals[:1]
        else:
            return []
