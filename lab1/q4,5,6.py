#QUESTION 5
from nltk.corpus import reuters

prepositions = ['of', 'in', 'to', 'for', 'with', 'on', 'at', 'by', 'from', 'about', 'as', 'into', 'like', 'through', 'after', 'over', 'between', 'out', 'against', 'during', 'without', 'before', 'under', 'around', 'among']

doc_words = reuters.words('training/9920')

word_count = len(doc_words)
preposition_count = sum(1 for word in doc_words if word.lower() in prepositions)

print(f"Number of words: {word_count}")
print(f"Number of prepositions: {preposition_count}")


#QUESTION 5
categories = reuters.categories()
file_ids_by_category = {category: reuters.fileids(category) for category in categories}
# Print categories and their file IDs
for category, file_ids in file_ids_by_category.items():
    print(f"{category}: {len(file_ids)} files")


#QUESTION 6
def word_freq(word, file_id):
    words = reuters.words(file_id)
    return words.count(word)
# Example usage
print(word_freq('market', 'training/9920'))
