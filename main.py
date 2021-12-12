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

    # 4.initialize CV
    C = 0
    V = 80

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
            V -= 1

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
                    C += 1
                else:
                    label = "wrong"

        except KeyError:
            label = 'guess'
            V -= 1
            bestOption = choice(options)

        row = [qWithAns[0], qWithAns[1], bestOption, label]
        fileCsvWriter.writerow(row)

    # header = [w2VecModel, len(preTrainedModel), C, V]
    # fileCsvWriter.writerow(header)

    # close file
    testData.close()
    wFile.close()

    return len(preTrainedModel), C, V, C/V if C != 0 else 0


def main():
    w2VecModel = "word2vec-google-news-300"
    wAnalysisFile = open('analysis.csv', 'w')
    analysisCsvWriter = csv.writer(wAnalysisFile)
    modelLength, C, V, rate = evalW2vecModel(w2VecModel, 'synonyms.csv')
    header = [w2VecModel, modelLength, C, V, rate]
    analysisCsvWriter.writerow(header)


if __name__ == "__main__":
    main()
