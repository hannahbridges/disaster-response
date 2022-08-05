# Disaster Response Pipeline Project

## Project Motivation
This project uses pre-labelled tweets from real disaster events provided by Figure Eight and Udacity as part of the Data Science Nanodegree to classify messages and identify where a disaster response is needed.

The project is divided into 3 parts:
1. ETL pipeline to prepare the raw data and load into a SQLite database
2. ML pipeline to train an NLP classifier with grid search to predict which categories a message belongs to
3. Web app to display visualizations of the training data and predict the categories for an input message

## Dependencies
Python 3.5+
Libraries: NumPy, Pandas, Scikit-Learn, NLTK, SQLAlchemy, SQLite3, Pickle, Flask, Plotly

## Installing
To clone the git repository:
git clone https://github.com/hannahbridges/disaster-response.git

## Running the Program:
1. Run the following commands in the project's root directory:
	- To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`
	
2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

## Licensing, Authors, Acknowledgements, etc.

Thanks to Udacity and Figure Eight for providing the data used in this project. 