"""AUTOCOMPLETE -
This file contains the process where we train our predictive models, Also
helpful are the load_models and save_models functions.
"""

import os

import collections

import pickle

from . import helpers

WORDS = []

WORD_TUPLES = []

WORDS_MODEL = {}

WORD_TUPLES_MODEL = {}

#This step is where we transform "raw" data
# into some sort of probabilistic model(s)
def train_models(corpus, model_name="models_compressed.pkl"):
    """Takes in a preferably long string (corpus/training data),
    split that string into a list, we \"chunkify\" resulting in
    a list of 2-elem list. Finally we create a dictionary,
    where each key = first elem and each value = Counter([second elems])

    Will save/pickle model by default ('models_compressed.pkl').
    Set second argument to false if you wish to not save the models.
    """

    # "preperation" step
    # word is in WORDS
    global WORDS
    WORDS = helpers.re_split(corpus)

    # first model -> P(word)
    global WORDS_MODEL
    WORDS_MODEL = collections.Counter(WORDS)

    # another preperation step
    # wordA, wordB are in WORDS
    global WORD_TUPLES
    WORD_TUPLES = list(helpers.chunks(WORDS, 2))

    # second model -> P(wordA|wordB)
    global WORD_TUPLES_MODEL
    WORD_TUPLES_MODEL = {first:collections.Counter()
                         for first, second in WORD_TUPLES}

    for tup in WORD_TUPLES:
        try:
            WORD_TUPLES_MODEL[tup[0]].update([tup[1]])
        except:
            # hack-y fix for uneven # of elements in WORD_TUPLES
            pass

    if model_name:
        save_models(os.path.join(os.path.dirname(__file__), model_name))


def train_bigtxt():
    """unnecessary helper function for training against
    default corpus data (big.txt)"""

    bigtxtpath = os.path.join(os.path.dirname(__file__), 'big.txt')
    with open(bigtxtpath, 'rb') as bigtxtfile:

        train_models(str(bigtxtfile.read()))


def save_models(path=None):
    """Save models to 'path'. If 'path' not specified,
    save to module's folder under name 'models_compressed.pkl'"""

    if path == None:
        path = os.path.join(os.path.dirname(__file__), 'models_compressed.pkl')

    print("saving to:", path)
    #save for next use. pickle format: (key=model name, value=model)
    pickle.dump({'words_model': WORDS_MODEL,
                 'word_tuples_model': WORD_TUPLES_MODEL},
                open(path, 'wb'),
                protocol=2)


def load_models(load_path=None):
    """Load autocomplete's built-in model (uses Norvig's big.txt). Optionally
    provide the path to Python pickle object."""

    if load_path is None:
        load_path = os.path.join(os.path.dirname(__file__),
                                 'models_compressed.pkl')
    try:
        models = pickle.load(open(load_path,'rb'))

        global WORDS_MODEL
        WORDS_MODEL = models['words_model']

        global WORD_TUPLES_MODEL
        WORD_TUPLES_MODEL = models['word_tuples_model']

        print("successfully loaded: models_compressed.pkl")
    except IOError:
        print("Error in opening pickle object. Training on default corpus text.")
        train_bigtxt()
    except KeyError:
        print("Error in loading both predictve models.\
              Training on default corpus text.")
        train_bigtxt()
    except ValueError:
        print("Corrupted pickle string.\
              Training on default corpus text (big.txt)")
        train_bigtxt()
