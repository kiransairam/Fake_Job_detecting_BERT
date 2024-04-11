# -*- coding: utf-8 -*-
"""Fake Job Hands on with BERT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IWD13thMAmU4pTDJBLgstHtCgSjTX7ap
"""



from sklearn.model_selection import train_test_split

"""Hands on with BERT

###Setup
"""

# A dependency of the preprocessing for BERT inputs
!pip install -q tensorflow-text

!pip install -q tf-models-official

import os
import shutil

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import optimization  # to create AdamW optmizer

import matplotlib.pyplot as plt

import numpy as np


tf.get_logger().setLevel('ERROR')



"""Downloading and uploading the dataset"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

df = pd.read_csv('fake_job_postings.csv')

print(df.head())

"""1- (1pt) Data is stored as a comma separated file. Store this file in a pandas dataframe. Append “title” to “description” with a space in between and store it as a new column, change the type of this column to string Note: you can convert column c in dataframe df to string using this syntax: df["c"]= df["c"].astype(str)"""

df['title_description'] = df['title'] + ' ' + df['description']

df['title_description'] = df['title_description'].astype(str)

print(df.head())

df_new = df[['title_description', 'fraudulent']]

df_1_tittle = df_new['title_description']
df_2_fraud = df_new['fraudulent']

df_1_train, df_1_test, df_2_train, df_2_test = train_test_split(df_1_tittle, df_2_fraud, test_size=0.20)

df_1_train, df_1_val, df_2_train, df_2_val = train_test_split(df_1_train, df_2_train , test_size=0.20)

"""###3- (1 pt) You can use tf.data.Dataset.from_tensor_slices function as follows to create tf.data.Dataset objects from train_x (title+description) and train_y(fraudulent) variables in the training data:"""

train_ds = tf.data.Dataset.from_tensor_slices((df_1_train , df_2_train))
train_ds= train_ds.batch(32)

val_ds = tf.data.Dataset.from_tensor_slices((df_1_val , df_2_val))
val_ds= val_ds.batch(32)

test_ds = tf.data.Dataset.from_tensor_slices((df_1_test , df_2_test))
test_ds= test_ds.batch(32)

"""###4- (3 pts) Now you can pass train_ds and validation_ds directly to your model to train and evaluateit (similar to this tensorflow tutorial). Use “sigmoid” for the final activation layer and set “from_logits=False” in BinaryCrossEntropyLoss.

"""

#@title Choose a BERT model to fine-tune

bert_model_name = 'small_bert/bert_en_uncased_L-8_H-512_A-8'  #@param ["bert_en_uncased_L-12_H-768_A-12", "bert_en_cased_L-12_H-768_A-12", "bert_multi_cased_L-12_H-768_A-12", "small_bert/bert_en_uncased_L-2_H-128_A-2", "small_bert/bert_en_uncased_L-2_H-256_A-4", "small_bert/bert_en_uncased_L-2_H-512_A-8", "small_bert/bert_en_uncased_L-2_H-768_A-12", "small_bert/bert_en_uncased_L-4_H-128_A-2", "small_bert/bert_en_uncased_L-4_H-256_A-4", "small_bert/bert_en_uncased_L-4_H-512_A-8", "small_bert/bert_en_uncased_L-4_H-768_A-12", "small_bert/bert_en_uncased_L-6_H-128_A-2", "small_bert/bert_en_uncased_L-6_H-256_A-4", "small_bert/bert_en_uncased_L-6_H-512_A-8", "small_bert/bert_en_uncased_L-6_H-768_A-12", "small_bert/bert_en_uncased_L-8_H-128_A-2", "small_bert/bert_en_uncased_L-8_H-256_A-4", "small_bert/bert_en_uncased_L-8_H-512_A-8", "small_bert/bert_en_uncased_L-8_H-768_A-12", "small_bert/bert_en_uncased_L-10_H-128_A-2", "small_bert/bert_en_uncased_L-10_H-256_A-4", "small_bert/bert_en_uncased_L-10_H-512_A-8", "small_bert/bert_en_uncased_L-10_H-768_A-12", "small_bert/bert_en_uncased_L-12_H-128_A-2", "small_bert/bert_en_uncased_L-12_H-256_A-4", "small_bert/bert_en_uncased_L-12_H-512_A-8", "small_bert/bert_en_uncased_L-12_H-768_A-12", "albert_en_base", "electra_small", "electra_base", "experts_pubmed", "experts_wiki_books", "talking-heads_base"]

