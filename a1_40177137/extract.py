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

# Function to tokenize the extracted article and headline text
def tokenize_articles(articles):
    token_stream = []

    for title, body in articles:
        # Tokenize title and body using NLTK's word_tokenize
        title_tokens = word_tokenize(title)
        body_tokens = word_tokenize(body)

        # Combine tokens from title and body
        all_tokens = title_tokens + body_tokens

        # Append to token stream
        token_stream.extend(all_tokens)

    return token_stream

# Example: Process all files in the Reuters-21578 dataset
def process_reuters_dataset(directory):
    all_tokens = []

    # Iterate through all the SGML files in the dataset
    for file_name in os.listdir(directory):
        if file_name.endswith('.sgm'):
            file_path = os.path.join(directory, file_name)

            # Extract articles from the file
            articles = extract_articles_from_sgm(file_path)

            # Tokenize the extracted articles
            tokens = tokenize_articles(articles)

            # Append the tokens to the complete token stream
            all_tokens.extend(tokens)

    return all_tokens

# Path to the Reuters-21578 dataset directory
reuters_dir = 'C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/'

# Process the dataset and extract the token stream
token_stream = process_reuters_dataset(reuters_dir)

# Display the first few tokens
print(token_stream[:100])
