from gensim import corpora, models, similarities, downloader
import csv


# https://radimrehurek.com/gensim/

# word_vectors = downloader.load("word2vec-google-news-300")


def main():
    yo = ["yo", "yo", "yo"]

    f = open('try.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(yo)
    f.close()


if __name__ == "__main__":
    main()
