import collections, math

class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    #self.KneserNeySmoothing
    self.reverseBigramCount = collections.defaultdict(lambda : collections.defaultdict(lambda : 0))
    self.bigramCount = collections.defaultdict(lambda :collections.defaultdict(lambda : 0))
    self.unigramCount = collections.defaultdict(lambda: 0)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """
    lastToken = "#"
    for sentence in corpus.corpus:
      for datum in sentence.data:
        token = datum.word
        self.reverseBigramCount[token][lastToken] = self.reverseBigramCount[token][lastToken] + 1
        self.bigramCount[lastToken][token] = self.bigramCount[lastToken][token] + 1
        self.unigramCount[token] = self.unigramCount[token] + 1
        self.total += 1
        lastToken = token


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    lastToken = "#"

    for token in sentence:
      bigramCount = self.bigramCount[lastToken][token]
      if (bigramCount > 2):
        bigramCount -=0.75
      elif (bigramCount > 0):
        bigramCount -= 0.5
      else:
        bigramCount = 0.0001
      lastTokenCount = self.unigramCount[lastToken]
      if (lastTokenCount == 0 ):
        lastTokenCount = 999999
      r = 0.75 / lastTokenCount * (len(self.bigramCount[lastToken].items()) + 0.001)

      pc = float(len(self.reverseBigramCount[token].items())) / self.total
      score += math.log(bigramCount/lastTokenCount + r * pc)

      lastToken = token
    return score
