import os
import pickle # module that stores positionalIndex as a serialized file
from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize

# PositionalIndex
positionalIndex = defaultdict(list)  # For PositionalIndex: {token: [(docID1, [pos1, pos2, ...]), ...]}

def create_positional_index(newid, title, body):
    # Process a single document token by token and update the PositionalIndex
    current_doc_id = newid
    token_offset = 0  # Track the position of the token in the document

    # Tokenize the title and body (token stream simulation)
    tokens = word_tokenize(title) + word_tokenize(body)

    for token in tokens:
        current_token = token

        # Update the PositionalIndex
        if current_token not in positionalIndex:
            positionalIndex[current_token].append((current_doc_id, [token_offset]))
        else:
            # Check if the current_doc_id is already in the positional index for this token
            found_doc = False
            for doc_info in positionalIndex[current_token]:
                if doc_info[0] == current_doc_id:
                    doc_info[1].append(token_offset)
                    found_doc = True
                    break
            if not found_doc:
                positionalIndex[current_token].append((current_doc_id, [token_offset]))

        # Increment the token offset for positional indexing
        token_offset += 1

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
            create_positional_index(newid, title_text, body_text)

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

# Custom print function to format like Figure 2.11
def print_positional_index(positional_index):
    print("\nPositional Index: ")
    # Loop through each token in the positional index
    for token, postings in positional_index.items():
        # Calculate the total frequency of the token across all documents
        total_frequency = sum(len(positions) for _, positions in postings)
        
        # Print the token and its total frequency across all documents
        print(f"{token}, {total_frequency}")
        
        # For each document that contains the token, print the docID, frequency, and positions
        for docID, positions in postings:
            doc_frequency = len(positions)  # Frequency of token in the specific document
            positions_str = ", ".join(map(str, positions))  # Format positions as a string
            print(f"    {docID}, {doc_frequency}: <{positions_str}>;")


# Get the current working directory
current_directory = os.getcwd()+"/a1_40177137"

# Construct the full paths for the pickle file
positional_index_file = os.path.join(current_directory, 'positionalIndex.pkl')

# Save primaryIndex to a file, so that it doesn't need to be rebuilt everytime I want to access it later on
with open(positional_index_file, 'wb') as f:
    pickle.dump(positionalIndex, f)


#print_positional_index(positionalIndex)

# print("\nPositional Index (first token):")
# for token, postings in list(positionalIndex.items())[:1]:
#     print(f"Token: {token}, Postings: {postings}")
