import json, sys
import base64
from Datum import Datum

class FeatureFactory:
    """
    Add any necessary initialization steps for your features here
    Using this constructor is optional. Depending on your
    features, you may not need to intialize anything.
    """
    def __init__(self):
        pass


    """
    Words is a list of the words in the entire corpus, previousLabel is the label
    for position-1 (or O if it's the start of a new sentence), and position
    is the word you are adding features for. PreviousLabel must be the
    only label that is visible to this method. 
    """

    def computeFeatures(self, words, previousLabel, position):
        features = []
        currentWord = words[position]

        """ Baseline Features """
        features.append("word=" + currentWord)
        #features.append("prevLabel=" + previousLabel)
        features.append("word=" + currentWord + ", prevLabel=" + previousLabel)


        """ Warning: If you encounter "line search failure" error when
        running the program, considering putting the baseline features
	    back. It occurs when the features are too sparse. Once you have
        added enough features, take out the features that you don't need. 
	    """


        """ TODO: Add your features here """
        punctuation = False
        has_digit = False
        capList = []
        wordFrontShape = ""
        wordEndShape = ""
        charMiddleShape = set()
        for i in range(len(currentWord)):
            if (currentWord[i].isupper()):
                capList.append(i)
            if currentWord[i] in "-.,=';:?":
                punctuation = True
            if currentWord.isdigit():
                has_digit = True
            if len(currentWord) >= 4:
                if i < 2:
                    wordFrontShape = wordFrontShape + self.wordShapeConversion(currentWord[i])
                elif i >= 2 and len(currentWord) - i > 2:
                    charMiddleShape.add(self.wordShapeConversion(currentWord[i]))
                elif len(currentWord) - i <= 2:
                    wordEndShape = wordEndShape + self.wordShapeConversion(currentWord[i])
            else:
                wordFrontShape = wordFrontShape + self.wordShapeConversion(currentWord[i])


        wordMiddleShape = "".join(sorted(list(charMiddleShape)))
        wordShape = wordFrontShape + wordMiddleShape + wordEndShape

        if len(capList) == 0:
            features.append("case=lowercase")
        elif len(capList) == 1 and capList[0] == 0:
            #features.append("case=Title")
            features.append("prevLabel=" + previousLabel + ", case=Title")
        elif len(capList) == len(currentWord):
            features.append("case=ALLCAP")
        elif len(capList) < len(currentWord) and len(capList) > 1:
            features.append("case=CamelCase")
            features.append("prevLabel=" + previousLabel + ", case=CamelCase")




        #last two char
        if currentWord[-2: ] =="ed":
            features.append("endwith=ed")
        #last three char
        elif currentWord[-3 :] == "nia":
            features.append("endwith=nia")
        elif currentWord[-3 :] == "ian":
            features.append("endwith=ian")
        elif currentWord[-3: ] == "nal":
            features.append("endwith=nal")
        elif currentWord[-3: ] == "ing":
            features.append("endwith=ing")
        elif currentWord[-3: ] == "ies":
            features.append("endwith=ies")
        elif currentWord[-3: ] == "day":
            features.append("endwith=day")
        elif currentWord[-3: ] == "ity":
            features.append("endwith=ity")
        elif currentWord[-3: ] == "ive":
            features.append("endwith=ive")
        elif currentWord[-3: ] == "ent":
            features.append("endwith=ent")
        elif currentWord[-3: ] == "ese":
            features.append("endwith=ese")
        elif currentWord[-3: ] == "ish":
            features.append("endwith=ish")


        #last four char
        elif currentWord[-4 :] == "stan":
            features.append("endwith=stan")
        elif currentWord[-4: ] == "sion":
            features.append("endwith=sion")
        elif currentWord[-4: ] == "tion":
            features.append("endwith=tion")
        elif currentWord[-4: ] == "land":
            features.append("endwith=land")
        elif currentWord[-4: ] == "bury":
            features.append("endwith=burynia")
        #last char
        elif currentWord[-1] in "aeiou":
            features.append("endwith=vowel")
            features.append("endwith=vowel, prevLabel=" + previousLabel)
        elif currentWord[-1] == "s":
            features.append("endwith=s")
        elif currentWord[-1] == "r":
            features.append("endwith=r")





        if len(currentWord) > 5 and currentWord[-2 :] == "is":
            features.append("endwith=is")

        if has_digit:
            features.append("has_digits")

        features.append("wordShape=" + wordShape)

        # if currentWord[0:2] == "Mc":
        #     features.append("beginwith=Mc")
        #
        features.append("beginWith=" + currentWord[0:2])
        features.append("terminateWith=" + currentWord[-3:])



        return features

    def wordShapeConversion(self, s):
        if s.isdigit():
            return "d"
        elif s.islower():
            return "x"
        elif s.isupper():
            return "X"
        else:
            return s


    """ Do not modify this method """
    def readData(self, filename):
        data = [] 
        
        for line in open(filename, 'r'):
            line_split = line.split()
            # remove emtpy lines
            if len(line_split) < 2:
                continue
            word = line_split[0]
            label = line_split[1]

            datum = Datum(word, label)
            data.append(datum)

        return data

    """ Do not modify this method """
    def readTestData(self, ch_aux):
        data = [] 
        
        for line in ch_aux.splitlines():
            line_split = line.split()
            # remove emtpy lines
            if len(line_split) < 2:
                continue
            word = line_split[0]
            label = line_split[1]

            datum = Datum(word, label)
            data.append(datum)

        return data


    """ Do not modify this method """
    def setFeaturesTrain(self, data):
        newData = []
        words = []

        for datum in data:
            words.append(datum.word)

        ## This is so that the feature factory code doesn't
        ## accidentally use the true label info
        previousLabel = "O"
        for i in range(0, len(data)):
            datum = data[i]

            newDatum = Datum(datum.word, datum.label)
            newDatum.features = self.computeFeatures(words, previousLabel, i)
            newDatum.previousLabel = previousLabel
            newData.append(newDatum)

            previousLabel = datum.label

        return newData

    """
    Compute the features for all possible previous labels
    for Viterbi algorithm. Do not modify this method
    """
    def setFeaturesTest(self, data):
        newData = []
        words = []
        labels = []
        labelIndex = {}

        for datum in data:
            words.append(datum.word)
            if datum.label not in labelIndex:
                labelIndex[datum.label] = len(labels)
                labels.append(datum.label)
        
        ## This is so that the feature factory code doesn't
        ## accidentally use the true label info
        for i in range(0, len(data)):
            datum = data[i]

            if i == 0:
                previousLabel = "O"
                datum.features = self.computeFeatures(words, previousLabel, i)

                newDatum = Datum(datum.word, datum.label)
                newDatum.features = self.computeFeatures(words, previousLabel, i)
                newDatum.previousLabel = previousLabel
                newData.append(newDatum)
            else:
                for previousLabel in labels:
                    datum.features = self.computeFeatures(words, previousLabel, i)

                    newDatum = Datum(datum.word, datum.label)
                    newDatum.features = self.computeFeatures(words, previousLabel, i)
                    newDatum.previousLabel = previousLabel
                    newData.append(newDatum)

        return newData

    """
    write words, labels, and features into a json file
    Do not modify this method
    """
    def writeData(self, data, filename):
        outFile = open(filename + '.json', 'w')
        for i in range(0, len(data)):
            datum = data[i]
            jsonObj = {}
            jsonObj['_label'] = datum.label
            jsonObj['_word']= base64.b64encode(datum.word)
            jsonObj['_prevLabel'] = datum.previousLabel

            featureObj = {}
            features = datum.features
            for j in range(0, len(features)):
                feature = features[j]
                featureObj['_'+feature] = feature
            jsonObj['_features'] = featureObj
            
            outFile.write(json.dumps(jsonObj) + '\n')
            
        outFile.close()

