"""Taxa Tree display models."""

import mongoengine as mdb


def validate_json_tree(root, parent=None):
    """Check that a tree has the appropriate fields."""
    if 'name' not in root:
        raise mdb.ValidationError('Node does not contain name field')

    if 'size' not in root:
        raise mdb.ValidationError('Node does not contain size field')
    else:
        try:
            float(root['size'])
        except ValueError:
            raise mdb.ValidationError('Size is not a float')

    if 'parent' not in root:
        raise mdb.ValidationError('Node does not contain parent field')
    elif parent and (root['parent'] != parent):
        msg = 'Listed parent ({}) does not match structural parent ({}) in node {}'
        msg = msg.format(root['parent'], parent, root['name'])
        raise mdb.ValidationError(msg)

    if 'children' not in root:
        raise mdb.ValidationError('Node does not contain children field')

    for child in root['children']:
        validate_json_tree(child, parent=root['name'])


class TaxaTreeResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Read stats embedded result."""

    metaphlan2 = mdb.MapField(field=mdb.DynamicField(), required=True)
    kraken = mdb.MapField(field=mdb.DynamicField(), required=True)
    krakenhll = mdb.MapField(field=mdb.DynamicField(), required=True)

    def clean(self):
        """Check that model is correct."""
        validate_json_tree(self.metaphlan2)
        validate_json_tree(self.kraken)
        validate_json_tree(self.krakenhll)
