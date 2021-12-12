import random
import numpy as np
from numpy.linalg import norm
from gensim import similarities, downloader
import csv
# https://radimrehurek.com/gensim/

# called by main each time after Experiment() has been called
# to record analysis data into analysis.csv returned from Experiment()
def Analysis(modelName='', vocabSize=0, C=0, V=0):
    analysis_csv = open('analysis.csv', 'a')
    analysis = csv.writer(analysis_csv)
    analysis.writerow([modelName, vocabSize, C, V, float(C) / V])
    analysis_csv.close()


# helper function to see if the word is presented in the model
# if no exception, meaning the word is presented in model, return true
# if KeyError Exception, meaning the word is not present in model, return false
# parameters:
# model - the model itself
# word - the target word
def IsWordInModel(model=None, word=''):
    if model == None or word == '':
        return False

    try:
        model[word]
    except KeyError:
        return False

    return True

# return the cosine similarity of the given two vectors
def cosineSimilarity(vec1, vec2):
    if len(vec1) != len(vec2):
        return 0

    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))


# called by main to run experiment on a specific word embedding and return the following:
# C - the number of correct labels
# V - the number of questions the model answered without guessing
# parameters:
# embedding - the pre-trained word embedding model
# modelName - the name of the current model (used to generate the model_detail_output csv file)
def Experiment(model=None, modelName=''):
    # open up the question csv file
    synonyms_csv = open('synonyms.csv', 'r')
    synonyms = csv.reader(synonyms_csv)
    # the first line wont count
    next(synonyms)

    # generate the <model_name>-details.csv file
    model_detail_output_csv = open(modelName + '-details.csv', 'w')
    model_detail_output = csv.writer(model_detail_output_csv)

    correctLabelCount = 0  # C
    notGuessCount = 80  # V

    # the following loop will execute 80 times (for this given synonyms test set)
    for r in synonyms:
        # extract the words from test set
        questionWord = r[0]
        answerWord = r[1]
        optionWords = r[2:6]

        # questionEmbedding = None
        # optionEmbedding = None

        label = ''
        modelAnswerWord = ''


        # try to find the embedding of questionWord from the model
        if IsWordInModel(model, questionWord):
            questionEmbedding = model[questionWord]
        else:
            label = 'guess'

        # if the question word is found, then safely proceed to getting the words
        if label != 'guess':
            # try all four answers and see which one is the best
            bestSimilarity = 0
            for option in optionWords:
                # first check if the option is in the model
                # if in the model, get the embedding and generate a similarity value
                if IsWordInModel(model, option):
                    optionEmbedding = model[option]
                    # currentSimilarity = similarities.Similarity(questionEmbedding, optionEmbedding)
                    currentSimilarity = cosineSimilarity(questionEmbedding, optionEmbedding)
                    print(f'{questionWord}, {option}, {currentSimilarity}')
                    # check if this similarity is better than the current best
                    if currentSimilarity > bestSimilarity:
                        bestSimilarity = currentSimilarity
                        modelAnswerWord = option

            # if after the above loop, the modelAnswerWord is still an empty string,
            # that means all four options does not exist in the model
            # put the label to guess and generate a random answer
            if modelAnswerWord == '':
                label = 'guess'
                modelAnswerWord = optionWords[random.randint(0, 3)]
            # now if the above if was not executed, that means we had an answer from the model

        # else if the question word is not found, then guess a random answer.
        else:
            modelAnswerWord = optionWords[random.randint(0, 3)]


        # record the first three fields of the detail csv file (questionWord, answerWord, modelAnswerWord)
        detailRowToWrite = [questionWord, answerWord, modelAnswerWord]
        # at last, see if the model gets the correct answer and update corresponding counters
        if answerWord == modelAnswerWord and label != 'guess':
            label = 'correct'
            correctLabelCount += 1
        elif answerWord != modelAnswerWord and label != 'guess':
            label = 'wrong'

        if label == 'guess':
            correctLabelCount -= 1

        detailRowToWrite.append(label)
        model_detail_output.writerow(detailRowToWrite)

    synonyms_csv.close()
    model_detail_output_csv.close()

    return correctLabelCount, notGuessCount

def main():
    # write analysis table head
    analysis_csv = open('analysis.csv', 'w')
    analysis = csv.writer(analysis_csv)
    analysis.writerow(['model name', '|V|', 'C', 'V', 'accuracy'])
    analysis_csv.close()
    # task1
    # first use the word2vec-google-news-300
    word2vecEmbedding = downloader.load("word2vec-google-news-300")
    C, V = Experiment(word2vecEmbedding, "word2vec-google-news-300")
    Analysis('word2vec-google-news-300', len(word2vecEmbedding), C, V)

if __name__ == "__main__":
    main()
