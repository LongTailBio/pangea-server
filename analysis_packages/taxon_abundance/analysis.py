"""Tasks to process Taxon Abundance results."""

import pandas as pd

from tool_packages.kraken import KrakenResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule
from tool_packages.krakenhll import KrakenHLLResultModule

from .exceptions import InvalidRank


TAXA_RANKS = 'kpcofgs'  # kingdom, phylum, classus...


def get_rank(taxa_name):
    """Return a rank code from a taxon ID."""
    rank = taxa_name.strip()[0].lower()
    if rank == 'd':
        rank = 'k'
    if rank not in TAXA_RANKS:
        raise InvalidRank(f'{rank} {taxa_name}')
    return rank


class TaxaFlow():
    """Represent and build Taxon Flow."""

    def __init__(self, samples, tool_name, min_abundance=0.05):
        """Initialize TaxaFlow."""
        self.samples = samples
        self.tool_name = tool_name
        self.min_abundance = min_abundance
        self.links = {}
        self.nodes = {}
        self.taxa_table = self.build_taxa_table(self.tool_name)
        self.graph = self.build_graph(self.taxa_table)

    def build_taxa_table(self, tool_name):
        """Return a scaled taxa table for a given tool."""
        taxa_table = {}
        for sample in self.samples:
            try:
                taxa_table[sample['name']] = sample[tool_name]['taxa']
            except KeyError:
                pass

        taxa_table = pd.DataFrame.from_dict(taxa_table, orient='columns').fillna(0)
        taxa_table = taxa_table.apply(lambda col: col / col.sum(), axis=0)

        return taxa_table.to_dict()

    def upsert_node(self, key, rank, value=100):
        """Update the node table."""
        try:
            self.nodes[key]['value'] += value
        except KeyError:
            display_name = key
            if '__' in display_name:
                display_name = display_name.split('__')[1]
            self.nodes[key] = {
                'id': key,
                'name': display_name,
                'value': value,
                'rank': rank,
            }

    def upsert_link(self, source, target, value):
        """Update the link table."""
        key = f'{source}->{target}'
        try:
            self.links[key]['value'] += value
        except KeyError:
            self.links[key] = {
                'source': source,
                'target': target,
                'value': value,
            }

    def handle_one_taxon(self, sample_name, taxon_name, abundance):
        """Process a single taxon line."""
        taxa_tokens = taxon_name.split('|')

        for prev_taxa, current_taxa in zip([None] + taxa_tokens[:-1], taxa_tokens):
            current_rank = get_rank(current_taxa)

            # Left hand root node: nothing to the left to link to, just update values
            if current_taxa == taxa_tokens[0]:
                self.upsert_node(key=current_taxa, rank=current_rank, value=abundance)
                continue

            # Middling taxa: update value AND link to previous taxa
            self.upsert_node(key=current_taxa, rank=current_rank, value=abundance)
            self.upsert_link(source=prev_taxa, target=current_taxa, value=abundance)

            # Last taxa: link to Sample as well
            if current_taxa == taxa_tokens[-1]:
                self.upsert_link(source=current_taxa, target=sample_name, value=abundance)

    def build_graph(self, taxa_table):
        """Return a JSON flow object.

        Takes a dict of sample_name to normalized taxa vectors
        """
        for sample_name, taxa_vector in taxa_table.items():
            # Add all samples as nodes
            self.upsert_node(sample_name, 'samples')

            for taxon_name, abundance in taxa_vector.items():
                if (abundance < self.min_abundance) or 't__' in taxon_name:
                    continue
                self.handle_one_taxon(sample_name, taxon_name, abundance)

            return {
                'nodes': list(self.nodes.values()),
                'edges': list(self.links.values()),
            }


def make_all_flows(samples):
    """Determine flows by tool."""
    flow_table = {}
    tool_names = [
        Metaphlan2ResultModule.name(),
        KrakenResultModule.name(),
        KrakenHLLResultModule.name(),
    ]
    for tool_name in tool_names:
        taxa_flow = TaxaFlow(samples, tool_name).graph

        save_tool_name = 'kraken'
        if 'metaphlan2' in tool_name:
            save_tool_name = 'metaphlan2'
        elif 'krakenhll' in tool_name:
            save_tool_name = 'krakenhll'

        flow_table[save_tool_name] = taxa_flow

    return {'by_tool': flow_table}


def processor(*samples):
    """Handle Taxon Abundance component calculations."""
    result = make_all_flows(samples)
    return result