map_name_to_handle = {
    'bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/3',
    'bert_en_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_cased_L-12_H-768_A-12/3',
    'bert_multi_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_multi_cased_L-12_H-768_A-12/3',
    'small_bert/bert_en_uncased_L-2_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-2_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-2_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-2_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-4_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-4_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-4_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-4_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-6_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-6_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-6_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-6_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-8_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-8_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-8_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-8_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-10_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-10_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-10_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-10_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-12_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-12_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-12_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-768_A-12/1',
    'albert_en_base':
        'https://tfhub.dev/tensorflow/albert_en_base/2',
    'electra_small':
        'https://tfhub.dev/google/electra_small/2',
    'electra_base':
        'https://tfhub.dev/google/electra_base/2',
    'experts_pubmed':
        'https://tfhub.dev/google/experts/bert/pubmed/2',
    'experts_wiki_books':
        'https://tfhub.dev/google/experts/bert/wiki_books/2',
    'talking-heads_base':
        'https://tfhub.dev/tensorflow/talkheads_ggelu_bert_en_base/1',
}

map_model_to_preprocess = {
    'bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'bert_en_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_cased_preprocess/3',
    'small_bert/bert_en_uncased_L-2_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-2_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-2_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-2_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-4_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-4_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-4_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-4_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-6_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-6_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-6_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-6_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-8_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-8_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-8_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-8_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-10_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-10_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-10_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-10_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-12_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-12_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-12_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'bert_multi_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_multi_cased_preprocess/3',
    'albert_en_base':
        'https://tfhub.dev/tensorflow/albert_en_preprocess/3',
    'electra_small':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'electra_base':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'experts_pubmed':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'experts_wiki_books':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'talking-heads_base':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
}

tfhub_handle_encoder = map_name_to_handle[bert_model_name]
tfhub_handle_preprocess = map_model_to_preprocess[bert_model_name]

print(f'BERT model selected           : {tfhub_handle_encoder}')
print(f'Preprocess model auto-selected: {tfhub_handle_preprocess}')

"""##The preprocessing model

Text inputs need to be transformed to numeric token ids and arranged in several Tensors before being input to BERT. TensorFlow Hub provides a matching preprocessing model for each of the BERT models discussed above, which implements this transformation using TF ops from the TF.text library. It is not necessary to run pure Python code outside your TensorFlow model to preprocess text.

The preprocessing model must be the one referenced by the documentation of the BERT model, which you can read at the URL printed above. For BERT models from the drop-down above, the preprocessing model is selected automatically.

Note: You will load the preprocessing model into a hub.KerasLayer to compose your fine-tuned model. This is the preferred API to load a TF2-style SavedModel from TF Hub into a Keras model.
"""

bert_preprocess_model = hub.KerasLayer(tfhub_handle_preprocess)

text_test = ['this is such an amazing movie!']
text_preprocessed = bert_preprocess_model(text_test)

print(f'Keys       : {list(text_preprocessed.keys())}')
print(f'Shape      : {text_preprocessed["input_word_ids"].shape}')
print(f'Word Ids   : {text_preprocessed["input_word_ids"][0, :12]}')
print(f'Input Mask : {text_preprocessed["input_mask"][0, :12]}')
print(f'Type Ids   : {text_preprocessed["input_type_ids"][0, :12]}')



"""## Using the BERT model"""

bert_model = hub.KerasLayer(tfhub_handle_encoder)

bert_results = bert_model(text_preprocessed)

