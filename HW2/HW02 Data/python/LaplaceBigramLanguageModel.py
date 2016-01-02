import collections, math

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    self.LaplaceBigramCount = collections.defaultdict(lambda: collections.defaultdict(lambda : 0))
    self.LaplaceUnigramCount = collections.defaultdict(lambda: 0)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """
    lastToken = "#"
    for sentence in corpus.corpus:
      for datum in sentence.data:
        token = datum.word
        self.LaplaceUnigramCount[token] = self.LaplaceUnigramCount[token] + 1
        self.LaplaceBigramCount[lastToken][token] = self.LaplaceBigramCount[lastToken][token] + 1
        self.total += 1
        lastToken = token


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    vcb = len(self.LaplaceUnigramCount.items())
    lastToken = "#"
    for token in sentence:
      score += math.log(self.LaplaceBigramCount[lastToken][token] + 1)
      score -= math.log(self.LaplaceUnigramCount[token] + vcb)
      lastToken = token
    return score
