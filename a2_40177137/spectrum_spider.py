import scrapy
import re
import io
import json
from PyPDF2 import PdfReader
from collections import defaultdict
from nltk.tokenize import word_tokenize  # For tokenizing the document text
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import numpy as np

class SpectrumSpider(scrapy.Spider):
    name = "spectrum"
    allowed_domains = ["spectrum.library.concordia.ca"]
    custom_settings = {
        "ROBOTSTXT_OBEY": True,  # Ensures the spider respects the site's robots.txt file
        "DOWNLOAD_DELAY": 1,  # Avoid overloading the server
    }

    # Track the number of files downloaded
    files_downloaded = 0

    #Track pdf id
    newid = 0

    # Dictionary to hold the positional index: maps tokens to the list of documents and positions
    positionalIndex = defaultdict(list)  # {token: [(docID1, [pos1, pos2, ...]), ...]}

    # Accept a file limit as an argument when the spider is initialized
    def __init__(self, file_limit=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_limit = int(file_limit)  
        self.documents = defaultdict(list)  # Store documents as a collection of tokens

    def start_requests(self):
        # Generate URLs dynamically for years from 2025 to 1965
        base_url = "https://spectrum.library.concordia.ca/view/year/"
        for year in range(2025, 2022, -1):  # Decreasing from 2025 to 1965
            url = f"{base_url}{year}.html"
            yield scrapy.Request(url=url, callback=self.parse_year, meta={"year": year})

    def parse_year(self, response):
        """
        extracts all publication links from a given year
        """
        # Check if the file limit is reached
        if self.files_downloaded >= self.file_limit:
            self.crawler.engine.close_spider(self, "File limit reached")
            return

        # Process a single year's page and extract publication links
        print(f"Processing year {response.meta['year']}, status: {response.status}")
        thesis_links = response.css("a::attr(href)").getall()
        thesis_links = [link for link in thesis_links if "id/eprint" in link]  # Filter thesis links

        for link in thesis_links:
            # Sequentially process each thesis for the current year
            yield response.follow(
                link,
                callback=self.extract_pdf_from_thesis,
                meta=response.meta  # Pass down metadata (e.g., year)
            )
        
        # Once all theses for this year are processed, log completion
        print(f"Finished processing all theses for year {response.meta['year']}")

    def extract_pdf_from_thesis(self, response):
        """
        extracts all pdf links within a given thesis
        """
        if self.files_downloaded >= self.file_limit:
            self.crawler.engine.close_spider(self, "File limit reached")
            return

        self.files_downloaded += 1  # Increment the file counter
        self.log(f"PDF ({self.files_downloaded}/{self.file_limit})")

        # Extract PDF links from the thesis page
        pdf_links = response.css("a.ep_document_link::attr(href)").getall()
        pdf_links = [response.urljoin(link) for link in pdf_links if link.endswith(".pdf")]

        for pdf_link in pdf_links:
            yield scrapy.Request(
                url=pdf_link,
                callback=self.extract_text_from_pdf,
                meta=response.meta  # Pass down metadata (e.g., year)
            )
        
        # Log once the thesis has been fully processed
        print(f"Processed a thesis from year {response.meta['year']}")

    def extract_text_from_pdf(self, response):
        """
        extract all the text and tokenize the given pdf 
        """
        print(f"Processing a PDF from year {response.meta['year']}")
        
        # Wrap the bytes in a BytesIO object
        pdf_stream = io.BytesIO(response.body)
        pdf_reader = PdfReader(pdf_stream)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Preprocess the text to fix concatenated words and clean up formatting
        preprocessed_text = self.preprocess_text(text)

        # Tokenize the text
        tokens = word_tokenize(preprocessed_text)

        # Sanitize and filter tokens
        sanitized_tokens = [self.sanitize_token(token) for token in tokens]
        sanitized_tokens = [token for token in sanitized_tokens if token]  # Remove None values

        current_doc_id = self.newid  # Document ID for this specific document
        token_offset = 0  # Track the position of the token in the document

        # Add each token and its position to the positional index
        for token in sanitized_tokens:
            current_token =  token # Current token being processed

            # If the token isn't already in the index, add it with the current docID and token position
            if current_token not in self.positionalIndex:
                self.positionalIndex[current_token].append((current_doc_id, [token_offset]))
            else:
                # If the token exists, check if the document ID is already in the index for this token
                found_doc = False
                for doc_info in self.positionalIndex[current_token]:
                    # If the document ID exists for this token, append the new token position
                    if doc_info[0] == current_doc_id:
                        doc_info[1].append(token_offset)
                        found_doc = True
                        break
                # If the document ID doesn't exist for this token, add the new docID and position list
                if not found_doc:
                    self.positionalIndex[current_token].append((current_doc_id, [token_offset]))

            # Move to the next token in the document by incrementing the token offset
            token_offset += 1

        self.newid += 1

        print("PRIMARY INDEX: ", self.positionalIndex)
        self.save_positional_index()
        # Trigger clustering after all documents are processed
        if self.files_downloaded >= self.file_limit:
            self.cluster_documents()

    def preprocess_text(self, text):
        """
        Clean and preprocess extracted text to address common formatting issues.
        """
        # Replace newlines, tabs, and multiple spaces with a single space
        text = re.sub(r"[\n\r\t]+", " ", text)
        text = re.sub(r"\s{2,}", " ", text)

        # Add spaces between concatenated words (e.g., "word1word2" -> "word1 word2")
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)  # Handle camel case
        text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)  # Handle word-number combinations
        text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text)  # Handle number-word combinations

        return text

    def sanitize_token(self, token):
        """
        Sanitize a token to ensure it is a valid word for indexing.
        """
        token = token.lower()  # Convert to lowercase

        # Remove stop words
        if token in stopwords.words("english"):
            return None

        # Remove tokens that are too short or not alphabetic
        if len(token) < 3 or not re.match(r"^[a-z]+$", token):
            return None

        return token

    def save_positional_index(self):
        """
        Save the positional index to a JSON file.
        """
        with open("positional_index.json", "w", encoding="utf-8") as f:
            json.dump(self.positionalIndex, f, indent=4, default=list)
        print("Positional index saved successfully.")

    def cluster_documents(self):
        """
        Cluster the documents based on the tokens using KMeans.
        """
        print("Clustering documents...")

        # Prepare data for clustering
        doc_ids = list(self.documents.keys())
        document_texts = [" ".join(self.documents[doc_id]) for doc_id in doc_ids]

        # Create a document-term matrix
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(document_texts)

        # Perform KMeans clustering
        num_clusters = 3  # You can adjust this based on your requirements
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(X)

        # Print clustering results
        clusters = {i: [] for i in range(num_clusters)}
        for doc_id, label in zip(doc_ids, kmeans.labels_):
            clusters[label].append(doc_id)

        print("Clustering Results:")
        for cluster_id, docs in clusters.items():
            print(f"Cluster {cluster_id}: {docs}")

        # Save clustering results to a JSON file
        with open("clustering_results.json", "w", encoding="utf-8") as f:
            json.dump(clusters, f, indent=4)
        print("Clustering results saved to 'clustering_results.json'.")

#end of class