import os
import pickle # module that stores primaryIndex as a serialized file
from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize

# PrimaryIndex
primaryIndex = defaultdict(list)  # For PrimaryIndex: {token: [docID1, docID2, ...]}

def create_primary_index(newid, title, body):
    # Process a single document token by token and update the PrimaryIndex
    current_doc_id = newid

    # Tokenize the title and body (token stream simulation)
    tokens = word_tokenize(title) + word_tokenize(body)

    for token in tokens:
        current_token = token

        # Update the PrimaryIndex
        if current_token not in primaryIndex:
            primaryIndex[current_token].append(current_doc_id)
        elif primaryIndex[current_token][-1] != current_doc_id:
            primaryIndex[current_token].append(current_doc_id)

def extract_and_index_from_sgm(file_path):
    with open(file_path, 'r', encoding='latin-1') as f:
        data = f.read()
        soup = BeautifulSoup(data, 'lxml')

        # Find all documents in the SGML file
        documents = soup.find_all('reuters')

        # Loop over each document to extract the title, body, and document ID (newid)
        for doc in documents:
            title = doc.find('title')
            title_text = title.text if title else ''

            body = doc.find('body')
            body_text = body.text if body else ''

            newid = doc['newid']

            # Stream and process each document token by token
            create_primary_index(newid, title_text, body_text)

def process_reuters_dataset(directory):
    # Iterate through all SGML files in the Reuters-21578 dataset directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.sgm'):
            file_path = os.path.join(directory, file_name)
            # Stream content from each SGML file and index it
            extract_and_index_from_sgm(file_path)

# Path to the Reuters-21578 dataset directory
reuters_dir = 'C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/'

# Process the Reuters-21578 dataset
process_reuters_dataset(reuters_dir)


# Get the current working directory
current_directory = os.getcwd()+"/a1_40177137"

# Construct the full paths for the pickle file
primary_index_file = os.path.join(current_directory, 'primaryIndex.pkl')

# Save primaryIndex to a file, so that it doesn't need to be rebuilt everytime I want to access it later on
with open(primary_index_file, 'wb') as f:
    pickle.dump(primaryIndex, f)

# Display the first entry of the PrimaryIndex
# print("Primary Index (first 2 tokens):")
# for token, postings in list(primaryIndex.items())[:2]:
#     print(f"Token: {token}, Postings: {postings}")