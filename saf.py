from pandas import pandas as pd
import numpy as np
import pickle, sys, os, json, csv
import tensorflow.keras as keras
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout
from sklearn.preprocessing import LabelBinarizer
import sklearn.datasets as skds
from pathlib import Path

# For reproducibility
np.random.seed(1237)

# Source file directory
path_train = "/home/munyole/Desktop/fake_news/data/"

data = path_train + "FAKE DETECTOR.csv"

f = open(data, "r")

reader = csv.reader(f)
data = list(reader)

files_train = skds.load_files(path_train,load_content=False)



label_index = files_train.target
label_names = files_train.target_names
labelled_files = files_train.filenames


data_tags = ["id","Status","title","filename"]



###########################################data_list = []




# Read and add data from file to a list
i=0
for f in labelled_files:
    data_list.append((f,label_names[label_index[i]],Path(f).read_text()))
    i += 1

# We have training data available as dictionary filename, category, data
##################33data = pd.DataFrame.from_records(data_list, columns=data_tags)
data = pd.DataFrame.from_records(data, columns=data_tags)

# 20 news groups
###########################################num_labels = 20
num_labels = 48
vocab_size = 15000
batch_size = 100

# lets take 80% data as training and remaining 20% for test.
train_size = int(len(data) * .8)

train_posts = data['id'][:train_size]
train_tags = data['Status'][:train_size]
train_files_names = data['filename'][:train_size]

test_posts = data['id'][train_size:]
test_tags = data['Status'][train_size:]
test_files_names = data['filename'][train_size:]

# define Tokenizer with Vocab Size
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(train_posts)

x_train = tokenizer.texts_to_matrix(train_posts, mode='tfidf')
x_test = tokenizer.texts_to_matrix(test_posts, mode='tfidf')

encoder = LabelBinarizer()
encoder.fit(train_tags)
y_train = encoder.transform(train_tags)
y_test = encoder.transform(test_tags)

model = Sequential()
model.add(Dense(512, input_shape=(vocab_size,)))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(num_labels))
model.add(Activation('softmax'))
model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=30,
                    verbose=1,
                    validation_split=0.1)

# creates a HDF5 file 'my_model.h5'
model.model.save('my_model.h5')

# Save Tokenizer i.e. Vocabulary
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)


score = model.evaluate(x_test, y_test,
                       batch_size=batch_size, verbose=1)

print('Test accuracy:', score[1])

text_labels = encoder.classes_

for i in range(10):
    prediction = model.predict(np.array([x_test[i]]))
    predicted_label = text_labels[np.argmax(prediction[0])]
    print(test_files_names.iloc[i])
    print('Actual label:' + test_tags.iloc[i])
    print("Predicted label: " + predicted_label)


