import os
from bs4 import BeautifulSoup  # For parsing SGML files

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



