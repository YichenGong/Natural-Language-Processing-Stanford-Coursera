import math, collections

class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    self.LaplaceUnigramCount = collections.defaultdict(lambda : 0)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      for datum in sentence.data:
        token = datum.word
        self.LaplaceUnigramCount[token] = self.LaplaceUnigramCount[token] + 1
        self.total += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    vab = len(list(self.LaplaceUnigramCount.items()))
    score = 0.0
    for token in sentence:
      count = self.LaplaceUnigramCount[token] + 1
      score += math.log(count)
      score -= math.log(self.total + vab)
    #print (score)
    return score
