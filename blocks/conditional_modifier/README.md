ConditionalModifier
===================
Adds a new new field, *title*, to input signals. The value of the attribute is determined by the *lookup* parameter. *lookup* is a list of formula/value pairs. In order, the *formula* of *lookup* are evaluated and when an evaluation is *True*, the *value* is assigned to the signal attribute *title*. If multiple formulas match, the first value is the one that is assigned to the signal.

Properties
----------
- **exclude**: Whether to exclude existing fields on incoming signals when creating an output signal.
- **fields**: Fields to add onto the incoming signal.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: One signal for every incoming signal, modified according to 'fields' and 'exclude'.

Commands
--------
None

