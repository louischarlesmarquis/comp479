import pickle
import os
from bs4 import BeautifulSoup
from PositionalIndex import positional_index_file
from nltk.tokenize import word_tokenize  # For tokenizing the document text

# Load primaryIndex from the file
with open(positional_index_file, 'rb') as f:
    positionalIndex = pickle.load(f)

# Path to the Reuters-21578 dataset directory
reuters_dir = 'C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/'

# function to retrieve a document by its id and tokenize it if it matches the specified id
def tokenize_doc_id(file_path, doc_id):
    with open(file_path, 'r', encoding='latin-1') as f:
        data = f.read()  # Read the content of the .sgm file
        soup = BeautifulSoup(data, 'lxml')  # Parse the SGML content using BeautifulSoup

        # Find all <REUTERS> documents in the file
        documents = soup.find_all('reuters')

        # Loop through each document to extract the title, body, and document ID (newid)
        for doc in documents:
            newid = doc['newid']  # Get the document ID (newid)
            # Tokenize and return the tokens if it matches the specified doc_id
            if doc_id == newid:
                title = doc.find('title')  # Extract the title (if available)
                title_text = title.text if title else ''  # Handle missing titles

                body = doc.find('body')  # Extract the body (if available)
                body_text = body.text if body else ''  # Handle missing bodies

                tokens = word_tokenize(title_text) + word_tokenize(body_text)
                return tokens
    return None  # Return None if the document is not found in the file

def process_reuters_dataset(directory, doc_id):
    """
    Processes the entire Reuters-21578 dataset by iterating through all .sgm files in the specified directory.
    For each file, it extracts and processes documents using the extract_and_index_from_sgm function.
    """
    # Iterate through each file in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.sgm'):  # Only process files with .sgm extension
            file_path = os.path.join(directory, file_name)  # Construct the full file path
            # Tokenize and return the document if found
            tokens = tokenize_doc_id(file_path, doc_id)
            if tokens is not None:
                return tokens
    return None  # Return None if the document is not found

# Concordance Function: Displays 2k+1 tokens around each occurrence of the query term
def concordance(query, k):
    query = query.upper()

    if query not in positionalIndex:
        print("The term was not found in the positional index")
        return []

    result = []
    
    # Find term in positionalIndex
    for doc_id, positions in positionalIndex[query]:
        article_tokens = process_reuters_dataset(reuters_dir, doc_id)
        
        if article_tokens is None:
            print(f"Document ID {doc_id} not found or could not be tokenized.")
            continue  # Skip to the next document if tokens are None
        
        for pos in positions:
            start = max(0, pos - k)
            end = min(len(article_tokens), pos + k + 1)
            context = article_tokens[start:end]
            context_string = f"{doc_id}: {' '.join(context)}"
            result.append(context_string)

    return result

# Example Concordance Query
concordance_results = concordance('CLIMATE', 10)

for line in concordance_results:
    print(line)
