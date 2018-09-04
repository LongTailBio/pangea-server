"""Beta Diversity tool module."""

from mongoengine import ValidationError, DictField

from tool_packages.base.models import GroupToolResult


def validate_entry(entry):
    """Validate individual Beta Diversity entry."""
    all_sample_names = entry.keys()
    for sample_name, sub_level in entry.items():
        level_sample_names = sub_level.keys()
        if all_sample_names != level_sample_names:
            message = f'Level {sample_name} did not contain correct sublevel samples.'
            raise ValidationError(message)
        for sub_level_name, value in sub_level.items():
            if not isinstance(value, (int, float)):
                message = (f'Value for [{sample_name}][{sub_level_name}] '
                           '({value}) is not a number!')
                raise ValidationError(message)


class BetaDiversityToolResult(GroupToolResult):  # pylint: disable=too-few-public-methods
    """Beta Diversity result type."""

    # Accept any JSON
    # Data: {<genus>: {<metric>: {<tool>: {<sample_name>: {<sample_name>: <value>}}}}}
    data = mongoDB.DictField(required=True)

    def clean(self):
        """Ensure data blob meets minimum requirements."""
        ranks = self.data
        for metric in ranks.values():
            for tool in metric.values():
                for entry in tool.values():
                    validate_entry(entry)
