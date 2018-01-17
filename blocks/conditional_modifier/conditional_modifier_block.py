from nio.block.base import Block
from nio.signal.base import Signal
from nio.properties import (StringProperty, PropertyHolder, BoolProperty,
                            Property, ListProperty, VersionProperty)


class LookupProperty(PropertyHolder):
    formula = Property(default='{{True}}', title='Formula')
    value = Property(default='value', title='Value')


class SignalField(PropertyHolder):
    title = StringProperty(default='', title="Attribute Title")
    lookup = ListProperty(LookupProperty, title='Lookup', default=[])


class ConditionalModifier(Block):
    """ Conditional Modifier block.

    Adds a new new field, *title*, to input signals. The
    value of the attribute is determined by the *lookup*
    parameter. *lookup* is a list of formula/value pairs.
    In order, the *formula* of *lookup* are evaluated and
    when an evaluation is *True*, the *value* is assigned
    to the signal attribute *title*. If multiple formulas
    match, the first value is the one that is assigned
    to the signal.

    """

    fields = ListProperty(SignalField, title='Fields', default=[])
    exclude = BoolProperty(default=False, title='Exclude existing fields?')
    version = VersionProperty("1.0.0")

    def process_signals(self, signals):
        fresh_signals = []

        for signal in signals:

            # if we are including only the specified fields, create
            # a new, empty signal object
            tmp = Signal() if self.exclude() else signal

            # iterate over the specified fields, evaluating the formula
            # in the context of the original signal
            for field in self.fields():
                value = self._evaluate_lookup(field.lookup(), signal)
                setattr(tmp, field.title(), value)
            # only rebuild the signal list if we're using new objects
            if self.exclude:
                fresh_signals.append(tmp)

        if self.exclude:
            signals = fresh_signals

        self.notify_signals(signals)

    def _evaluate_lookup(self, lookup, signal):
        for lu in lookup:
            value = lu.formula(signal)
            if value:
                return lu.value(signal)