print(f'Loaded BERT: {tfhub_handle_encoder}')
print(f'Pooled Outputs Shape:{bert_results["pooled_output"].shape}')
print(f'Pooled Outputs Values:{bert_results["pooled_output"][0, :12]}')
print(f'Sequence Outputs Shape:{bert_results["sequence_output"].shape}')
print(f'Sequence Outputs Values:{bert_results["sequence_output"][0, :12]}')

"""## Define your model"""

def build_classifier_model():
  text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
  preprocessing_layer = hub.KerasLayer(tfhub_handle_preprocess, name='preprocessing')(text_input)
  Bert_layer = hub.KerasLayer(tfhub_handle_encoder, trainable=True, name='BERT_encoder')(preprocessing_layer)
  Bert_output = Bert_layer['pooled_output']
  net = tf.keras.layers.Dropout(0.1)(Bert_output)
  output_layer = tf.keras.layers.Dense(1, activation="sigmoid", name='classifier')(net)
  return tf.keras.Model(text_input, output_layer)

classifier_model = build_classifier_model()
tf.keras.utils.plot_model(classifier_model)

"""### Loss function"""

# loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)
# metrics = tf.metrics.BinaryAccuracy()


loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)
metrics = tf.keras.metrics.AUC()

"""### Optimizer"""

epochs = 5
steps_per_epoch = tf.data.experimental.cardinality(train_ds).numpy()
num_train_steps = steps_per_epoch * epochs
num_warmup_steps = int(0.1*num_train_steps)

init_lr = 3e-5
optimizer = optimization.create_optimizer(init_lr=init_lr,
                                          num_train_steps=num_train_steps,
                                          num_warmup_steps=num_warmup_steps,
                                          optimizer_type='adamw')



"""### Loading the BERT model and training"""

classifier_model.compile(optimizer=optimizer,
                         loss=loss,
                         metrics=metrics)

print(f'Training model with {tfhub_handle_encoder}')
history = classifier_model.fit(x=train_ds,
                               validation_data=val_ds,
                               epochs=epochs)

"""### Evaluate the model"""

loss, accuracy = classifier_model.evaluate(val_ds)

print(f'Loss: {loss}')
print(f'Accuracy: {accuracy}')

"""### Plot the accuracy and loss over time"""

history_dict.keys()

history_dict = history.history
print(history_dict.keys())

acc = history_dict['auc']
val_acc = history_dict['val_auc']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)
fig = plt.figure(figsize=(10, 6))
fig.tight_layout()

