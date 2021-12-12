from gensim import corpora, models, similarities, downloader
from random import choice
import csv


# https://radimrehurek.com/gensim/


def evalW2vecModel(w2VecModel, testDataSet):
    """initialization: """
    # 1. download a w2VecModel by given model name
    preTrainedModel = downloader.load(w2VecModel)

    # 2. testData: open a file to read from test data set
    testData = open(testDataSet, 'r', newline='')
    # 2.1. initialize a test data csv reader and skip the first line(intro)
    testCsvReader = csv.reader(testData, delimiter=',')
    next(testCsvReader)

    # 3. wFile: open a file to write analysis for test data set
    wFile = open(w2VecModel + 'details.csv', 'w')
    fileCsvWriter = csv.writer(wFile)

    # divide test data
    for row in testCsvReader:
        """ 
        note that the data structure in the file is
        [question, answer, 0, 1, 2, 3] 
        """
        # processing data
        qWithAns = [row[0], row[1]]
        options = row[2:6]
        # initialize data needed
        label = ""
        optionSim = []
        bestOption = ""

        # check if option exist
        counter = 0
        for item in options:
            try:
                temp = preTrainedModel[item]
                counter += 1
            except KeyError:
                print("For question " + qWithAns[0])
                print("The option " + item + " is not in provided model")
        if counter == 0:
            label = 'guess'

        # check if question exist
        try:
            temp = preTrainedModel[qWithAns[0]]

            for index, item in enumerate(options):
                optionSim.append(preTrainedModel.similarity(qWithAns[0], options[index]))

            for index, item in enumerate(optionSim):
                if item == max(optionSim):
                    bestOption = options[index]

            if label != "guess":
                if bestOption == qWithAns[1]:
                    label = "correct"
                else:
                    label = "wrong"

        except KeyError:
            label = 'guess'
            bestOption = choice(options)
            print("The question " + qWithAns[0] + " is not in provided model")

        row = [qWithAns[0], qWithAns[1], bestOption, label]
        fileCsvWriter.writerows(row)
    # close file
    testData.close()
    wFile.close()


def main():
    evalW2vecModel("word2vec-ruscorpora-300", 'synonyms.csv')


if __name__ == "__main__":
    main()
