import pickle
from PrimaryIndex import primary_index_file  # Import the file path for the primaryIndex

# Load primaryIndex from the serialized file (pickle)
with open(primary_index_file, 'rb') as f:
    primaryIndex = pickle.load(f)  # Deserialize the primaryIndex for use in retrieval

def boolean_retrieval(primary_index, query, query_type):
    """
    Function to handle Boolean retrieval queries (single term, OR, and AND queries).
    Returns a list of document IDs that match the query.
    """
    documents = []  # List to store document IDs that match the query
    
    # Single Term Query: retrieves documents containing the query term
    if query_type == "single":
        query = query.upper()  # Convert query to uppercase to ensure case-insensitive matching
        print(f"Find {query}")
        if query in primary_index:
            documents.extend(primary_index[query])  # Add all document IDs where the term is found
        else:
            print(f"{query} not found")  # Output message if the term is not in the index

    # OR Query: retrieves documents containing any of the terms in the query
    elif query_type == "or":
        terms = [term.upper() for term in query.split()]  # Split the query into terms and normalize to uppercase
        print(f"Find {terms[0]} or {terms[1]}")
        
        for term in terms:
            if term in primary_index:
                # Add document IDs for each term that exists in the index
                documents.extend(primary_index[term])
            else:
                print(f"{term} not found")  # Output message if a term is not in the index

    # AND Query: retrieves documents containing both terms in the query
    elif query_type == "and":
        terms = [term.upper() for term in query.split()]  # Split the query into terms and normalize to uppercase
        print(f"Find {terms[0]} and {terms[1]}")
        
        # Check if both terms exist in the index
        if terms[0] in primary_index and terms[1] in primary_index:
            # Perform set intersection to find common document IDs between the two terms
            doc_ids_term_1 = set(primary_index[terms[0]])  # Get document IDs for the first term
            doc_ids_term_2 = set(primary_index[terms[1]])  # Get document IDs for the second term
            common_doc_ids = doc_ids_term_1.intersection(doc_ids_term_2)  # Find common documents
            
            if common_doc_ids:
                documents.extend(list(common_doc_ids))  # Add the common document IDs to the results
            else:
                print(f"No documents contain both {terms[0]} and {terms[1]}")  # Output if no common docs found
        else:
            # Output messages for each term that isn't found in the index
            if terms[0] not in primary_index:
                print(f"{terms[0]} not found")
            if terms[1] not in primary_index:
                print(f"{terms[1]} not found")
    
    return documents  # Return the list of matching document IDs

# Example queries to test the retrieval function
print(boolean_retrieval(primaryIndex, "BUSH", "single"))  # Single term query
print(boolean_retrieval(primaryIndex, "REAGAN BUSH", "or"))  # OR query with two terms
print(boolean_retrieval(primaryIndex, "GLEN KUWAIT", "and"))  # AND query with two terms