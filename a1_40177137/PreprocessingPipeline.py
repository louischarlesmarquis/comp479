import os
from bs4 import BeautifulSoup  # For parsing SGML files
import pickle  # Optional import to serialize data

def extract_and_index_from_sgm(file_path):
    """
    Extracts documents from an .sgm file and retrieves the title, body, and document ID (newid)
    for each document. This function is designed to parse and process individual Reuters documents.
    """
    with open(file_path, 'r', encoding='latin-1') as f:
        data = f.read()  # Read the content of the .sgm file
        soup = BeautifulSoup(data, 'lxml')  # Parse the SGML content using BeautifulSoup

        # Find all <REUTERS> documents in the file
        documents = soup.find_all('reuters')

        # Loop through each document to extract the title, body, and document ID (newid)
        for doc in documents:
            title = doc.find('title')  # Extract the title (if available)
            title_text = title.text if title else ''  # Handle missing titles

            body = doc.find('body')  # Extract the body (if available)
            body_text = body.text if body else ''  # Handle missing bodies

            newid = doc['newid']  # Get the document ID (newid)

            # Placeholder for future indexing logic (e.g., tokenize and store document information)
            # The title_text, body_text, and newid would be used here for indexing or further processing.

def process_reuters_dataset(directory):
    """
    Processes the entire Reuters-21578 dataset by iterating through all .sgm files in the specified directory.
    For each file, it extracts and processes documents using the extract_and_index_from_sgm function.
    """
    # Iterate through each file in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.sgm'):  # Only process files with .sgm extension
            file_path = os.path.join(directory, file_name)  # Construct the full file path
            # Extract and index the content of the SGML file
            extract_and_index_from_sgm(file_path)

# Path to the Reuters-21578 dataset directory
reuters_dir = 'C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/'

# Create an empty dictionary to store docID to file offset mappings
doc_id_mapping = {}

# This code was added to make concordance queries more efficient
# Function to build a document index for fast retrieval
def build_doc_id_index():
    for file_name in os.listdir(reuters_dir):
        if file_name.endswith('.sgm'):
            file_path = os.path.join(reuters_dir, file_name)

            with open(file_path, 'r', encoding='latin-1') as f:
                # Read the file in chunks and find <REUTERS> tags manually
                while True:
                    start_position = f.tell()  # Get the current byte position
                    data = f.read(10000)  # Read a chunk of the file

                    if not data:  # End of file
                        break
                    
                    # Parse the chunk using BeautifulSoup
                    soup = BeautifulSoup(data, 'lxml')

                    # Find all <REUTERS> documents
                    documents = soup.find_all('reuters')

                    for doc in documents:
                        doc_id = doc['newid']

                        # Map the document ID to the file name and the start byte offset
                        doc_id_mapping[doc_id] = (file_name, start_position)

                    # Move back a bit in case the chunk cuts off in the middle of a tag
                    f.seek(f.tell() - 100)

    # Save the mapping to a file (e.g., JSON or pickle)
    with open('doc_id_index.pkl', 'wb') as f:
        pickle.dump(doc_id_mapping, f)

# Build the index
build_doc_id_index()

