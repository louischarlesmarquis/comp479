import nltk
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import os

# Download the NLTK tokenizer resources
#nltk.download('punkt')

# Function to parse each Reuters-21578 file and extract the article text and headline
def extract_articles_from_sgm(file_path):
    articles = []

    # Open the SGML file and parse it with BeautifulSoup
    with open(file_path, 'r', encoding='latin-1') as f:
        data = f.read()
        soup = BeautifulSoup(data, 'lxml')

        # Find all documents (<REUTERS> tags)
        documents = soup.find_all('reuters')

        # Loop over each document to extract text and title
        for doc in documents:
            # Find the title (headline) within <TITLE> tags
            title = doc.find('title')
            title_text = title.text if title else ''

            # Find the article text within <BODY> tags
            body = doc.find('body')
            body_text = body.text if body else ''

            # Store the extracted title and body as a tuple
            articles.append((title_text, body_text))

    return articles
