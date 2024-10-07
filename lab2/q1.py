#QUESTION 1
from bs4 import BeautifulSoup

# Load and parse the .sgm file
def count_documents_in_sgm(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return len(soup.find_all('reuters'))

# Count the documents in reut2-020.sgm and reut2-021.sgm
count_020 = count_documents_in_sgm('C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/reut2-020.sgm')
count_021 = count_documents_in_sgm('C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/reut2-021.sgm')

print(f"Number of documents in reut2-020.sgm: {count_020}")
print(f"Number of documents in reut2-021.sgm: {count_021}")
