import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''Reads data from specified files and returns merged dataframe.'''
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    
    return messages.merge(categories,on='id')


def clean_data(df):
    '''Returns cleaned dataframe with categories converted to binary columns'''
    # split categories into separate columns
    categories = df['categories'].str.split(';',expand=True)
    
    #rename category columns
    row = categories.iloc[0]
    category_colnames = list(row.apply(lambda x: x[0:-2]))
    categories.columns = category_colnames
    
    #convert values to binary
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
        # convert to numeric
        categories[column] = pd.to_numeric(categories[column])
        
    #replace 2s in related column with 1s - probably dodgy data
    categories['related'] = categories['related'].map(lambda x: 1 if x==2 else x)
        
    
    #replace original column with separate binary columns
    df.drop('categories',axis =1,inplace=True)
    df = pd.concat([df,categories],axis=1)
    

    #drop duplicates
    df = df.drop_duplicates()
    
    return df



def save_data(df, database_filename):
    '''Saves dataframe df to specified database'''
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('messages_cleaned', engine, if_exists = 'replace', index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()