plt.subplot(2, 1, 1)
# "bo" is for "blue dot"
plt.plot(epochs, loss, 'r', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
# plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(epochs, acc, 'r', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')

dataset_name = 'fake'
saved_model_path = './{}_bert'.format(dataset_name.replace('/', '_'))

classifier_model.save(saved_model_path, include_optimizer=False)



"""Use Area Under Curve (AUC) (https://www.tensorflow.org/api_docs/python/tf/keras/metrics/AUC ) metric to evaluate your model. As data is severely imbalanced, accuracy is not a meaningful metric. Use early stopping to stop the training if there is no improvement in the validation AUC. Tune the learning rate in the range (5e-5, 3e-5, 2e-5, and 1e-5)"""

import tensorflow as tf

tf.keras.metrics.AUC(
    num_thresholds=200,
    curve='ROC',
    summation_method='interpolation',
    #name=None,
    #dtype=None,
    #thresholds=None,
    multi_label=False,
    #num_labels=None,
    label_weights=500,
    from_logits=False
)

# classifier_model.compile(optimizer=optimizer,
#               loss='binary_crossentropy',
#               metrics=[tf.keras.metrics.AUC()])

from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler

learning_rates = [5e-5, 3e-5, 2e-5, 1e-5]
epochs = 5

es = EarlyStopping(monitor='val_auc', mode='max', patience=5, verbose=1, restore_best_weights=True)
for lr in learning_rates:
    optimizer = tf.keras.optimizers.Adam(learning_rate=lr)
    classifier_model.compile(optimizer=optimizer,
              loss='binary_crossentropy',
              metrics=[tf.keras.metrics.AUC()])

history = classifier_model.fit(x=train_ds,
                                   validation_data=val_ds,
                                   epochs=epochs,
                                   callbacks=[es],
                                   verbose=1)

# from tensorflow.keras.callbacks import EarlyStopping

# es = EarlyStopping(monitor='val_auc', mode='max', patience=5, verbose=1, restore_best_weights=True)

# classifier_model.compile(optimizer=optimizer,
#               loss='binary_crossentropy',
#               metrics=[tf.keras.metrics.AUC()])

#history = classifier_model.fit(x=train_ds,
#                               validation_data=val_ds,
#                               epochs=epochs,
#                               callbacks=[es])


# epochs = 10

# history = classifier_model.fit(x=train_ds,
#                                validation_data=val_ds,
#                                epochs=epochs,
#                                callbacks=[es],
#                                verbose=1)

loss, acc = classifier_model.evaluate(val_ds)

print(f'Loss: {loss}')
print(f'Accuracy: {accuracy}')

"""5- (2 pt) Once training is completed, use model.predict to get the predictions for the validation data and compare it to the true labels. Use sklearn.metrics.confusion_matrix toget the confusion matrix and sklearn.metrics.classification_report to get precision, recall, and F1 score for the fraudulent class."""

import numpy as np
y_true = np.array([])
for samples, target in val_ds:
  y_true = np.append(y_true, target.numpy())

# y_pred_probs = classifier_model.predict(val_ds)
# y_pred = np.argmax(y_pred_probs, axis=1)

y_pred = classifier_model.predict(val_ds)

y_pred_prob = y_pred

y_pred = np.where(y_pred > 0.5, 1,0)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_true, y_pred)
print(cm)

"""True Negatives (TN): 2696

False Positives (FP): 15

False Negatives (FN): 56

True Positives (TP): 94





"""

from sklearn.metrics import classification_report


print(classification_report(y_true, y_pred))

"""The classification report provides more detailed performance metrics for the model, including precision, recall, and F1-score for both classes (fraudulent and non-fraudulent) as well as overall accuracy, macro-averaged F1-score, and weighted-averaged F1-score.

Overall, the model appears to perform well on the non-fraudulent class (high precision, recall, and F1-score), but less well on the fraudulent class (lower precision, recall, and F1-score). This suggests that the model may need further tuning or refinement in order to better detect fraudulent transactions.

#Undersampling
"""

# survived = df[df['survived']==1]
# deceased = df[df['survived']==0]
# deceased = deceased.sample(n=len(survived), random_state=101)
# df = pd.concat([survived,deceased],axis=0)


train_df = pd.DataFrame(columns=['job_title_description', 'fraudulent'])
train_df['job_title_description'] = df_1_train
train_df['fraudulent'] = df_2_train

fraudulent = train_df[train_df['fraudulent']==1]
real = train_df[train_df['fraudulent']==0]

real = real.sample(n=len(fraudulent), random_state=101)
traindf = pd.concat([fraudulent, real],axis=0)

traindf = traindf.sample(frac=1).reset_index(drop=True)
traindf = traindf.sample(frac=1).reset_index(drop=True)
traindf = traindf.sample(frac=1).reset_index(drop=True)
traindf = traindf.sample(frac=1).reset_index(drop=True)


train_ds_bal = tf.data.Dataset.from_tensor_slices((traindf.job_title_description, traindf.fraudulent))
train_ds_bal= train_ds_bal.batch(32)

history = classifier_model.fit(x=train_ds_bal,
                                   validation_data=val_ds,
                                   epochs=5,
                                   callbacks=[es],
                                   verbose=1)

loss, auc = classifier_model.evaluate(val_ds)

history_dict.keys()

history_dict = history.history
print(history_dict.keys())

auc = history_dict['auc_5']
val_auc = history_dict['val_auc_5']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(auc) + 1)
fig = plt.figure(figsize=(10, 6))
fig.tight_layout()

