import os
from bs4 import BeautifulSoup

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

def process_reuters_dataset(directory):
    # Iterate through all SGML files in the Reuters-21578 dataset directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.sgm'):
            file_path = os.path.join(directory, file_name)
            # Stream content from each SGML file and index it
            extract_and_index_from_sgm(file_path)