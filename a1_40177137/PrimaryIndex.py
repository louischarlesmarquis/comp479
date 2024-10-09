import os
import pickle  # Used to serialize and save the primaryIndex to a file
from collections import defaultdict
from bs4 import BeautifulSoup  # For parsing the SGML files
from nltk.tokenize import word_tokenize  # For tokenizing the document text

# Dictionary to hold the inverted index: maps tokens to the list of documents containing them
primaryIndex = defaultdict(list)  # {token: [docID1, docID2, ...]}

def create_primary_index(newid, title, body):
    """
    Processes a single document by tokenizing its title and body,
    and updates the primary index by mapping each token to the document's ID (newid).
    """
    current_doc_id = newid  # Document ID for this specific document

    # Tokenize the title and body text
    tokens = word_tokenize(title) + word_tokenize(body)

    # Add each token to the primary index, mapping it to the current document ID
    for token in tokens:
        current_token = token  # Current token being processed

        # If the token isn't already in the index, add it with the current docID
        if current_token not in primaryIndex:
            primaryIndex[current_token].append(current_doc_id)
        # If the token exists, check that this document ID isn't already in the list to avoid duplicates
        elif primaryIndex[current_token][-1] != current_doc_id:
            primaryIndex[current_token].append(current_doc_id)

def extract_and_index_from_sgm(file_path):
    """
    Extracts all documents from an .sgm file, retrieves their titles and bodies,
    and indexes their tokens using create_primary_index().
    """
    with open(file_path, 'r', encoding='latin-1') as f:
        data = f.read()  # Read the content of the .sgm file
        soup = BeautifulSoup(data, 'lxml')  # Parse the SGML content using BeautifulSoup

        # Find all <REUTERS> documents in the file
        documents = soup.find_all('reuters')

        # Loop through each document to extract the text and index it
        for doc in documents:
            title = doc.find('title')  # Extract the title (if available)
            title_text = title.text if title else ''  # Handle missing titles

            body = doc.find('body')  # Extract the body (if available)
            body_text = body.text if body else ''  # Handle missing bodies

            newid = doc['newid']  # Get the document ID

            # Process and index the document's content
            create_primary_index(newid, title_text, body_text)

def process_reuters_dataset(directory):
    """
    Processes all SGML files in the dataset directory, extracting and indexing documents
    from each file by calling extract_and_index_from_sgm().
    """
    for file_name in os.listdir(directory):  # Iterate through each file in the directory
        if file_name.endswith('.sgm'):  # Only process .sgm files
            file_path = os.path.join(directory, file_name)  # Construct the full file path
            extract_and_index_from_sgm(file_path)  # Extract and index the file's contents

# Path to the Reuters-21578 dataset directory
reuters_dir = 'C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/'

# Process and index the Reuters dataset by scanning the entire dataset directory
process_reuters_dataset(reuters_dir)

# Get the current working directory for saving the index
current_directory = os.getcwd() + "/a1_40177137"

# Define the file path to save the primaryIndex as a pickle file
primary_index_file = os.path.join(current_directory, 'primaryIndex.pkl')

# Save the primaryIndex to a file so it can be reused later without rebuilding
with open(primary_index_file, 'wb') as f:
    pickle.dump(primaryIndex, f)

# Optional: Uncomment to display the first 2 tokens and their associated document lists
# print("Primary Index (first 2 tokens):")
# for token, postings in list(primaryIndex.items())[:2]:
#     print(f"Token: {token}, Postings: {postings}")
