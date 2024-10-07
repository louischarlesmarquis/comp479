import nltk
import os
from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Ensure necessary NLTK resources are available
nltk.download('punkt')
nltk.download('stopwords')

# Initialize PorterStemmer and stopword list
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# PrimaryIndex and PositionalIndex
primary_index = defaultdict(list)  # For PrimaryIndex: {token: [docID1, docID2, ...]}
positional_index = defaultdict(list)  # For PositionalIndex: {token: [(docID1, [pos1, pos2, ...]), ...]}

def process_document(newid, title, body):
    # Process a single document token by token and update the PrimaryIndex and PositionalIndex
    current_doc_id = newid
    token_offset = 0  # Track the position of the token in the document

    # Tokenize the title and body (token stream simulation)
    tokens = word_tokenize(title) + word_tokenize(body)

    # Apply case-folding, remove non-alphabetic tokens and stopwords, and apply stemming
    for token in tokens:
        current_token = token.lower()
        if not current_token.isalpha() or current_token in stop_words:
            continue
        current_token = stemmer.stem(current_token)

        # Update the PrimaryIndex
        if current_token not in primary_index:
            primary_index[current_token].append(current_doc_id)
        elif primary_index[current_token][-1] != current_doc_id:
            primary_index[current_token].append(current_doc_id)

        # Update the PositionalIndex
        if current_token not in positional_index:
            positional_index[current_token].append((current_doc_id, [token_offset]))
        else:
            # Check if the current_doc_id is already in the positional index for this token
            found_doc = False
            for doc_info in positional_index[current_token]:
                if doc_info[0] == current_doc_id:
                    doc_info[1].append(token_offset)
                    found_doc = True
                    break
            if not found_doc:
                positional_index[current_token].append((current_doc_id, [token_offset]))

        # Increment the token offset for positional indexing
        token_offset += 1

#Function to extract articles from Reuters-21578 SGML files
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
            process_document(newid, title_text, body_text)

# Iterate through all SGML files in the Reuters-21578 dataset directory
def process_reuters_dataset(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith('.sgm'):
            file_path = os.path.join(directory, file_name)
            # Stream content from each SGML file and index it
            extract_and_index_from_sgm(file_path)

# Path to the Reuters-21578 dataset directory
reuters_dir = 'C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/'

# Process the Reuters-21578 dataset
process_reuters_dataset(reuters_dir)

# Display the first few entries of the PrimaryIndex and PositionalIndex
print("Primary Index (first 10 tokens):")
for token, postings in list(primary_index.items())[:10]:
    print(f"Token: {token}, Postings: {postings}")

print("\nPositional Index (first 10 tokens):")
for token, postings in list(positional_index.items())[:10]:
    print(f"Token: {token}, Postings: {postings}")