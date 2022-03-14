import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity    

def greeting(name):
    return 'hello ' + name

def hello():
    return 'Hello World'

def ask(message):
    return 'ANSWER, ' + message

if __name__ == '__main__':
    # load dataset using pandas
    qa = pd.read_csv('data/chat.csv', header=None, sep='\t')
    print(qa) # print dataset

    # create a tf-idf vectorizer
    vectorizer = TfidfVectorizer(lowercase = True, stop_words = 'english')
    X = vectorizer.fit_transform(qa[0])
    question = X.toarray()
    print(question) # print tf-idf matrix
    print(len(question[0])) # print number of questions

    exit_list = ['exit', 'see you later', 'bye', 'quit', 'break', 'stop']
    while True:
        text = input('> ').lower()
        if text in exit_list:
            break
        else:
            # transform the question's input to tf-idf vector
            text_vector = vectorizer.transform([text])
            text_vector = text_vector.toarray()

            # print text_vector
            print(text_vector)

            # find the most similar question
            text_vector = text_vector[0].reshape(1, -1)
            similarity = cosine_similarity(text_vector, question)
            
            # print similarity
            print(similarity)

            # find the index of the most similar question
            index = np.argmax(similarity)
            print(index)

            # print the answer
            answer = qa[1].iloc[index]
            print('Bot : ' + answer)
