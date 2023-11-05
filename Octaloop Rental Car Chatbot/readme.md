Rental Car Chatbot Development Guide
Introduction
This guide provides a detailed overview of the steps involved in coding a Rental Car Chatbot using Python, Gradio, and TensorFlow. The chatbot is designed to answer questions related to rental cars and uses a neural network-based model for intent classification.

Note: Use google colab to run/test the project, i have added intent.json(dataset) in the directory.

Tools and Technologies Used
Python
Gradio
NLTK (Natural Language Toolkit)
NumPy
TensorFlow

Step 1: Setting Up the Development Environment
Install Python: Ensure you have Python 3.x installed on your system.

Install Required Libraries:

Install Gradio: pip install gradio
Install NLTK: pip install nltk
Install NumPy: pip install numpy
Install TensorFlow: pip install tensorflow

Step 2: Data Preparation
Created a JSON file (intents.json) that contains the following:
tag: Intent tag.
patterns: An array of patterns (questions or statements) related to the intent.
responses: An array of possible responses for the intent.
Data Structure: Define the structure for the intents. Each intent have a unique tag, an array of patterns, and an array of responses. For example:
{
"tag": "greeting",
"patterns": ["Hi", "Hello", "Good day"],
"responses": ["Hello, thanks for visiting", "Hi there, how can I help?"]
}

Step 3: Data Preprocessing
Initialize NLTK: Import NLTK and initialize a stemmer (e.g., LancasterStemmer) for word stemming.

Tokenization: Tokenize the patterns in intents.json to split sentences into individual words.

Stemming: Stem each word in the tokenized patterns to reduce words to their root form (e.g., "running" becomes "run").

Word Vocabulary: Created a list of unique words from the tokenized and stemmed patterns.

Step 4: Intent Classification Model
Create Training Data: Generated training data for neural network model. This data consisted of input patterns (bag of words) and corresponding output labels (intents).
Neural Network Model: Build a neural network model using TensorFlow's Keras API.

Compile Model: Compiled the model using the Adam optimizer and categorical cross-entropy loss function.

Train Model: Trained the model using the training data. On 1000 the number of epochs, 8 batch size.

Save Model: Saved the trained model as model.h5 for later use.

Step 5: Chatbot Interface with Gradio
Initialize Gradio: Import Gradio and create a Gradio interface.

Defined a function that takes user input and returns chatbot responses.
User Input: Use a Gradio Textbox component to take user input as text.

Response Output: Use a Gradio Text component to display chatbot responses.

Deployment: Launch the Gradio interface, making the chatbot accessible through a web browser.

Step 6: Testing and Interaction
Access the chatbot interface via a web browser.

Enter car-related questions or statements in the text box and click "submit" to interact with the chatbot.