plt.subplot(2, 1, 1)
# "bo" is for "blue dot"
plt.plot(epochs, loss, 'r', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
# plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(epochs, auc, 'r', label='Training auc')
plt.plot(epochs, val_auc, 'b', label='Validation auc')
plt.title('Training and validation AUC')
plt.xlabel('Epochs')
plt.ylabel('AUC')
plt.legend(loc='lower right')

y_pred_balanced = classifier_model.predict(val_ds)

y_pred_balanced = np.where(y_pred_balanced > 0.5, 1,0)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_true, y_pred_balanced)
print(cm)

"""2710 true negatives (non-fraudulent cases correctly predicted)
2 false positives (non-fraudulent cases incorrectly predicted as fraudulent)
14 false negatives (fraudulent cases incorrectly predicted as non-fraudulent)
135 true positives (fraudulent cases correctly predicted).
"""

from sklearn.metrics import classification_report

print(classification_report(y_true, y_pred_balanced,target_names = ['0', '1']))

"""**it After undersampling, the model's precision, recall, and f1-score for the minority class (1) decreased, but its recall increased slightly. This means that the model is predicting more true positives for the minority class, but also more false positives. The overall accuracy of the model did not change significantly, and the macro average and weighted average f1-scores stayed relatively stable.**

**Comparing the classification reports before and after undersampling, we can see that undersampling has decreased the recall of the fraudulent class (1.0) from 0.70 to 0.75, but it has increased the precision from 0.84 to 0.73. As a result, the F1-score of the fraudulent class has decreased slightly from 0.76 to 0.74.**

##7- (1pt) Evaluate your best model on the test data. As before, report AUC, confusion matrix,precision, recall and F1
"""

t_loss, t_auc = classifier_model.evaluate(test_ds)

y_pred_balanced_test = classifier_model.predict(test_ds)

y_pred_balanced_test = np.where(y_pred_balanced_test > 0.5, 1,0)

import numpy as np

y_true_test = np.array([])
for samples, target in test_ds:
  y_true_test = np.append(y_true_test, target.numpy())

from sklearn.metrics import confusion_matrix
cf_test = confusion_matrix(y_true_test, y_pred_balanced_test)
print(cf_test)

from sklearn.metrics import classification_report

print(classification_report(y_true_test, y_pred_balanced_test))

"""**The test dataset report shows similar trends to the validation dataset report after undersampling. The F1-score for the fraudulent class has increased to 0.77 from 0.74 before undersampling, indicating that undersampling has helped in improving the model's ability to correctly identify fraudulent transactions.**

**##Oversampling using text augmentation**
"""

#print(len(job_title_description))
#print(len(fraudulent))

#aug_df = pd.DataFrame(columns=['job_title_description', 'fraudulent'])

# aug = nac.KeyboardAug()
# augmented_text = aug.augment()


# temp_df = pd.DataFrame(columns=['job_title_description', 'fraudulent'])
# temp_df['job_title_description'] = df_1_train
# temp_df['fraudulent'] = df_2_train

# Count fraudulent entries
# count_fraudulent = temp_df_o.groupby('fraudulent').count()
# count_fraudulent.reset_index(inplace=True)

# print("Original:")
# print(text)
# print("Augmented Text:")
# print(augmented_text)

from sklearn.model_selection import train_test_split
from nlpaug.augmenter.word import WordEmbsAug
from tqdm import tqdm
import nlpaug.augmenter.word as naw

# import necessary libraries
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from tqdm import tqdm
# from sklearn.utils import shuffle
# #import numpy as np
# import tensorflow as tf
#from transformers import pipeline, set_seed
#from transformers import AutoTokenizer, TFAutoModelForSequenceClassification

# # Define the data augmentation function
# def augment_text(df, samples=10000, pr=0.2):
#     # Initialize the augmenter
#     aug = naw.SynonymAug(aug_src='wordnet')

#     # Set the probability of augmentation
#     aug.prob = pr

#     # Select the minority class samples
#     df_fraud = df[df['fraudulent'] == 1].reset_index(drop=True)

