import collections, math

class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    self.trigramCount = collections.defaultdict(lambda:collections.defaultdict(lambda: collections.defaultdict(lambda : 0)))
    self.bigramCount = collections.defaultdict(lambda: collections.defaultdict(lambda : 0))
    self.unigramCount = collections.defaultdict(lambda: 0)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    lastSecondToken = "#"
    lastToken = "#"
    for sentence in corpus.corpus:
      for datum in sentence.data:
        token = datum.word
        self.unigramCount[token] = self.unigramCount[token] + 1
        self.bigramCount[lastToken][token] = self.bigramCount[lastToken][token] + 1
        self.trigramCount[lastSecondToken][lastToken][token] = self.trigramCount[lastSecondToken][lastToken][token] + 1
        self.total += 1
        lastSecondToken = lastToken
        lastToken = token

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    lastSecondToken = "#"
    lastToken = "#"
    for token in sentence:
      triCount = self.trigramCount[lastSecondToken][lastToken][token]
      biCount = self.bigramCount[lastToken][token]
      uniCount = self.unigramCount[token]
      if (triCount > 0):
        score += math.log(triCount)
        score -= math.log(biCount)
      elif (biCount > 0):
        score += math.log(0.4)
        score += math.log(biCount)
        score -= math.log(uniCount)
      elif (uniCount > 0):
        score += math.log(0.16)
        score += math.log(uniCount)
        score -= math.log(self.total)
      else:
        score += math.log(0.064)
        score -= math.log(self.total)
      lastSecondToken = lastToken
      lastToken = token

    return score
