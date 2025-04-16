import requests  # Library to make HTTP requests
from bs4 import BeautifulSoup # Library to parse HTML
import re
from typing import Tuple, List

def extract_article_paragraphs(url):
    """
    Fetches HTML from a URL and extracts text from <p> tags
    within <article id='article-view-content-div'.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        list: A list of strings, where each string is the text
              content of a <p> tag within the specified article.
              Returns an empty list if the article or <p> tags
              are not found.
        None: If there was an error fetching or processing the URL.
    """
    extracted_texts = []
    try:
        # Set a User-Agent header to mimic a browser request
        # Some websites block requests without a valid User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Send an HTTP GET request to the URL with headers and a timeout
        print(f"Fetching content from: {url}")
        response = requests.get(url, headers=headers, timeout=10) # Timeout in seconds

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the specific article tag by its ID
        article_div = soup.find('article', id='article-view-content-div')

        # Check if the article tag was found
        if article_div:
            # Find all <p> tags directly within the found article tag
            p_tags = article_div.find_all('p')

            # Loop through each found <p> tag and extract text
            for p in p_tags:
                text = p.get_text(strip=True)
                # Optionally add only non-empty paragraphs
                if text:
                    extracted_texts.append(text)
            print(f"Successfully extracted {len(extracted_texts)} paragraphs.")
            return extracted_texts
        else:
            # If the specific article div wasn't found on the page
            print(f"Warning: Could not find <article id='article-view-content-div'> on page: {url}")
            return [] # Return an empty list as the target element wasn't found

    except Exception as e:
        raise e

def split_article_content(paragraphs: List[str]) -> Tuple[List[str], List[str]]:
    """
    기사 내용을 소개 부분과 주요 뉴스 부분으로 나눕니다.
    첫 번째 ■ 문자를 기준으로 구분합니다.
    
    Args:
        paragraphs (List[str]): extract_article_paragraphs 함수의 결과물
        
    Returns:
        Tuple[List[str], List[str]]: (소개 문단 리스트, 주요 뉴스 문단 리스트)
    """
    if not paragraphs:
        return [], []
    
    intro_parts = []
    news_parts = []
    found_first_bullet = False
    
    bullet_pattern = re.compile(r"^■")
    email_pattern = re.compile(r"AI타임스\s+news@aitimes\.com")
    
    for para in paragraphs:
        # 이메일 문구는 건너뛰기
        if email_pattern.search(para):
            continue
            
        # 첫 번째 ■를 찾은 경우
        if not found_first_bullet and bullet_pattern.search(para):
            found_first_bullet = True
            news_parts.append(para)
            continue
            
        # 첫 번째 ■ 이전 내용은 intro_parts에
        if not found_first_bullet:
            intro_parts.append(para)
        # 첫 번째 ■ 이후 내용은 news_parts에
        else:
            news_parts.append(para)
    
    return intro_parts, news_parts

if __name__ == "__main__":
    # --- Example Usage ---
    target_url = "https://www.aitimes.com/news/articleView.html?idxno=169645"
    
    # 기사 전체 내용 가져오기
    paragraphs = extract_article_paragraphs(target_url)
    
    if paragraphs is not None:
        if paragraphs:
            # 기사 내용 분리
            intro, news = split_article_content(paragraphs)

            print("\n=== 기사 소개 ===")
            for para in intro:
                print(f"{para}\n")
                
            print("\n=== 주요 뉴스 ===")
            for para in news:
                print(f"{para}\n")
        else:
            print("No paragraphs were found in the specified article section.")
    else:
        print("\nFailed to retrieve or process the webpage due to an error.")
