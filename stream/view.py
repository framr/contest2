from itertools import chain

class StreamItem(object):
    pass


class View(object):
    """
    A view of a stream.
    Each view has position of central item and some context around it
    """
    def __init__(self, position, context):
        self.pos = position
        self.context = context


class StreamViewer(object):
    pass


class SessionStreamViewer(StreamViewer):
    def __init__(self, instream, context_hsize=None):
        """
        :param instream: input stream of sessions, each session is a list
        :param context_hsize has on effect on the behaviour
        :return: stream of views
        """
        self.instream = iter(instream)
        self.pos = 0
        self.session = []

    def __iter__(self):
        return self

    def next(self):
        """
        :return: tuple - (position of current element in context, buffered batch of records)
        """
        if self.pos == len(self.session):
            self.session = []
            self.pos = 0
            while not self.session:
                event = next(self.instream)
                self.session = list(event)

        shift = self.pos
        self.pos += 1
        return View(shift, self.session)

class SymmetricStreamViewer(StreamViewer):

    def __init__(self, instream, context_hsize=10):

        self.context = deque()
        self.pos = self.left = self.right = 0
        self.context_hsize = context_hsize # context half size
        self.instream = iter(instream)

    def __iter__(self):
        return self

    def next(self):
        """
        :return: tuple - (position of current element in context, buffered batch of records)
        """
        while self.right - self.pos < self.context_hsize + 1:
            try:
                self.context.append(next(self.instream))
                self.right += 1
            except StopIteration:
                break

        while self.pos - self.left > self.context_hsize:
            self.context.popleft()
            self.left += 1

        if self.pos > self.right - 1 or not self.context:
            # nothing to process
            raise StopIteration


        shift = self.pos - self.left
        self.pos += 1
        return View(shift, self.context)
        #self.pos += 1



if __name__ == '__main__':

    tests = [
        [],
        [1],
        [1, 2],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ]

    print "context size = 1"
    for s in tests:
        b = SymmetricStreamViewer(s, 1)
        print "stream ", s
        for p, context in b:
            print p, list(context)

    print "context size = 2"
    for s in tests:
        b = SymmetricStreamViewer(s, 2)
        print "stream ", s
        for p, context in b:
            print p, list(context)



    print "Session streamer"
    b = SymmetricStreamViewer(tests)
    for p, context in b:
        print p, list(context)


    stream = [["a", "b"], ["c", "d", "e"], ["f"]]
    flattened = list(chain.from_iterable(stream))
    feature_map = dict((w, i) for i, w in enumerate(flattened))
    sampling_table = dict(zip(flattened,  len(flattened) * [1.0]))
    print stream, feature_map
    print "Testing skipgrams"