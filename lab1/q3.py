# Documents: The individual news items in the corpus.
# Words: The total number of words across all documents.
# Sentences: The number of sentences in the entire corpus.

from nltk.corpus import reuters
from nltk.tokenize import sent_tokenize

# Number of documents
num_docs = len(reuters.fileids())

# Count words and sentences
word_count = 0
sentence_count = 0

for file_id in reuters.fileids():
    words = reuters.words(file_id)
    word_count += len(words)
    
    sentences = sent_tokenize(reuters.raw(file_id))
    sentence_count += len(sentences)

print(f"Number of documents: {num_docs}")       #10,788
print(f"Number of words: {word_count}")         #1,720,901
print(f"Number of sentences: {sentence_count}") #53,792
