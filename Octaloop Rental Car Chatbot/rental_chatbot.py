# -*- coding: utf-8 -*-
"""Rental Chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zBKjs0QKHaA_dKmPo2fAAcu9hIq736gY
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
import numpy as np
import json


from nltk.stem.lancaster import LancasterStemmer
import random

# Importing Libraries
import nltk
nltk.download("punkt")

import tensorflow as tf
stemmer = LancasterStemmer()
# Importing Libraries needed for Tensorflow
import tensorflow as tf
import numpy as np

from google.colab import files
uploaded = files.upload()

# Reset the default graph
tf.compat.v1.reset_default_graph()

# Load intents from JSON file
with open("intents.json") as json_data:
    intents = json.load(json_data)

intents

stemmer = LancasterStemmer()

words = []
documents = []
classes = []

# Define a list for punctuation marks to ignore
ignore = ["?"]

# Loop through each intent and pattern
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        # Tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent["tag"]))

        # Add the tag to 'classes' if it's not already present
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Stem and lowercase the words, removing duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore]
words = sorted(list(set(words)))

# Remove duplicate classes
classes = sorted(list(set(classes)))

# Create training data
training = []
output = []

# Create an empty array for output
output_empty = [0] * len(classes)

# Create the training set and bag of words for each sentence
for doc in documents:
    bag = [0] * len(words)

    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]

    # Create the bag of words array
    for w in words:
        if w in pattern_words:
            bag[words.index(w)] = 1
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])


random.shuffle(training)

# Convert training data to a numpy array
training = np.array(training)

# Create training lists
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# Build a Keras model
model = Sequential()
model.add(Dense(10, input_shape=(len(train_x[0]),), activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dense(10, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_x, train_y, epochs=1000, batch_size=8, verbose=1)

# Save the model
model.save("model.h5")  # Save the model to a file

model.summary()

import pickle
import json
import nltk
import random
import numpy as np
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Load intents from JSON file
with open("intents.json") as json_data:
    intents = json.load(json_data)

model = load_model("model.h5")
stemmer = LancasterStemmer()

# Load training data
pickle.dump({"words": words, "classes": classes, "train_x": train_x, "train_y": train_y}, open("training_data", "wb"))
data = pickle.load(open("training_data", "rb"))
words = data["words"]
classes = data["classes"]
train_x = data["train_x"]
train_y = data["train_y"]

# Cleaning User Input
def clean_up_sentence(sentence):
    # Tokenizing the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # Stemming each word from the user's input
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# Returning bag of words array: 0 or 1 for each word in the bag that exists in our words list
def bow(sentence, words, show_details=False):

    sentence_words = clean_up_sentence(sentence)

    # Generating bag of words from the sentence that the user entered
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("Found in bag: %s" % w)
    return np.array(bag)

# Adding some context to the conversation for better results
context = {}

ERROR_THRESHOLD = 0.25
def classify(sentence):
    # Generating probabilities from the model
    results = model.predict(np.array([bow(sentence, words)]))[0]

    # Filter out predictions below a threshold
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]

    # Sorting by the strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))

    # Return a tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    response_text = ""

    # If we have a classification then find the matching intent tag
    if results:
        while results:
            for i in intents['intents']:
                # Find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # Set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details:
                            print('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # Check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                            (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details:
                            print('tag:', i['tag'])

                        # A random response from the intent
                        response_text = random.choice(i['responses'])

            results.pop(0)

    return response_text

pip install gradio

import gradio as gr

iface = gr.Interface(
    fn=lambda User: response(User),
    inputs=gr.Textbox(),
    outputs="text",
    layout="vertical",
    title="Rental Car Chatbot",
    description="Ask any car-related question, and the chatbot will respond.",
    output_title="Chatbot",
)
iface.launch()