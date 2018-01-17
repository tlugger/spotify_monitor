from blink1.blink1 import Blink1 as B1

from nio.properties import (Property, ObjectProperty, PropertyHolder,
                            VersionProperty)
from nio import TerminatorBlock


class Color(PropertyHolder):
    red = Property(title='Red', default='0')
    green = Property(title='Green', default='0')
    blue = Property(title='Blue', default='0')


class Blink1(TerminatorBlock):

    """ Control a blink(1) dongle. """

    fade_milliseconds = Property(title='Time to fade (ms)',
                                 default='1000')
    color = ObjectProperty(Color, title='Color', default=Color())
    version = VersionProperty("1.0.0")

    def __init__(self):
        super().__init__()
        self._blink1 = None

    def configure(self, context):
        super().configure(context)
        self.logger.debug('Connecting to Blink1')
        self._blink1 = B1()
        self.logger.debug('Connected to Blink1')

    def stop(self):
        try:
            self._blink1.close()
        except:
            self.logger.exception('Exception while closing Blink1 connection')
        super().stop()

    def process_signals(self, signals, input_id='default'):
        for signal in signals:
            try:
                fade_milliseconds = int(self.fade_milliseconds(signal))
                red = int(self.color().red(signal))
                green = int(self.color().green(signal))
                blue = int(self.color().blue(signal))
            except:
                self.logger.exception('Failed to evalue fade variables')
                continue
            try:
                self.logger.debug(
                    'Fading to ({}, {}, {}) over {} milliseconds'.format(
                        red, green, blue, fade_milliseconds))
                self._blink1.fade_to_rgb(fade_milliseconds, red, green, blue)
            except:
                self.logger.exception('Failed to fade Blink1')
