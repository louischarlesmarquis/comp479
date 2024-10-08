import nltk
import os
from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download necessary NLTK resources
# nltk.download('punkt')
# nltk.download('stopwords')

# Initialize variables
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Dictionary to hold statistics
statistics = []

# Function to extract tokens from articles
def extract_articles_from_sgm(file_path):
    tokens = []
    with open(file_path, 'r', encoding='latin-1') as f:
        data = f.read()
        soup = BeautifulSoup(data, 'lxml')
        documents = soup.find_all('reuters')
        for doc in documents:
            title = doc.find('title')
            title_text = title.text if title else ''
            body = doc.find('body')
            body_text = body.text if body else ''
            tokens.extend(word_tokenize(title_text) + word_tokenize(body_text))
    return tokens

# Function to process Reuters dataset with different preprocessing steps
def process_reuters_dataset(directory, filters=None):
    all_tokens = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.sgm'):
            file_path = os.path.join(directory, file_name)
            tokens = extract_articles_from_sgm(file_path)
            if filters:
                tokens = apply_filters(tokens, filters)
            all_tokens.extend(tokens)
    return all_tokens

# Function to apply filters based on options
def apply_filters(tokens, filters):
    # Remove numbers
    if 'no_numbers' in filters:
        tokens = [token for token in tokens if not token.isdigit()]

    # Case folding
    if 'case_folding' in filters:
        tokens = [token.lower() for token in tokens]

    # Remove stopwords
    if 'stopwords_removal' in filters:
        tokens = [token for token in tokens if token not in stop_words and token.isalpha()]

    # Apply stemming
    if 'stemming' in filters:
        tokens = [stemmer.stem(token) for token in tokens]

    return tokens

# Function to calculate statistics
def calculate_statistics(tokens):
    distinct_terms = set(tokens)
    term_frequency = defaultdict(int)
    for token in tokens:
        term_frequency[token] += 1

    return {
        'distinct_terms': len(distinct_terms),
        'non_positional_postings': sum(term_frequency.values()),
        'tokens': len(tokens)
    }

# Process each stage and store the results
def collect_statistics(directory):
    stages = [
        ('unfiltered', []),
        ('no_numbers', ['no_numbers']),
        ('case_folding', ['no_numbers', 'case_folding']),
        ('stopwords_30', ['no_numbers', 'case_folding', 'stopwords_removal']),
        ('stopwords_150', ['no_numbers', 'case_folding', 'stopwords_removal']),
        ('stemming', ['no_numbers', 'case_folding', 'stopwords_removal', 'stemming'])
    ]

    for name, filters in stages:
        print(f"Processing stage: {name}")
        tokens = process_reuters_dataset(directory, filters)
        stats = calculate_statistics(tokens)
        statistics.append((name, stats))
        print(f"Stats for {name}: {stats}")

# Calculate percentage difference
def calculate_percentage_diff(current, previous):
    return round(((current - previous) / previous) * 100, 2) if previous != 0 else 0

# Directory containing the Reuters-21578 dataset
reuters_dir = 'C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/'

# Collect statistics for all preprocessing stages
collect_statistics(reuters_dir)

# Output results in a tabular format (similar to Table 5.1) with delta and total columns
print("\nPreprocessing Results for Reuters-21578 with Delta and Total Columns")
print(f"{'Stage':<15}{'Distinct Terms':<15}{'Δ%':<10}{'T%':<10}{'Nonpositional Postings':<25}{'Δ%':<15}{'T%':<15}{'Tokens':<10}{'Δ%':<10}{'T%':<10}")

initial_stats = statistics[0][1]
previous_stats = initial_stats

for i, (stage, stats) in enumerate(statistics):
    # Delta (difference from the previous row)
    delta_terms = calculate_percentage_diff(stats['distinct_terms'], previous_stats['distinct_terms'])
    delta_postings = calculate_percentage_diff(stats['non_positional_postings'], previous_stats['non_positional_postings'])
    delta_tokens = calculate_percentage_diff(stats['tokens'], previous_stats['tokens'])

    # Total (difference from the first row)
    total_terms = calculate_percentage_diff(stats['distinct_terms'], initial_stats['distinct_terms'])
    total_postings = calculate_percentage_diff(stats['non_positional_postings'], initial_stats['non_positional_postings'])
    total_tokens = calculate_percentage_diff(stats['tokens'], initial_stats['tokens'])

    # Output row
    print(f"{stage:<15}{stats['distinct_terms']:<15}{delta_terms:<10}{total_terms:<10}{stats['non_positional_postings']:<25}{delta_postings:<15}{total_postings:<15}{stats['tokens']:<10}{delta_tokens:<10}{total_tokens:<10}")

    # Update previous stats for next delta calculation
    previous_stats = stats
