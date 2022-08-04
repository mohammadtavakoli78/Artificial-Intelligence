import itertools
import random
import os


def pre(string):
    string = string.lower().replace("*", "").replace("?", "").replace("!", "").replace(".", "")
    string = string.lower().replace(",", "").replace("-", " ").replace("(", "").replace(")", "")
    string = string.lower().replace("[", "").replace("]", " ").replace("\"", "").replace("'", "")
    return string


def fillUnigramDict(sentences):
    unigramDict = {}
    for i in range(len(sentences)):
        splitedSentence = sentences[i].split()
        for d in splitedSentence:
            if d in unigramDict.keys():
                unigramDict[d] += 1
            else:
                unigramDict[d] = 1
    return unigramDict


def fillBigramDict(sentences):
    bigramDict = {}
    for i in range(len(sentences)):
        splitedSentence = sentences[i].split()
        for j in range(len(splitedSentence) - 1):
            words = splitedSentence[j] + "|" + splitedSentence[j + 1]
            if words in bigramDict.keys():
                bigramDict[words] += 1
            else:
                bigramDict[words] = 1
    return bigramDict


def goodComment(inputString, positiveUniProb, positiveBiProb, negativeUniProb, negativeBiProb, langType='bigram'):
    cleanString = pre(inputString).split()
    positiveProbability = 1
    negativeProbability = 1


    epsilon = 0.4
    landa1 = 0.3
    landa2 = 0.7
    landa3 = 0.7


    if langType == 'bigram':
        if cleanString[0] in positiveUniProb:
            positiveProbability *= positiveUniProb[cleanString[0]]
        if cleanString[0] in negativeUniProb:
            negativeProbability *= negativeUniProb[cleanString[0]]

        for i in range(len(cleanString) - 1):
            biWord = cleanString[i] + "|" + cleanString[i + 1]
            biWordPositiveProb = 0
            biWordNegativeProb = 0

            if biWord in positiveBiProb:
                biWordPositiveProb += landa3 * positiveBiProb[biWord]
            if biWord in negativeBiProb:
                biWordNegativeProb += landa3 * negativeBiProb[biWord]

            if cleanString[i] in positiveUniProb:
                biWordPositiveProb += landa2 * positiveUniProb[cleanString[i]]
            if cleanString[i] in negativeBiProb:
                biWordPositiveProb += landa2 * negativeUniProb[cleanString[i]]

            biWordPositiveProb += landa1 * epsilon
            biWordNegativeProb += landa1 * epsilon

            positiveProbability *= biWordPositiveProb
            negativeProbability *= biWordNegativeProb
    else:
        for i in range(len(cleanString)):
            uniWordPositiveProb = 0
            uniWordNegativeProb = 0
            if cleanString[i] in positiveUniProb:
                uniWordPositiveProb += landa2 * positiveUniProb[cleanString[i]]
            if cleanString[i] in negativeBiProb:
                uniWordPositiveProb += landa2 * negativeUniProb[cleanString[i]]
            uniWordPositiveProb += landa1 * epsilon
            uniWordNegativeProb += landa1 * epsilon

            positiveProbability *= uniWordPositiveProb
            negativeProbability *= uniWordNegativeProb

    return positiveProbability > negativeProbability


positiveFile = open(os.path.join(os.path.dirname(__file__)+"/rt-polarity.pos"))
negativeFile = open(os.path.join(os.path.dirname(__file__)+"/rt-polarity.neg"))
positiveSentences = positiveFile.readlines()
negativeSentences = negativeFile.readlines()

# random.shuffle(positiveSentences)
# random.shuffle(negativeSentences)

for i in range(len(positiveSentences)):
    positiveSentences[i] = pre(positiveSentences[i])
for i in range(len(negativeSentences)):
    negativeSentences[i] = pre(negativeSentences[i])

positiveSentencesSize = len(positiveSentences)
negativeSentencesSize = len(negativeSentences)

positiveTrainSentences = positiveSentences[:int(positiveSentencesSize * 0.85)]
positiveTestSentences = positiveSentences[int(positiveSentencesSize * 0.85):]

negativeTrainSentences = negativeSentences[:int(negativeSentencesSize * 0.85)]
negativeTestSentences = negativeSentences[int(negativeSentencesSize * 0.85):]

positiveUnigramDict = fillUnigramDict(positiveTrainSentences)
negativeUnigramDict = fillUnigramDict(negativeTrainSentences)

positiveBigramDict = fillBigramDict(positiveTrainSentences)
negativeBigramDict = fillBigramDict(negativeTrainSentences)

positiveUnigramDict = dict(sorted(positiveUnigramDict.items(), key=lambda kval: kval[1]))
negativeUnigramDict = dict(sorted(negativeUnigramDict.items(), key=lambda kval: kval[1]))

positiveUnigramDict = dict(list(positiveUnigramDict.items())[:-10])
negativeUnigramDict = dict(list(negativeUnigramDict.items())[:-10])

positiveUnigramDict = dict([(p, m) for p, m in positiveUnigramDict.items() if m > 1])
negativeUnigramDict = dict([(p, m) for p, m in negativeUnigramDict.items() if m > 1])

positiveProbUniDict = {}
negativeProbUniDict = {}
positiveProbBiDict = {}
negativeProbBiDict = {}

positiveWordsNumber = 0
for key in positiveUnigramDict.keys():
    positiveWordsNumber += positiveUnigramDict[key]

negativeWordsNumber = 0
for key in negativeUnigramDict.keys():
    negativeWordsNumber += negativeUnigramDict[key]



for key in positiveUnigramDict.keys():
    positiveProbUniDict[key] = positiveUnigramDict[key] / positiveWordsNumber

for key in negativeUnigramDict.keys():
    negativeProbUniDict[key] = negativeUnigramDict[key] / negativeWordsNumber


for key in positiveBigramDict:
    wordZero = key.split("|")[0]
    if wordZero in positiveUnigramDict:
        positiveProbBiDict[key] = positiveBigramDict[key] / positiveUnigramDict[wordZero]
    else:
        positiveProbBiDict[key] = 1

for key in negativeBigramDict:
    wordZero = key.split("|")[0]
    if wordZero in negativeUnigramDict:
        negativeProbBiDict[key] = negativeBigramDict[key] / negativeUnigramDict[wordZero]
    else:
        negativeProbBiDict[key] = 1


c = 0
for testSentence in positiveTestSentences:
    if goodComment(testSentence, positiveProbUniDict, positiveProbBiDict, negativeProbUniDict, negativeProbBiDict, 'bigram'):
        c += 1

for testSentence in negativeTestSentences:
    if not goodComment(testSentence, positiveProbUniDict, positiveProbBiDict, negativeProbUniDict, negativeProbBiDict, 'bigram'):
        c += 1

print(c / len(positiveTestSentences + negativeTestSentences))


sentence = input()
while sentence != '!q':
    if goodComment(sentence, positiveProbUniDict, positiveProbBiDict, negativeProbUniDict, negativeProbBiDict, 'bigram'):
        print('not filter this')
    else:
        print('filter this')
    sentence = input()