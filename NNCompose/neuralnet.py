# Create first network with Keras
from keras.models import Sequential,load_model
from keras.layers import Dense, Dropout, Activation, LSTM
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasRegressor
from keras.callbacks import ModelCheckpoint
#sciKit for pipeline and CV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

class network(object):
    def __init__(self, X):
        self.model = self.getModel(X)

    def getModel(self,X):
        # create model
        model = Sequential()
        model.add(LSTM(400, input_shape=(X.shape[1],X.shape[2]), return_sequences=True))
        model.add(LSTM(200, input_shape=(X.shape[1],X.shape[2])))
        model.add(Dense(128,activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        return model
    
    def train(self,x,y,epochs=20,batch_size=5,filepath="recent_lstm_model_weights.h5"):
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        callbacks_list = [checkpoint]
        # fit the model
        self.model.fit(x, y, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list)
        self.model = self.load_best_model(filepath)
        return self.model
        
    def load_best_model(self, filepath="recent_lstm_model_weights.h5"):
        return load_model(filepath)