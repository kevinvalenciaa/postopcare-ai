

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
    # TODO: Implement
    # 1. Build URL with params: db=pubmed, term=query, retmax=max_results, retmode=json
    # 2. Add api_key if available
    # 3. Make GET request
    # 4. Parse JSON response
    # 5. Return idlist
    
    # Build request parameters
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
    
    #coma seperated list of pmids
    pmid_list = ','.join(pmids)
    
    # request parameters 
    params = {
        'db': 'pubmed',
        'id': pmid_list,
        'retmode': 'xml'
    }
    
    #add api key if it's available 
    if API_KEY:
        params['api_key'] = API_KEY
    
    #make the GET request to efetch the endpoint
    url = f"{BASE_URL}/efetch.fcgi"
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    #parse through the xml response 
    root = ET.fromstring(response.text)
    articles = []
    
    # Loop through each PubmedArticle element
    for article_elem in root.findall('.//PubmedArticle'):
        medline_citation = article_elem.find('MedlineCitation')
        if medline_citation is None:
            continue
        
        # Extract the pmid 
        pmid_elem = medline_citation.find('PMID')
        pmid = pmid_elem.text if pmid_elem is not None else ""
        
        # get article information
        article = medline_citation.find('Article')
        if article is None:
            continue
        
        # take the tile 
        title_elem = article.find('ArticleTitle')
        title = title_elem.text if title_elem is not None else ""
        
        # get the abstract 
        abstract_text = ""
        abstract = article.find('Abstract')
        if abstract is not None:
            abstract_text_elem = abstract.find('AbstractText')
            if abstract_text_elem is not None:
                abstract_text = abstract_text_elem.text if abstract_text_elem.text else ""
        
        # get author name
        authors = []
        author_list = article.find('AuthorList')
        if author_list is not None:
            for author in author_list.findall('Author'):
                last_name_elem = author.find('LastName')
                initials_elem = author.find('Initials')
                if last_name_elem is not None and initials_elem is not None:
                    authors.append(f"{last_name_elem.text} {initials_elem.text}")
                elif last_name_elem is not None:
                    authors.append(last_name_elem.text)
        
        # take journla title 
        journal_title = ""
        journal = article.find('Journal')
        if journal is not None:
            journal_title_elem = journal.find('Title')
            journal_title = journal_title_elem.text if journal_title_elem is not None else ""
        
        # take year 
        year = ""
        date_completed = medline_citation.find('DateCompleted')
        if date_completed is not None:
            year_elem = date_completed.find('Year')
            year = year_elem.text if year_elem is not None else ""
        
        #article dictionary with all the article key features
        article_dict = {
            "pmid": pmid,
            "title": title,
            "authors": authors,
            "abstract": abstract_text,
            "journal": journal_title,
            "year": year
        }
        
        articles.append(article_dict)
    
    return articles


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
    
    # Call search_pubmed to get PMIDs
    pmids = search_pubmed(query, max_results)
    
    # Call fetch_article_details to get full article information
    articles = fetch_article_details(pmids)
    
    # Build result dict
    result = {
        "query": query,
        "count": len(articles),
        "articles": articles
    }
    
    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)


# Test the module
if __name__ == "__main__":
    # Example usage - uncomment to test:
    # 
    # # Test search
    # pmids = search_pubmed("knee replacement post operative care", max_results=5)
    # print(f"Found PMIDs: {pmids}")

    
    # Test search_pubmed function
    print("Testing search_pubmed()...")
    pmids = search_pubmed("knee replacement post operative care", max_results=5)
    print(f"Found {len(pmids)} PMIDs: {pmids}")
    print()
    # Test fetch_article_details function
    print("\nTesting fetch_article_details()...")
    articles = fetch_article_details(pmids)
    print(f"Retrieved {len(articles)} articles:")
    for article in articles:
        print(f"  - PMID: {article['pmid']}")
        print(f"    Title: {article['title']}")
        print(f"    Authors: {', '.join(article['authors'][:2])}")
        print()
    
    # Test search_and_save function
    print("Testing search_and_save()...")
    output_file = "knee_articles.json"
    search_and_save("knee replacement post operative care", output_file, max_results=3)
    print(f"Saved results to {output_file}")
    print()
    
    # Display saved file contents
    print("testing save and search results...")
    with open(output_file, 'r') as f:
        saved_data = json.load(f)
        print(f"  Query: {saved_data['query']}")
        print(f"  Count: {saved_data['count']}")
        print(f"  First article title: {saved_data['articles'][0]['title'][:60]}...")
    # Test full pipeline
    search_and_save("knee replacement post operative care", "knee_articles.json", max_results=10)
    print("Saved to knee_articles.json")