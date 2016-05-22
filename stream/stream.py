from collections import namedtuple


def stream_generator(tstable, field, session=False):
    """
    Raw stream generator
    :param filename: input filename
    :param meta: meta class
    :param field: field to extract
    :param session: boolean variable indicating, whether to group items into sessions
    :return: generate sequence of items or lists of items
    """

    Record = tstable.make_record_cls()
    for line in open(tstable.filename):
        splitted = line.strip().split('\t')
        rec = Record(*splitted)
        value = getattr(rec, field)
        items = value.split()
        if session:
            yield items
        else:
            for it in items:
                yield it
