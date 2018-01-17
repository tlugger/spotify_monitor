Debounce
========
After a signal flows through the block, filter out following signals for [interval] seconds.

Properties
----------
- **group_by**: The value by which signals are grouped.
- **interval**: Amount of time to wait before allowing another signal in a matching group.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: The first signal for each group, every interval.

Commands
--------
- **groups**: Display the existing groups.

Dependencies
------------
None