#QUESTION 1
from bs4 import BeautifulSoup

path_to_reuter_files = 'C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/'

# Load and parse the .sgm file
def count_documents_in_sgm(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return len(soup.find_all('reuters'))
# Count the documents in reut2-020.sgm 
file_name = "reut2-020.sgm"
full_path = f"{path_to_reuter_files}{file_name}"
count_020 = count_documents_in_sgm(full_path)
#Count the documents in reut2-021.sgm 
file_name = "reut2-021.sgm"
full_path = f"{path_to_reuter_files}{file_name}"
count_021 = count_documents_in_sgm(full_path)
print(f"Number of documents in reut2-020.sgm: {count_020}") #1000
print(f"Number of documents in reut2-021.sgm: {count_021}") #578


#QUESTION 2
def extract_articles(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        soup = BeautifulSoup(file, 'html.parser')
    articles = {}
    for reuter in soup.find_all('reuters'):
        newid = reuter['newid']
        text = reuter.find('text').get_text()
        articles[newid] = text
    return articles
articles = extract_articles(full_path)
for newid, article_text in articles.items():
    print(f"NEWID: {newid}\nArticle Text: {article_text[:200]}...\n")


#ADVANCED -> QUESTION 1
# Load organization names
file_name = "all-orgs-strings.lc.txt"
full_path = f"{path_to_reuter_files}{file_name}"
with open(full_path, 'r') as file:
    orgs = [line.strip() for line in file]
    #It's a concise way to create a list by iterating over each line in the file.
    #line.strip() removes any leading and trailing whitespace (including newline characters) from each line of text
# Count occurrences of each org in the articles
org_counts = {org: 0 for org in orgs} 
for article in articles.values():
    for org in orgs:
        if org in article:
            org_counts[org] += 1
# Print results
for org, count in org_counts.items():
    print(f"{org}: {count}")


#ADVANCED -> QUESTION 3-4
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary resources
nltk.download('punkt')
nltk.download('stopwords')

# Clean article text
def clean_text(article):
    tokens = word_tokenize(article)
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return tokens

# Clean all articles
cleaned_articles = {newid: clean_text(text) for newid, text in articles.items()}

from nltk.tokenize import word_tokenize

tokenized_articles = {newid: word_tokenize(text) for newid, text in articles.items()}
for newid, tokens in tokenized_articles.items():
    print(f"NEWID: {newid}\nTokens: {tokens[:20]}...\n")
