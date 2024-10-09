import pickle
from PositionalIndex import positional_index_file  # Import the positional index file path

# Load positionalIndex from the serialized file (pickle)
with open(positional_index_file, 'rb') as f:
    positionalIndex = pickle.load(f)  # Deserialize the positional index

# Assign the positional index to a simpler variable name for convenience
index = positionalIndex

# NEAR Operator: Returns documents where term1 and term2 are at most 'k' tokens apart
def near_operator(term1, term2, k):
    """
    Optimized function to find documents where 'term1' and 'term2' appear within 'k' positions of each other.
    Utilizes a two-pointer technique to efficiently search through the postings lists of both terms.
    """
    # Convert both terms to uppercase for case-insensitive matching
    term1 = term1.upper()
    term2 = term2.upper()
    
    # Check if both terms are in the positional index
    if term1 not in index or term2 not in index:
        print("Neither or one of the terms were found in the positional index")
        return []
    
    result_docs = []  # List to store document IDs where terms are found within k positions

    # Get positional information for both terms (list of (docID, [positions]))
    postings_term1 = index[term1]  
    postings_term2 = index[term2]  

    # Initialize pointers for both postings lists
    i, j = 0, 0

    # Use the two-pointer technique to iterate over both postings lists
    while i < len(postings_term1) and j < len(postings_term2):
        doc1_string, positions1 = postings_term1[i]
        doc2_string, positions2 = postings_term2[j]
        
        # Convert document IDs from string to integer for comparison
        doc1 = int(doc1_string)
        doc2 = int(doc2_string)

        # If both terms are in the same document, check their positions
        if doc1 == doc2:
            a, b = 0, 0  # Pointers for positions within the document
            found_match = False  # Flag to indicate if a match was found in this document

            # Compare positions of both terms within the document using a two-pointer technique
            while a < len(positions1) and b < len(positions2):
                if abs(positions1[a] - positions2[b]) <= k:  # Check if the terms are within k tokens
                    if doc1 not in result_docs:
                        result_docs.append(doc1)  # Add the document to the result list
                    found_match = True  # Mark that a match was found

                # Move the pointer that's behind to narrow the window
                if positions1[a] < positions2[b]:
                    a += 1
                else:
                    b += 1

            # Move both document pointers forward once the match has been evaluated
            if found_match:
                i += 1
                j += 1
            elif doc1 < doc2:
                i += 1
            else:
                j += 1

        # If document IDs don't match, move the pointer for the smaller document ID
        elif doc1 < doc2:
            i += 1
        elif doc1 > doc2:
            j += 1  

    return result_docs  # Return the list of document IDs where the terms are within k tokens

# Brute force implementation of the NEAR operator (less efficient)
def near_operator_brute_force(term1, term2, k):
    """
    Brute force implementation of the NEAR operator.
    Iterates through all documents in the postings lists and compares all position pairs.
    """
    term1 = term1.upper()
    term2 = term2.upper()
    
    if term1 not in index or term2 not in index:
        print("neither terms were found in the positional index")
        return []
    
    result_docs = []  # List to store document IDs where terms are found within k positions
    
    # Get positional information for both terms
    postings_term1 = index[term1]
    postings_term2 = index[term2]
    
    # Iterate over both posting lists, comparing positions within each document
    for doc1, positions1 in postings_term1:
        for doc2, positions2 in postings_term2:
            if doc1 == doc2:  # Only compare positions within the same document
                for pos1 in positions1:
                    for pos2 in positions2:
                        if abs(pos1 - pos2) <= k:  # Check if the terms are within k tokens
                            result_docs.append(doc1)
                            break
    
    return result_docs  # Return the list of document IDs

# Example NEAR Query: Use the near_operator function to find terms within k tokens of each other
print("near_operator function results:")
print("NEAR('REAGAN', 'WAR', 15): ", near_operator('REAGAN', 'WAR', 15))
#print("NEAR('BAKER', 'HI', 2): ", near_operator('BAKER', 'HI', 2))

# Example brute force NEAR Query (uncomment to test)
# print("\n near_operator_brute_force function results: ")
# print("NEAR('BAKER', 'SAYS', 5): ", near_operator_brute_force('BAKER', 'SAYS', 5))
# print("NEAR('BAKER', 'HI', 2): ", near_operator_brute_force('BAKER', 'HI', 2))