try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import csv
import tabulate


def as_table(rows, headers=None, table_format=None):
    if not rows:
        return ""
    if table_format == u'csv':
        sio = StringIO()
        csv_writer = csv.writer(sio)
        if headers:
            csv_writer.writerow(headers)
        for data in rows:
            csv_writer.writerow(data)
        return sio.getvalue()

    if table_format:
        assert table_format in tabulate.tabulate_formats, (
            "Unsupported table format {}".format(table_format)
        )
    return tabulate.tabulate(rows, headers=headers, tablefmt=table_format)
