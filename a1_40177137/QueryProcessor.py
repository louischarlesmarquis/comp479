import pickle
from PrimaryIndex import primary_index_file

# Load primaryIndex from the file
with open(primary_index_file, 'rb') as f:
    primaryIndex = pickle.load(f)

def boolean_retrieval(primary_index, query, query_type):
    documents = []
    
    # Single Term Query
    if query_type == "single":
        query = query.upper()
        print(f"Find {query}")
        if query in primary_index:
            documents.extend(primary_index[query])
        else:
            print(f"{query} not found")

    # Or query
    elif query_type == "or":
        terms = [term.upper() for term in query.split()]
        print(f"Find {terms[0]} or {terms[1]}")
        
        for term in terms:
            if term in primary_index:
                # Append document IDs for each term (if it exists)
                documents.extend(primary_index[term])
            else:
                print(f"{term} not found")

    # And query
    elif query_type == "and":
        terms = [term.upper() for term in query.split()]
        print(f"Find {terms[0]} and {terms[1]}")
        
        if terms[0] in primary_index and terms[1] in primary_index:
            # Perform set intersection to get common document IDs
            doc_ids_term_1 = set(primary_index[terms[0]])
            doc_ids_term_2 = set(primary_index[terms[1]])
            common_doc_ids = doc_ids_term_1.intersection(doc_ids_term_2)
            
            if common_doc_ids:
                documents.extend(list(common_doc_ids))
            else:
                print(f"No documents contain both {terms[0]} and {terms[1]}")
        else:
            if terms[0] not in primary_index:
                print(f"{terms[0]} not found")
            if terms[1] not in primary_index:
                print(f"{terms[1]} not found")
    
    return documents

print(boolean_retrieval(primaryIndex, "BAHIA", "single"))
print(boolean_retrieval(primaryIndex, "BAHIA FORM", "or"))
print(boolean_retrieval(primaryIndex, "PIE VIDEO", "and"))