import dga_classifier.data as data
import dga_classifier.lstm as lstm
import dga_classifier.bigram as bigram

import itertools
import os
import pickle
import matplotlib
matplotlib.use('Agg')
import numpy as np

from sklearn.metrics import roc_curve, auc
import os
import pickle
import numpy as np
from sklearn.metrics import roc_curve, auc
from matplotlib import pyplot as plt

RESULT_FILE = 'results.pkl'

print(os.getcwd())

def run_experiments(isbigram=True, islstm=True, nfolds=10):
    """Runs all experiments"""
    bigram_results = None
    lstm_results = None

    if isbigram:
        bigram_results = bigram.run(nfolds=nfolds)

    if islstm:
        lstm_results = lstm.run(nfolds=nfolds)

    return bigram_results, lstm_results

def create_figs(isbigram=True, islstm=True, nfolds=10, force=False):
    """Create figures"""
    # Generate results if needed
    if force or (not os.path.isfile(RESULT_FILE)):
        bigram_results, lstm_results = run_experiments(isbigram, islstm, nfolds)

        results = {'bigram': bigram_results, 'lstm': lstm_results}

        pickle.dump(results, open(RESULT_FILE, 'wb'))
    else:
        results = pickle.load(open(RESULT_FILE, 'rb'))


if __name__ == "__main__":
    create_figs(isbigram=False, nfolds=1)  # Run with 1 to make it fast