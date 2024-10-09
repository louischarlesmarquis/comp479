import nltk
import os
from collections import defaultdict
from bs4 import BeautifulSoup  # For parsing SGML files
from nltk.tokenize import word_tokenize  # For tokenizing text into individual words
from nltk.corpus import stopwords  # For stopword removal
from nltk.stem import PorterStemmer  # For stemming words

# Download necessary NLTK resources (uncomment if needed)
# nltk.download('punkt')
# nltk.download('stopwords')

# Initialize stopword list and stemming tool
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# List to store preprocessing statistics for each stage
statistics = []

# Function to extract tokens from SGML articles
def extract_articles_from_sgm(file_path):
    """
    Extracts tokens from the title and body of each article in a given SGML file.
    """
    tokens = []  # List to store tokens from the file
    with open(file_path, 'r', encoding='latin-1') as f:
        data = f.read()
        soup = BeautifulSoup(data, 'lxml')  # Parse SGML file

        # Extract each <REUTERS> document and tokenize the title and body
        documents = soup.find_all('reuters')
        for doc in documents:
            title = doc.find('title')
            title_text = title.text if title else ''  # Handle missing titles

            body = doc.find('body')
            body_text = body.text if body else ''  # Handle missing bodies

            # Tokenize the title and body, then add to the token list
            tokens.extend(word_tokenize(title_text) + word_tokenize(body_text))

    return tokens  # Return the list of tokens

# Function to process the Reuters dataset with various preprocessing filters
def process_reuters_dataset(directory, filters=None):
    """
    Processes all SGML files in the Reuters dataset directory and applies optional filters
    such as case folding, stopword removal, number removal, and stemming.
    """
    all_tokens = []  # List to store all tokens from the dataset
    for file_name in os.listdir(directory):
        if file_name.endswith('.sgm'):  # Only process .sgm files
            file_path = os.path.join(directory, file_name)
            tokens = extract_articles_from_sgm(file_path)  # Extract tokens from the file
            if filters:
                tokens = apply_filters(tokens, filters)  # Apply any specified filters
            all_tokens.extend(tokens)  # Add tokens from the current file to the main list
    return all_tokens  # Return all the tokens from the dataset

# Function to apply preprocessing filters to a token list
def apply_filters(tokens, filters):
    """
    Applies various filters to the token list such as number removal, case folding,
    stopword removal, and stemming.
    """
    # Remove numerical tokens if the 'no_numbers' filter is enabled
    if 'no_numbers' in filters:
        tokens = [token for token in tokens if not token.isdigit()]

    # Convert tokens to lowercase if 'case_folding' filter is enabled
    if 'case_folding' in filters:
        tokens = [token.lower() for token in tokens]

    # Remove stopwords and non-alphabetic tokens if 'stopwords_removal' filter is enabled
    if 'stopwords_removal' in filters:
        tokens = [token for token in tokens if token not in stop_words and token.isalpha()]

    # Apply stemming if the 'stemming' filter is enabled
    if 'stemming' in filters:
        tokens = [stemmer.stem(token) for token in tokens]

    return tokens  # Return the filtered token list

# Function to calculate basic statistics from the token list
def calculate_statistics(tokens):
    """
    Calculates statistics from a token list, such as distinct terms,
    total number of tokens, and non-positional postings (term frequencies).
    """
    distinct_terms = set(tokens)  # Find distinct tokens
    term_frequency = defaultdict(int)  # Dictionary to store term frequencies

    # Count the occurrences of each token
    for token in tokens:
        term_frequency[token] += 1

    # Return a dictionary with the calculated statistics
    return {
        'distinct_terms': len(distinct_terms),  # Number of distinct terms
        'non_positional_postings': sum(term_frequency.values()),  # Total term occurrences
        'tokens': len(tokens)  # Total number of tokens
    }

# Function to process multiple preprocessing stages and collect statistics
def collect_statistics(directory):
    """
    Processes the Reuters dataset through different preprocessing stages,
    collects statistics for each stage, and stores the results.
    """
    stages = [
        ('unfiltered', []),  # No filtering
        ('no_numbers', ['no_numbers']),  # Remove numerical tokens
        ('case_folding', ['no_numbers', 'case_folding']),  # Apply case folding after number removal
        ('stopwords_30', ['no_numbers', 'case_folding', 'stopwords_removal']),  # Remove stopwords
        ('stopwords_150', ['no_numbers', 'case_folding', 'stopwords_removal']),  # Another stopword test
        ('stemming', ['no_numbers', 'case_folding', 'stopwords_removal', 'stemming'])  # Apply stemming
    ]

    # Process each stage and calculate statistics
    for name, filters in stages:
        print(f"Processing stage: {name}")
        tokens = process_reuters_dataset(directory, filters)  # Get tokens with filters
        stats = calculate_statistics(tokens)  # Calculate statistics for this stage
        statistics.append((name, stats))  # Store the statistics
        print(f"Stats for {name}: {stats}")  # Output statistics for this stage

# Function to calculate percentage difference between current and previous values
def calculate_percentage_diff(current, previous):
    """
    Calculates the percentage difference between two values. 
    Returns 0 if the previous value is 0 to avoid division by zero.
    """
    return round(((current - previous) / previous) * 100, 2) if previous != 0 else 0

# Directory containing the Reuters-21578 dataset
reuters_dir = 'C:/Users/lcmar/OneDrive/Bureau/Concordia_University/fall_2024/comp479/reuters21578/'

# Collect statistics for all preprocessing stages
collect_statistics(reuters_dir)

# Output results in a tabular format, with delta and total columns for comparison
print("\nPreprocessing Results for Reuters-21578 with Delta and Total Columns")
print(f"{'Stage':<15}{'Distinct Terms':<15}{'Δ%':<10}{'T%':<10}{'Nonpositional Postings':<25}{'Δ%':<15}{'T%':<15}{'Tokens':<10}{'Δ%':<10}{'T%':<10}")

# Get the initial statistics for comparison
initial_stats = statistics[0][1]
previous_stats = initial_stats

# Loop through each stage and print the statistics, calculating delta and total percentage changes
for i, (stage, stats) in enumerate(statistics):
    # Delta (difference from the previous row)
    delta_terms = calculate_percentage_diff(stats['distinct_terms'], previous_stats['distinct_terms'])
    delta_postings = calculate_percentage_diff(stats['non_positional_postings'], previous_stats['non_positional_postings'])
    delta_tokens = calculate_percentage_diff(stats['tokens'], previous_stats['tokens'])

    # Total (difference from the first row)
    total_terms = calculate_percentage_diff(stats['distinct_terms'], initial_stats['distinct_terms'])
    total_postings = calculate_percentage_diff(stats['non_positional_postings'], initial_stats['non_positional_postings'])
    total_tokens = calculate_percentage_diff(stats['tokens'], initial_stats['tokens'])

    # Output row with statistics and percentage changes
    print(f"{stage:<15}{stats['distinct_terms']:<15}{delta_terms:<10}{total_terms:<10}{stats['non_positional_postings']:<25}{delta_postings:<15}{total_postings:<15}{stats['tokens']:<10}{delta_tokens:<10}{total_tokens:<10}")

    # Update previous stats for the next iteration
    previous_stats = stats
