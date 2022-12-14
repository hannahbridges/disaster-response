import sys
import nltk
nltk.download(['omw-1.4','punkt', 'wordnet', 'stopwords'])

import pandas as pd
import re
import sqlite3
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report


def load_data(database_filepath):
    '''Load data and split into message and category responses.'''
    conn = sqlite3.connect(database_filepath)
    
    df = pd.read_sql('SELECT * FROM messages_cleaned', conn)
    
    category_names= list(df.iloc[:,4:].columns)
    X = df['message'].values
    Y = df[category_names].values
    
    return X,Y,category_names


def tokenize(text):
    '''Tokenize text.'''
    
    #remove punctuation
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    
    words = word_tokenize(text)
    
    #remove stop words
    words = [w for w in words if w not in stopwords.words("english")]
    
    #normalize and lemmatize
    lemmatizer = WordNetLemmatizer()

    tokens = []
    for w in words:
        token = lemmatizer.lemmatize(w).lower().strip()
        tokens.append(token)

    return tokens


def build_model():
    '''Create a pipeline to train a classification model with grid search.'''
    pipeline = Pipeline([
        ('vect',CountVectorizer(tokenizer=tokenize)),
        ('tfidf',TfidfTransformer()),
        ('clf',MultiOutputClassifier(MultinomialNB()))
    ])      
        
    parameters = {
                'clf__estimator__alpha': [0.001, 0.01, 0.1],
                'vect__ngram_range':  [(1,1), (1,2), (2,2)]
    }

    # create grid search object 
    model = GridSearchCV(pipeline,parameters,cv=3,verbose=2)
    return model
    


def evaluate_model(model, X_test, Y_test, category_names):
    '''Evaluate trained model by f-score, precision, recall.'''
    Y_pred = model.predict(X_test)
    for i in range(0,36):
        print(classification_report(Y_test[:,i],Y_pred[:,i]))


def save_model(model, model_filepath):
    '''Save trained model as pickle.'''
    pickle.dump(model , open(model_filepath, "wb"))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()