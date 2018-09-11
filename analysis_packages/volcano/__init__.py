"""Volcano plot module.

This module shows what features differ between a
particular metadata category and the rest of this group.

These differences proceed on two axes, the mean log fold change
between the selected category and the background, and the
negative log of the p-value of the difference.

Since p-value is partly based on the magnitude of the difference
this creates a plot that looks vaguely like a volcano exploding.
Points on the top right and left are likely to be both signfiicant
and testable.
"""

from .modules import VolcanoAnalysisModule
