import os
import pickle  # For saving and loading the positionalIndex
from collections import defaultdict
from bs4 import BeautifulSoup  # For parsing SGML files
from nltk.tokenize import word_tokenize  # For tokenizing the document text

# Dictionary to hold the positional index: maps tokens to the list of documents and positions
positionalIndex = defaultdict(list)  # {token: [(docID1, [pos1, pos2, ...]), ...]}

def create_positional_index(newid, title, body):
    """
    Processes a single document by tokenizing its title and body,
    and updates the positional index by mapping each token to its positions in the document.
    """
    current_doc_id = newid  # Document ID for this specific document
    token_offset = 0  # Track the position of the token in the document

    # Tokenize the title and body text
    tokens = word_tokenize(title) + word_tokenize(body)

    # Add each token and its position to the positional index
    for token in tokens:
        current_token = token  # Current token being processed

        # If the token isn't already in the index, add it with the current docID and token position
        if current_token not in positionalIndex:
            positionalIndex[current_token].append((current_doc_id, [token_offset]))
        else:
            # If the token exists, check if the document ID is already in the index for this token
            found_doc = False
            for doc_info in positionalIndex[current_token]:
                # If the document ID exists for this token, append the new token position
                if doc_info[0] == current_doc_id:
                    doc_info[1].append(token_offset)
                    found_doc = True
                    break
            # If the document ID doesn't exist for this token, add the new docID and position list
            if not found_doc:
                positionalIndex[current_token].append((current_doc_id, [token_offset]))

        # Move to the next token in the document by incrementing the token offset
        token_offset += 1

def extract_and_index_from_sgm(file_path):
    """
    Extracts all documents from an .sgm file, retrieves their titles and bodies,
    and passes them for tokenization and positional indexing using create_positional_index().
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
            create_positional_index(newid, title_text, body_text)

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

def print_positional_index(positional_index):
    """
    Prints the positional index in a custom format. For each token, print its total frequency across
    all documents, and for each document, print the docID, frequency, and positions.
    """
    print("\nPositional Index: ")
    
    # Loop through each token in the positional index
    for token, postings in positional_index.items():
        # Calculate the total frequency of the token across all documents
        total_frequency = sum(len(positions) for _, positions in postings)
        
        # Print the token and its total frequency across all documents
        print(f"{token}, {total_frequency}")
        
        # For each document containing the token, print docID, frequency, and positions
        for docID, positions in postings:
            doc_frequency = len(positions)  # Frequency of the token in the specific document
            positions_str = ", ".join(map(str, positions))  # Format positions as a string
            print(f"    {docID}, {doc_frequency}: <{positions_str}>;")

# Get the current working directory to save the index
current_directory = os.getcwd() + "/a1_40177137"

# Define the file path to save the positionalIndex as a pickle file
positional_index_file = os.path.join(current_directory, 'positionalIndex.pkl')

# Save the positionalIndex to a file so it can be reused later without rebuilding
with open(positional_index_file, 'wb') as f:
    pickle.dump(positionalIndex, f)

# Uncomment to print the positional index in the custom format
# print_positional_index(positionalIndex)

# Optional: Uncomment to display the first token and its associated document positions from the positional index
# print("\nPositional Index (first token):")
# for token, postings in list(positionalIndex.items())[:1]:
#     print(f"Token: {token}, Postings: {postings}")
