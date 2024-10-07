#QUESTION 1
from bs4 import BeautifulSoup

# Open and read the .sgm file
with open('C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/reut2-020.sgm', 'r', encoding='ISO-8859-1') as f:
    data = f.read()

# Parse the file using BeautifulSoup
soup = BeautifulSoup(data, 'html.parser')

# Find all <REUTERS> tags (each article is inside a <REUTERS> tag)
articles = soup.find_all('reuters')

# Count the number of articles
print(f"Number of articles in reut2-020.sgm: {len(articles)}") #1000 articles


