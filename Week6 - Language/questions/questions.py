import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    Files = dict()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            Files[filename] = file.read()
    return Files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = []

    stop_words = nltk.corpus.stopwords.words('english')
    punctuations = string.punctuation

    for word in nltk.word_tokenize(document.lower()):
        # Removing all the punctuations
        for char in punctuations:
            if char in word:
                word = word.replace(char, '')

        if word not in stop_words and word != "":
            words.append(word)

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    words = set()
    for document in documents:
        words.update(documents[document])
    for word in words:
        frequency = sum(word in documents[document] for document in documents)
        idf = math.log(len(documents) / frequency)
        idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf = dict()
    for file in files:
        tfidf[file] = 0
        for word in query:
            if word in idfs:
                tfidf[file] += (files[file].count(word) /
                                len(files[file]) * idfs[word])

    return sorted(tfidf, key=tfidf.get, reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_idfs = dict()
    for sentence in sentences:
        idf = 0
        td = 0

        if "==" in sentence or "===" in sentence:
            continue

        for word in query:
            tmp = 0
            if word in sentences[sentence]:
                tmp = idfs[word]
                td += 1
            idf += tmp
        sentence_idfs[sentence] = [idf, td / len(sentences[sentence])]

    return sorted(sentence_idfs,
                  key=lambda x: (sentence_idfs[x][0], sentence_idfs[x][1]),
                  reverse=True)[:n]


if __name__ == "__main__":
    main()
