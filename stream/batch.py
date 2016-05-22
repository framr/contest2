
class Batch2BatchStreamer(object):
    """
    Transform input stream containing from batches into batches of specified size (or greater)
    """
    def __init__(self, instream, batch_size):
        self.instream = instream
        self.batch_size = batch_size
    def __iter__(self):
        return self
    def next(self):
        batch = []
        while len(batch) < self.batch_size:
            try:
                batch.extend(next(self.instream))
            except StopIteration:
                break

        if not batch:
            raise StopIteration
        return batch
