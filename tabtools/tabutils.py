#!/usr/bin/env python

from  collections import namedtuple


class TSTable(object):
    def __init__(self, filename, meta_filename=None, meta=None):
        if meta is not None:
            fields = meta
        elif meta_filename is not None:
            fields = open(meta_filename).read().strip().split('\t')
        else:
            fields = open('meta.' + filename).read().strip().split('\t')

        self.meta = TSTableMeta(fields)
        self.filename = filename
    def make_record_cls(self):
        return namedtuple("Record", self.meta.fields())


class TSTableMeta(object):
    def __init__(self, fields):
        '''
        :param columns: mapping from column names to indices
        :param fields: list of column names (order is important)
        :return:
        '''
        self._fields = fields
        self._columns = dict((col, i) for i, col in enumerate(fields))

    def __getitem__(self, i):
        return self._columns[i]

    def fields(self):
        return self._fields

#class TSRecord(object):
    pass


#def dump_records(f, records):
#    for r in records:
#        f.write("%s\n" % "\t".join([getattr(r, field) for field in r._fields]))

