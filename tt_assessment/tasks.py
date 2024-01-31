from celery import Celery
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ARRAY
from sqlalchemy.sql import func
import subprocess
import feedparser
import hashlib
from datetime import datetime
from typing import List
import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging

# Create a Celery instance
app = Celery('tasks', broker='sqla+postgresql://kaustubh:concept@localhost:4111/thetimeisnow')


# Define the PostgreSQL connection string
db_string = 'postgresql://kaustubh:concept@localhost:4111/thetimeisnow'

# Create an engine to connect to the database
engine = create_engine(db_string)

logging.basicConfig(filename='celery_errors.log', level=logging.ERROR)

# Define metadata
metadata = MetaData()

# Define the articles table
articles = Table(
    'articles',
    metadata,
    Column('article_id', Integer, primary_key=True),
    Column('title', String),
    Column('title_details', String),
    Column('published_date', DateTime(timezone=True), default=func.now()),
    Column('url', String),
    Column('source_id', Integer),
    Column('genre_id', ARRAY(String)),
    Column('body', String),
    Column('header', String)
)

# Define a Celery task to insert data into the articles table
@app.task
def insert_into_articles(data):

    try:
        with engine.begin() as connection:
            connection.execute(articles.insert().values(data))
            print("executed")
            
    except Exception as e:
        logging.error(f'Error in insertion: {e}')
        raise
        


# Define a Celery task to retrieve data from the articles table
@app.task
def retrieve_from_articles():
    # Open a connection
    with engine.connect() as connection:
        # Select data from the articles table
        result = connection.execute(articles.select())
        # Fetch all rows
        rows = result.fetchall()
        # Print the rows
        for row in rows:
            print(row)

# Sample data
data = {
    'title': 'Sample Title 5',
    'title_details': 'Sample Title Details',
    'published_date': '2024-01-29 12:00:00' ,
    'url': 'http://example.com',
    'source_id': 101,
    'genre_id': [1,2],
    'body': 'Sample Body',
    'header': 'Sample Header'
}

# # Call the Celery task to insert data into the articles table
# try:
#    # Insert article record
#    insert_into_articles.delay(data)
# except Exception as e:
#    print("Insert failed:", e)
#    logging.error("Insert error:", exc_info=True)


# Start the Celery worker
# worker_command = [
#     'celery',
#     '-A', 'tasks',
#     'worker',
#     '--loglevel=info',
#     '--hostname=brad'
# ]
# subprocess.Popen(worker_command)



insert_into_articles.delay(data)

#insert_into_articles.apply_async(args=[data], queue='brad')
#insert_into_articles(data)

# Call the Celery task to retrieve data from the articles table
#retrieve_from_articles.delay()


with open('celery_errors.log', 'r') as log_file:
    print(log_file.read())
