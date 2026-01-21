

# pubmed_scraper.py
"""
PubMed API Scraper for PostopCare

Setup:
    pip install requests
    Get free API key: https://www.ncbi.nlm.nih.gov/account/

PubMed API returns XML by default. Key endpoints:
    - esearch: Search and get PMIDs
    - efetch: Get full article details by PMID
"""
# make sure to install python-dotenv and requests to ensure dependencies work properly
import requests
import json
import xml.etree.ElementTree as ET
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
API_KEY = os.getenv("PUBMED_API_KEY")


def search_pubmed(query: str, max_results: int = 10) -> list[str]:
    """
    Search PubMed and return list of PMIDs.
    
    Uses the esearch endpoint: {BASE_URL}/esearch.fcgi
    
    Input:
        query = "knee replacement post operative care"
        max_results = 10
    
    Output:
        ["39847123", "39845678", "39842345", ...]  # List of PMIDs
    
    Example API URL:
        https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=knee+replacement&retmax=10&retmode=json&api_key=YOUR_KEY
    
    Example Response (JSON mode):
        {
            "esearchresult": {
                "count": "12345",
                "retmax": "10",
                "idlist": ["39847123", "39845678", ...]
            }
        }
    """
    #request parameters
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': max_results,
        'retmode': 'json'
    }
    
    #adding the api key
    if API_KEY:
        params['api_key'] = API_KEY
    
    # Make GET request to esearch endpoint
    url = f"{BASE_URL}/esearch.fcgi"
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    # Parse JSON response and return idlist
    data = response.json()
    return data['esearchresult']['idlist']





    pass


def fetch_article_details(pmids: list[str]) -> list[dict]:
    """
    Fetch full article details for given PMIDs.
    
    Uses the efetch endpoint: {BASE_URL}/efetch.fcgi
    
    Input:
        pmids = ["39847123", "39845678"]
    
    Output:
        [
            {
                "pmid": "39847123",
                "title": "Post-operative care following total knee arthroplasty",
                "authors": ["Smith J", "Johnson M"],
                "abstract": "Background: Total knee arthroplasty is a common...",
                "journal": "Journal of Bone and Joint Surgery",
                "year": "2023"
            },
            ...
        ]
    
    Example API URL:
        https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39847123,39845678&retmode=xml&api_key=YOUR_KEY
    
    XML Structure to Parse:
        <PubmedArticleSet>
            <PubmedArticle>
                <MedlineCitation>
                    <PMID>39847123</PMID>
                    <Article>
                        <ArticleTitle>Post-operative care...</ArticleTitle>
                        <Abstract>
                            <AbstractText>Background: Total knee...</AbstractText>
                        </Abstract>
                        <AuthorList>
                            <Author>
                                <LastName>Smith</LastName>
                                <Initials>J</Initials>
                            </Author>
                        </AuthorList>
                        <Journal>
                            <Title>Journal of Bone and Joint Surgery</Title>
                        </Journal>
                    </Article>
                    <DateCompleted>
                        <Year>2023</Year>
                    </DateCompleted>
                </MedlineCitation>
            </PubmedArticle>
        </PubmedArticleSet>
    """
    # TODO: Implement
    # 1. Build URL with params: db=pubmed, id=comma_separated_pmids, retmode=xml
    # 2. Make GET request
    # 3. Parse XML using ET.fromstring(response.text)
    # 4. Loop through each PubmedArticle element
    # 5. Extract: PMID, ArticleTitle, AbstractText, Authors, Journal Title, Year
    # 6. Return list of article dicts
    pass


def search_and_save(query: str, output_file: str, max_results: int = 10) -> None:
    """
    Search PubMed and save results to JSON file.
    
    Input:
        query = "appendectomy post operative instructions"
        output_file = "appendectomy_articles.json"
        max_results = 10
    
    Output (saved to appendectomy_articles.json):
        {
            "query": "appendectomy post operative instructions",
            "count": 10,
            "articles": [
                {
                    "pmid": "12345678",
                    "title": "Recovery after appendectomy...",
                    "authors": ["Smith J", "Johnson M"],
                    "abstract": "This study examined...",
                    "journal": "Surgery Today",
                    "year": "2023"
                },
                ...
            ]
        }
    """
    # TODO: Implement
    # 1. Call search_pubmed(query, max_results)
    # 2. Call fetch_article_details(pmids)
    # 3. Build result dict with query, count, articles
    # 4. Save to JSON using json.dump()
    pass


# Test the module
if __name__ == "__main__":
    # Example usage - uncomment to test:
    # 
    # # Test search
    # pmids = search_pubmed("knee replacement post operative care", max_results=5)
    # print(f"Found PMIDs: {pmids}")
    # 
    # # Test fetch
    # articles = fetch_article_details(pmids)
    # for article in articles:
    #     print(f"- {article['title'][:50]}...")
    # 
    # # Test full pipeline
    # search_and_save("knee replacement post operative care", "knee_articles.json", max_results=10)
    # print("Saved to knee_articles.json")
    
    # Test search_pubmed function
    print("Testing search_pubmed()...")
    pmids = search_pubmed("knee replacement post operative care", max_results=5)
    print(f"Found {len(pmids)} PMIDs: {pmids}")