#     # Generate augmented samples
#     new_text = []
#     for i in tqdm(np.random.randint(0, len(df_fraud), samples)):
#         text = df_fraud.loc[i, 'job_title_description']
#         augmented_text = aug.augment(text)
#         new_text.append(augmented_text)

#     # Create the new dataframe with augmented samples
#     new = pd.DataFrame({'job_title_description': new_text, 'fraudulent': 1})
#     df_augmented = pd.concat([df, new], ignore_index=True)

#     return df_augmented

# # Call the data augmentation function on the training dataset
# train_augmented = augment_text(temp_df)

!pip install transformers

import nltk
!pip install nlpaug
import nlpaug.augmenter.word as naw

temp_df = pd.DataFrame(columns=['job_title_description', 'fraudulent'])
temp_df['job_title_description'] = df_1_train
temp_df['fraudulent'] = df_2_train

fraudulent_data = temp_df[temp_df['fraudulent']==1]

aug = naw.ContextualWordEmbsAug(
    model_path='bert-base-uncased', action="insert")

aug_data = pd.DataFrame(columns=['job_title_description', 'fraudulent'])
for text in fraudulent_data['job_title_description']:
  augmented_text = aug.augment(text)
  df2 = {'job_title_description': augmented_text, 'fraudulent':1}
  aug_data = aug_data.append(df2, ignore_index=True)

aug_data.shape
aug_data.describe()

#fraudulent_data = temp_df[temp_df['fraudulent']==1]

#fraudulent_data = temp_df[temp_df['fraudulent']==1]

# aug = naw.ContextualWordEmbsAug(
#     model_path='bert-base-uncased', action="insert")

# aug_data = pd.DataFrame(columns=['title_description','fraudulent'])
# for text in fraudulent_data['title_description']:
#   augmented_text = aug.augment(text)
#   df2 = {'title_description': augmented_text, 'fraudulent':1}
#   aug_data = aug_data.apped(df2, ignore_index=True)

# fraudulent_data = train_df[train_df['fraudulent'] == 1]

# aug = naw.ContextualWordEmbsAug(
#     model_path='bert-base-uncased', action="insert")

# aug_data = pd.DataFrame(columns=['text', 'fraudulent'])
# for text in fraudulent_data['text']:
#     augmented_text = aug.augment(text)
#     df2 = {'text': augmented_text, 'fraudulent': 1}
#     aug_data = aug_data.append(df2, ignore_index=True)


print("Original:")
print(temp_df)
print("Augmented Text:")
print(aug_data)

# import plotly.express as px

# fig = px.bar(train_augmented , x='fraudulent', y='job_title_description',
#              color='fraudulent',
#              labels={'job_title_description': 'Count', 'fraudulent': 'Fraudulent'})
# fig.show()

# augmented_text = aug.augment(train_df['title_description'].tolist())

# # create a new dataframe with the augmented data and the corresponding target data
# aug_train_df = pd.DataFrame({'title_description': augmented_text, 'fraudulent': train_df['fraudulent']})

# # create new datasets from the augmented data
# aug_train_ds = tf.data.Dataset.from_tensor_slices((aug_train_df['title_description'].values, aug_train_df['fraudulent'].values))
# aug_train_ds = aug_train_ds.batch(32)

# fit the classifier model on the augmented data
# history = classifier_model.fit(x=aug_train_ds,
#                                validation_data=val_ds,
#                                epochs=5,
#                                callbacks=[es],
#                                verbose=1)

print(aug_data.dtypes)

#train_ds_bal_ov = tf.data.Dataset.from_tensor_slices((aug_data['job_title_description'].to_numpy(), aug_data['fraudulent'].to_numpy()))

#aug_data['job_title_description'] = aug_data['job_title_description'].apply(lambda x: ' '.join(x))

# job_title_description_list = aug_data['job_title_description'].tolist()
# fraudulent_list = aug_data['fraudulent'].tolist()

aug_data['job_title_description'] = aug_data['job_title_description'].apply(lambda x: ' '.join(x))


