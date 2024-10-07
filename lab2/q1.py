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
