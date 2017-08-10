import collections
import nltk
import dateutil.parser as parser

from sentimental.src import *
from sentimental.src.home import *
from sentimental.src.searchdatabase import *

from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt


from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, Context
from numpy import mean
from sentimental.database import CSVtoMongoDB
from sentimental.models import brandnameReviews, genericnameReviews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from nltk.corpus import stopwords


def keywordslist(request):
    d = path.dirname("/Users/Nil/GradFinalProject/sentianalysis/")
    # / Users / Nil / GradFinalProject / sentianalysis / data.txt
    text = open(path.join(d, 'data.txt')).read()
    wordcloud = WordCloud().generate(text)

    wordcloud = WordCloud(max_font_size=40).generate(text)
    # plt.figure()
    # plt.imsave("words.png",wordcloud)
    # plt.axis("off")
    image = wordcloud.to_image()

    wordcloud.to_file("data.png")

    # image.show()
    return render_to_response('sentimental/keywords.html')



def keyData(text):
    word_list = list()

    # Used when tokenizing words
    sentence_re = r'''(?x)      # set flag to allow verbose regexps
          ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
        | \w+(-\w+)*            # words with optional internal hyphens
        | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
        | \.\.\.                # ellipsis
        | [][.,;"'?():-_`]      # these are separate tokens
    '''

    lemmatizer = nltk.WordNetLemmatizer()
    stemmer = nltk.stem.porter.PorterStemmer()

    # Taken from Su Nam Kim Paper...
    grammar = r"""
        NBAR:
            {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

        NP:
            {<NBAR>}
            {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
    """
    chunker = nltk.RegexpParser(grammar)

    # toks = nltk.regexp_tokenize(text, sentence_re)
    # postoks = nltk.tag.pos_tag(toks)

    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    # for a in sentences:
    accepted = list()
    toks = nltk.word_tokenize(text)
    postoks = nltk.tag.pos_tag(toks)

    # print postoks

    tree = chunker.parse(postoks)
    from nltk.corpus import stopwords
    stopwords = stopwords.words('english')

    def leaves(tree):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
            yield subtree.leaves()

    def normalise(word):
        """Normalises words to lowercase and stems and lemmatizes it."""
        word = word.lower()
        word = stemmer.stem_word(word)
        word = lemmatizer.lemmatize(word)
        return word

    def acceptable_word(word):
        """Checks conditions for acceptable word: length, stopword."""
        accepted = bool(2 <= len(word) <= 40 and word.lower() not in stopwords)
    return accepted

    def get_terms(tree):
        for leaf in leaves(tree):
            term = [normalise(w) for w, t in leaf if acceptable_word(w)]
            print leaf
            yield term

    terms = get_terms(tree)

    for term in terms:
        print len(term)
        word_list.append(' '.join(word for word in term))

    return word_list