import random

class SkipGramStreamer(object):
    def __init__(self, context_streamer, neg_pairs=1.0, window_size=5, min_window_size=None,
        sampling_table=None, neg_sampling_table=None, shuffle=True):
        """
        :param context_streamer:
        :param feature_map: if provided, remap words according to mapping
        :param neg_sampling_table: tuple of arrays (items, probabilities)
        :return: tuples (word, context, distance between context and word positions)
        """

        self.shuffle = shuffle
        self.neg_pairs = neg_pairs
        self.window_size = window_size
        self.min_window_size = min_window_size
        self.sampling_table = sampling_table
        self.context_streamer = context_streamer
        self.neg_sampling_table = neg_sampling_table


    def __iter__(self):
        return self
    def next(self):
        good_context = False
        while not good_context:
            center_pos, context = next(self.context_streamer)
            center_word = context[center_pos]

            good_context = True
            if len(context) < 2:
                good_context = False
            if self.sampling_table:
                if self.sampling_table[center_word] < random.random():
                    good_context = False
        #print "word, context %s, %s" % (center_word, context)

        # define window around pos
        if self.min_window_size is None:
            window_size = self.window_size
        else:
            window_size = random.randint(self.min_window_size, self.window_size)
        window_begin = max(center_pos - window_size, 0)
        window_end = min(center_pos + window_size, len(context) - 1)

        # aggregates positive pairs
        pairs = []
        for pos in range(window_begin, window_end + 1):
            if pos != center_pos:
                pairs.append((center_word, context[pos], abs(pos - center_pos)))

        num_positives = len(pairs)
        labels = len(pairs) * [1]

        # generate negative samples
        num_negatives = int(num_positives * self.neg_pairs)
        negatives = []
        sample_from_neg_table = np.random.multinomial(num_negatives, self.neg_sampling_table[1])
        for index in np.nonzero(multi):
            negatives.extend(
                [(center_word, self.neg_sampling_table[0][index], 0) for i in range(sample_from_neg_table[index])]
            )

        labels += len(negatives) * [0]
        pairs += negatives

        if self.shuffle:
            tmp = zip(pairs, labels)
            random.shuffle(tmp)
            pairs, labels = zip(*tmp)

        return pairs, labels