aug_data['fraudulent'] = aug_data['fraudulent'].astype(int)

aug_data

train_ds_bal_ov_o = tf.data.Dataset.from_tensor_slices((aug_data['job_title_description'], aug_data['fraudulent']))
train_ds_bal_ov_o_o = train_ds_bal_ov_o.batch(32)

#aug_data[column_name] = aug_data[column_name].astype(str)
#aug_data['fraudulent'] = aug_data['fraudulent'].astype(int)

#x_train = np.array(aug_data['job_title_description'])


history = classifier_model.fit(x=train_ds_bal_ov_o_o,
                                   validation_data=val_ds,
                                   epochs=5,
                                   callbacks=[es],
                                   verbose=1)

loss, auc_bal = classifier_model.evaluate(val_ds)

history_dict.keys()

history_dict = history.history
print(history_dict.keys())

acc = history_dict['auc_5']
val_acc = history_dict['val_auc_5']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)
fig = plt.figure(figsize=(10, 6))
fig.tight_layout()

plt.subplot(2, 1, 1)
# "bo" is for "blue dot"
plt.plot(epochs, loss, 'r', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
# plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(epochs, acc, 'r', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')

y_pred_balanced_over = classifier_model.predict(val_ds)

y_pred_balanced_over = np.where(y_pred_balanced > 0.5, 1,0)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_true, y_pred_balanced_over)
print(cm)

from sklearn.metrics import classification_report

print(classification_report(y_true, y_pred_balanced_over))

"""**it seems that the oversampling dataset performs better than the other two datasets for detecting fraudulent job postings. The oversampling dataset has a higher F1-score for the minority class (fraudulent), indicating that it is better at correctly identifying fraudulent postings.**

**How does chatGPT solves this problem?**

**Method 1**
"""

import pandas as pd
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split

# Load the dataset into a pandas dataframe and append "title" to "description"
df = pd.read_csv("job_postings.csv")
df['title_description'] = df['title'] + ' ' + df['description']
df['title_description'] = df['title_description'].astype(str)

# Create train, validation, and test datasets
df_new = df[['title_description', 'fraudulent']]
df_1_tittle = df_new['title_description']
df_2_fraud = df_new['fraudulent']
df_1_train, df_1_test, df_2_train, df_2_test = train_test_split(df_1_tittle, df_2_fraud, test_size=0.20)
df_1_train, df_1_val, df_2_train, df_2_val = train_test_split(df_1_train, df_2_train , test_size=0.20)

# Create tf.data.Dataset objects from the training data
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_ds = tf.data.Dataset.from_tensor_slices((df_1_train , df_2_train))
train_ds = train_ds.shuffle(len(df_1_train)).batch(32)
train_ds = train_ds.map(lambda x, y: (tokenizer(x, padding=True, truncation=True, return_tensors='tf'), y))

# Create tf.data.Dataset objects from the validation data
val_ds = tf.data.Dataset.from_tensor_slices((df_1_val , df_2_val))
val_ds = val_ds.batch(32)
val_ds = val_ds.map(lambda x, y: (tokenizer(x, padding=True, truncation=True, return_tensors='tf'), y))

# Create tf.data.Dataset objects from the test data
test_ds = tf.data.Dataset.from_tensor_slices((df_1_test , df_2_test))
test_ds = test_ds.batch(32)
test_ds = test_ds.map(lambda x, y: (tokenizer(x, padding=True, truncation=True, return_tensors='tf'), y))

# Load the pre-trained BERT model and add a classification layer
bert_model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
input_ids = tf.keras.layers.Input(shape=(None,), dtype=tf.int32, name="input_ids")
attention_mask = tf.keras.layers.Input(shape=(None,), dtype=tf.int32, name="attention_mask")
outputs = bert_model({'input_ids': input_ids, 'attention_mask': attention_mask})[0]
model = tf.keras.models.Model(inputs=[input_ids, attention_mask], outputs=[outputs])

