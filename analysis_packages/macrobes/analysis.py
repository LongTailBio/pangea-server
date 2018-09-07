"""Wrangler for Macrobe Directory results."""

from pandas import DataFrame

from tool_packages.macrobes import MacrobeResultModule


def collate_macrobes(samples, reverse):
    """Group a macrobes from a set of samples."""
    sample_dict = {}
    for sample in samples:
        sample_name = sample['name']
        sample_dict[sample_name] = {
            macrobe_name: val['rpkm']
            for macrobe_name, val in sample[MacrobeResultModule.name()]['macrobes'].items()
        }
    sample_tbl = DataFrame.from_dict(sample_dict, orient='index').fillna(0)
    if len(samples) > 1:
        sample_tbl = (sample_tbl - sample_tbl.mean()) / sample_tbl.std(ddof=0)  # z score normalize
    if reverse:
        sample_dict = {'samples': sample_tbl.to_dict()}
    else:
        sample_dict = {'samples': sample_tbl.to_dict(orient='index')}
    return sample_dict


def processor(*sample_data):
    """Handle Macrobe Directory component calculations."""
    samples = list(sample_data)
    reverse = len(samples) > 1
    return collate_macrobes(samples, reverse)
