from gensim import similarities, downloader
import csv
# https://radimrehurek.com/gensim/



# called by main each time after Experiment() has been called
# to record analysis data into analysis.csv returned from Experiment()
def Analysis(modelName='', vocabSize=0, C=0, V=0):
    pass

# called by main to run experiment on a specific word embedding and return the following:
# C - the number of correct labels
# V - the number of questions the model answered without guessing
# parameters:
# embedding - the pre-trained word embedding model
# modelName - the name of the current model (used to generate the model_detail_output csv file)
def Experiment(embedding=None, modelName=''):
    # open up the question csv file
    synonyms_csv = open('synonyms.csv', 'r')
    synonyms = csv.reader(synonyms_csv)
    # the first line wont count
    next(synonyms)

    # generate the <model_name>-details.csv file
    model_detail_output = open(modelName + '-details.csv', 'w')

    # the following loop will execute 80 times
    for r in synonyms:
        # extract the words
        question = r[0]
        answer = r[1]
        option1 = r[2]
        option2 = r[3]
        option3 = r[4]
        option4 = r[5]





    synonyms_csv.close()


def main():
    # task1
    # first use the word2vec-google-news-300
    # word2vecEmbedding = downloader.load("word2vec-google-news-300")
    # Experiment(word2vecEmbedding, "word2vec-google-news-300")
    Experiment()

if __name__ == "__main__":
    main()
