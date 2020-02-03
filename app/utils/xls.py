"""Excel utilities."""

from collections import OrderedDict

import xlrd


class XLSDictReader:  # pylint: disable=too-few-public-methods
    """
    A csv.DictReader-like class from xls(x) files.

    Based on: https://stackoverflow.com/a/25914394
    """

    def __init__(self, workbook_file, sheet_index=0):
        """Create XLSDictReader from file."""
        book = xlrd.open_workbook(workbook_file)
        sheet = book.sheet_by_index(sheet_index)

        def item(i, j):
            """Return header and contents for a given cell location."""
            return (sheet.cell_value(0, j), sheet.cell_value(i, j))

        self.rows = (OrderedDict(item(i, j) for j in range(sheet.ncols))
                     for i in range(1, sheet.nrows))
        self.fieldnames = [sheet.cell_value(0, i) for i in range(sheet.ncols)]
        self.row_num = 0

    def __iter__(self):
        """Return iterator."""
        return self

    def __next__(self):
        """Get next item of iterator."""
        if self.row_num >= len(self.rows):
            raise StopIteration()

        row = self.rows[self.row_num]
        self.row_num += 1
        return row