# Compile the model with binary cross-entropy loss and Adam optimizer
model.compile(optimizer=tf.keras.optimizers.Adam(lr=2e-5), loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

# Train the model for 3 epochs
model.fit(train_ds, validation_data=val_ds, epochs=3)

# Evaluate the model on the test dataset
model.evaluate(test_ds)

"""**Diffrence Between the code we have chatGPT generated code**

**Preprocessing: In the code we have, the preprocessing is done using the preprocessing_layer defined in build_classifier_model() instead of being done separately before defining the model.**

**Metrics: The metrics used for evaluation are different. In the code we have, the metric used is AUC, while in my code, it is accuracy.**

**Optimizer: In the we have, the optimizer used is AdamW, which is a variant of Adam optimizer that is designed for use with weight decay, while in GPT code, used the standard Adam optimizer.**

**Training and evaluation: The training and evaluation are done using different functions. In the code you provided, the training is done using classifier_model.fit() function and evaluation is done using classifier_model.evaluate() function, while in GPT code used the tf.keras.Model subclassing API for training and evaluation.**

**Saving the model: The code you provided saves the model using the saved_model_path specified in the code, while in my code, I did not include model saving.**

**Overall, both codes aim to fine-tune a BERT model on the job postings dataset, but they differ in some implementation details such as preprocessing, metrics, optimizer, and model training and evaluation functions.**
"""



"""**Method 2**"""

import tensorflow as tf
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def tokenize_text(text, tokenizer, max_seq_length):
    input_ids = []
    attention_masks = []
    for sentence in text:
        encoded = tokenizer.encode_plus(
            text=sentence,
            add_special_tokens=True,
            max_length=max_seq_length,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='tf',
            truncation=True
        )
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])
    return tf.concat(input_ids, axis=0), tf.concat(attention_masks, axis=0)

max_seq_length = 512
train_input_ids, train_attention_masks = tokenize_text(train_data['title_description'], tokenizer, max_seq_length)
val_input_ids, val_attention_masks = tokenize_text(val_data['title_description'], tokenizer, max_seq_length)
test_input_ids, test_attention_masks = tokenize_text(test_data['title_description'], tokenizer, max_seq_length)

train_labels = tf.convert_to_tensor(train_data['fraudulent'])
val_labels = tf.convert_to_tensor(val_data['fraudulent'])
test_labels = tf.convert_to_tensor(test_data['fraudulent'])


from transformers import TFBertForSequenceClassification
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)




epochs = 3
batch_size = 8
steps_per_epoch = len(train_data) // batch_size

optimizer = tf.keras.optimizers.Adam(lr=2e-5)

model.compile(optimizer=optimizer, loss=model.compute_loss, metrics=['accuracy'])

history = model.fit(
    x=[train_input_ids, train_attention_masks],
    y=train_labels,
    validation_data=([val_input_ids, val_attention_masks], val_labels),
    epochs=epochs,
    batch_size=batch_size,
    steps_per_epoch=steps_per_epoch
)

"""**Model architecture: The model architecture is different. The code GPT generated uses a pre-trained BERT model and adds a classification layer on top of it, while the code we have provided uses a pre-trained BERT model specifically designed for sequence classification tasks.**

**Loss function: The loss function used is different. The code GPT generated uses binary cross-entropy loss, while the code GPT provided uses sparse categorical cross-entropy loss.**

**Optimizer: The optimizer used is different. The code GPT generated uses the AdamW optimizer, while the code you provided uses the Adam optimizer.**

**Metrics: The metrics used to evaluate the model are different. The code GPT generated uses the AUC metric, while the code you provided uses the accuracy metric.**

**Training: The code GPT generated includes code to fine-tune the pre-trained BERT model on the job postings dataset, while the code we have provided assumes that the pre-trained BERT model is already specifically designed for sequence classification tasks and does not include any fine-tuning.**

**Overall, the approach GPT provided includes fine-tuning a pre-trained BERT model on the job postings dataset, while the approach we assumes a pre-trained BERT model specifically designed for sequence classification tasks.**
"""