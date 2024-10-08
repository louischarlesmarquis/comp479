from PositionalIndex import *

index = positionalIndex

# NEAR Operator: Returns documents where term1 and term2 are at most 'k' tokens apart
def near_operator(term1, term2, k):
    term1 = term1.upper()
    term2 = term2.upper()
    
    if term1 not in index or term2 not in index:
        print("Neither or one of the terms were found in the positional index")
        return []
    
    result_docs = []

    # Get positional information for both terms
    postings_term1 = index[term1]  # List of (docID, [positions])
    postings_term2 = index[term2]  # List of (docID, [positions])

    # Initialize pointers for both postings lists
    i, j = 0, 0

    # Use two-pointer technique to iterate over both postings lists
    while i < len(postings_term1) and j < len(postings_term2):
        doc1_string, positions1 = postings_term1[i]
        doc2_string, positions2 = postings_term2[j]
        doc1 = int(doc1_string)
        doc2 = int(doc2_string)

        if doc1 == doc2:
            # Use two-pointer technique to iterate over both frequency lists
            a, b = 0, 0  # Reset a and b for each new document comparison
            found_match = False

            while a < len(positions1) and b < len(positions2):
                if abs(positions1[a] - positions2[b]) <= k:
                    if doc1 not in result_docs:
                        result_docs.append(doc1)
                    found_match = True  # Mark that we found a match

                # Move the pointer that's behind to narrow the window
                if positions1[a] < positions2[b]:
                    a += 1
                else:
                    b += 1

            # Move both document pointers forward once match has been evaluated
            if found_match:
                i += 1
                j += 1
            elif doc1 < doc2:
                i += 1  # Move i to the next document
            else:
                j += 1  # Move j to the next document
        elif doc1 < doc2:
            i += 1  # Move i to the next document
        elif doc1 > doc2:
            j += 1  # Move j to the next document

    return result_docs

#brute force implementation of the near operator, still works, but less efficient
def near_operator_brute_force(term1, term2, k):
    term1 = term1.upper()
    term2 = term2.upper()
    
    if term1 not in index or term2 not in index:
        print("neither terms were found in the positional index")
        return []
    
    result_docs = []
    
    # Get positional information for both terms
    postings_term1 = index[term1]
    postings_term2 = index[term2]
    
    #Iterate over both posting lists
    for doc1, positions1 in postings_term1:
        for doc2, positions2 in postings_term2:
            if doc1 == doc2:  # Only compare positions within the same document
                for pos1 in positions1:
                    for pos2 in positions2:
                        if abs(pos1 - pos2) <= k:
                            result_docs.append(doc1)
                            break
    
    return result_docs


# Example NEAR Query
print("near_operator function results:")
print("NEAR('BAKER', 'SAYS', 5): ", near_operator('BAKER', 'SAYS', 5, ))
print("NEAR('BAKER', 'HI', 2): ", near_operator('BAKER', 'HI', 2))

# print("\n near_operator_brute_force function results: ")
# print("NEAR('BAKER', 'SAYS', 5): ", near_operator_brute_force('BAKER', 'SAYS', 5))
# print("NEAR('BAKER', 'HI', 2): ", near_operator_brute_force('BAKER', 'HI', 2))