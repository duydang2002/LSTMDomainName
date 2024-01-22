"""Train and test LSTM classifier"""
import dga_classifier.data as data
import numpy as np
import pickle
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, SpatialDropout1D, LSTM, Dense

import sklearn
from sklearn.model_selection import train_test_split
def build_model(max_features, maxlen):
    """Build LSTM model"""
    model = Sequential()
    model.add(Embedding(max_features, 128, input_length=maxlen))
    model.add(SpatialDropout1D(0.5))
    model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop')

    return model

def run(max_epoch=25, nfolds=10, batch_size=128):
    """Run train/test on logistic regression model"""
    indata = data.get_data()

    labels, X = zip(*indata)

    # Generate a dictionary of valid characters
    valid_chars = {x:idx+1 for idx, x in enumerate(set(''.join(X)))}
    print(type(valid_chars))
    pickle.dump(valid_chars,open('Validchars.pkl', 'wb'),protocol=pickle.HIGHEST_PROTOCOL)
    max_features = len(valid_chars) + 1
    maxlen = np.max([len(x) for x in X])

    # Convert characters to int and pad
    X = [[valid_chars[y] for y in x] for x in X]
    X = sequence.pad_sequences(X, maxlen=maxlen)

    # Convert labels to 0-1
    y = [0 if x == 'benign' else 1 for x in labels]

    final_data = []

    for fold in range(nfolds):
        print("fold {}/{}".format(fold+1, nfolds))
        X_train, X_test, y_train, y_test, _, label_test = train_test_split(X, y, labels, 
                                                                           test_size=0.2)

        print('Build model...')
        model = build_model(max_features, maxlen)

        print("Train...")
        X_train, X_holdout, y_train, y_holdout = train_test_split(X_train, y_train, test_size=0.05)
        best_iter = -1
        best_auc = 0.0
        out_data = {}
        for ep in range(max_epoch):
            X_train = np.array(X_train)
            print(X_train[0])
            y_train = np.array(y_train)
            model.fit(X_train, y_train, batch_size=batch_size, epochs=1)

            t_probs = model.predict(X_holdout)
            
            t_auc = sklearn.metrics.roc_auc_score(y_holdout, t_probs)  # Assuming binary classification, adjust if necessary
            
            print ('Epoch %d: auc = %f (best=%f)' % (ep, t_auc, best_auc))
            test_loss, test_accuracy = model.evaluate(X_test, y_test)
            print(f"Final Test Loss: {test_loss}, Final Test Accuracy: {test_accuracy}") 
            if t_auc > best_auc:
                best_auc = t_auc
                best_iter = ep

                probs = model.predict(X_test)
                classes_x_test = np.argmax(probs,axis=-1)

                out_data = {'y':y_test, 'labels': label_test, 'probs':classes_x_test , 'epochs': ep,
                            'confusion_matrix': sklearn.metrics.confusion_matrix(y_test, probs > .5)}

                print (sklearn.metrics.confusion_matrix(y_test, probs > .5))

            else:
                # No longer improving...break and calc statistics
                if (ep-best_iter) > 2:
                    break

        final_data.append(out_data)
    return final_data